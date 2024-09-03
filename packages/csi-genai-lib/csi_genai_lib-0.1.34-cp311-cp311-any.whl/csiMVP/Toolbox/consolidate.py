# ##################################################################################################
#  Copyright (c) 2022.    Caber Systems, Inc.                                                      #
#  All rights reserved.                                                                            #
#                                                                                                  #
#  CABER SYSTEMS CONFIDENTIAL SOURCE CODE                                                          #
#  No license is granted to use, copy, or share this software outside of Caber Systems, Inc.       #
#                                                                                                  #
#  If used, attribution of open-source code is included where required by original author          #
#                                                                                                  #
#  Filename:  consolidate.py                                                                       #
#  Authors:  Rob Quiros <rob@caber.com>  rlq                                                       #
# ##################################################################################################

import warnings
warnings.filterwarnings("ignore")

import re
import pandas as pd
from numpy import nan
from datetime import timedelta, datetime, timezone
from urllib.parse import urlsplit
from hashlib import sha256
from csiMVP.Common.init import CFG
from csiMVP.Common.remote_open import get_object_store_client
from csiMVP.Toolbox.goodies import fnfilter_list, first_valid
from csiMVP.Toolbox.filenames import parse_cori
from csiMVP.Toolbox.pandas_tools import categorical_to_object, in_it, set_x, update_then_concat, validate_df, top_x
from csiMVP.Toolbox.pandas_tools import columns_to_dict_series, explode_dict_column, Iterable, check_df_indices
from csiMVP.Toolbox.service_discovery_tools import get_sid_from_name
from csiMVP.Dependencies.elastic_search_init import ESP

esp = None
DEBUG = (CFG.logLevel == "verbose" or CFG.logLevel == "debug")

# Enforce categories for event.direction and event.class
# ev_dir_cat_type = pd.CategoricalDtype(['<', '-', '>'])
# ev_class_cat_type = pd.CategoricalDtype(['gets', 'puts', 'gets_meta', 'puts_meta', 'deletes', 'creates', 'drop'])
ev_dir_cat_type = 'string'
ev_class_cat_type = 'string'


def convert_message_columns(api_df):
    # If there is data in the request ('source') and the response ('target') we need to create two
    # records instead of one.  This will simplify building the data flow graph later.

    split_df = []
    for d in ['REQ', 'RSP']:
        cbdy = f'C.{d}.body'
        csha = f'C.{d}.sha256'
        if not {cbdy, csha}.difference(api_df.columns):
            no_body = api_df[cbdy].eq('') | api_df[cbdy].isna() | api_df[csha].str.contains(r"^.*NO_BODY$")
            if no_body.all():
                continue

            renamer = in_it({f'C.{d}.headers.Content-Length': 'data.bytes',
                             f'C.{d}.headers.Content-Type': 'data.mime_type',
                             f'C.{d}.headers.Range': 'data.range',
                             f'C.{d}.headers.Content-Range': 'data.range',
                             f'C.{d}.sha256': 'data.sha256',
                             f'C.{d}.base64': 'data.base64',
                             f'C.{d}.body': 'data.body'}, api_df)
            ddf = api_df.loc[~no_body].copy().rename(columns=renamer)
            ddf['index'] = ddf['R.ID'] + ("-P" if d == 'REQ' else '-G')
            ddf['event.time_min'] = ddf['event.time']
            if 'event.latency' in ddf.columns and isinstance(ddf['event.latency'], str) and ddf['event.latency'].isnumeric():
                latency = timedelta(milliseconds=float(ddf['event.latency']))
            elif 'event.latency' in ddf.columns and isinstance(ddf['event.latency'], (int, float)):
                latency = timedelta(milliseconds=ddf['event.latency'])
            elif 'event.latency' in ddf.columns and isinstance(ddf['event.latency'], pd.Series):
                latency = ddf['event.latency'].transform(lambda T: timedelta(milliseconds=T))
            else:
                latency = timedelta(milliseconds=.2)
            if isinstance(ddf['event.time'], str):
                ev_time_max = (datetime.fromisoformat(ddf['event.time']) + latency).isoformat()
            elif isinstance(ddf['event.time'], datetime):
                ev_time_max = ddf['event.time'] + latency
            elif isinstance(ddf['event.time'], pd.Series):  # if isinstance(ddf['event.time'], datetime):
                ev_time_max = pd.to_datetime(ddf['event.time']) + latency
            else:
                raise TypeError(f"event.time is not a string or datetime object: {type(ddf['event.time'])}")

            ddf['event.time_max'] = ev_time_max
            if d == 'RSP':
                ddf['event.time'] = ev_time_max

            ddf['event.direction'] = (">" if d == 'REQ' else '<')
            if "event.id" in ddf.columns:
                ddf = ddf.drop(columns=["event.id"])
            ddf = ddf.set_index('index', drop=False).rename(columns={'index': 'event.id'})

            # Get the data length from the Content-Range header values
            if f'data.range' in ddf.columns and d == 'RSP':
                lbytes = ddf['data.range'].str.startswith('bytes')
                filler = pd.Series('', index=ddf.index, dtype=str)
                dr = ddf.loc[lbytes, 'data.range'].str.split(' ', n=1, expand=True).get(1, filler) \
                    .str.rsplit('/', n=1, expand=True).get(0, filler) \
                    .str.split('-', n=1, expand=True).astype('int')
                lsum = dr.ne('').all(axis=1)
                dr.loc[lsum] = dr.loc[lsum].astype(int)
                ddf['data.bytes'] = dr.loc[lsum, 1] - dr.loc[lsum, 0] + 1  # Range is inclusive

            split_df.append(ddf.copy())

    if len(split_df) > 1:
        rr_df = pd.concat(split_df)
    elif len(split_df) == 1:
        rr_df = split_df[0]
    else:
        rr_df = pd.DataFrame()

    if not rr_df.empty:
        api_df.drop(index=rr_df['R.ID'].drop_duplicates(), inplace=True)

    if not api_df.empty:
        api_df["event.direction"] = "-"
        api_df["event.id"] = api_df["R.ID"] + "-N"
        api_df.set_index("event.id", drop=False, inplace=True)

    api_df = pd.concat([rr_df, api_df])
    api_df = api_df[api_df.index.notnull()]
    api_df['event.source.name'] = f"caber:{CFG.modhome.lower()}:etl"
    api_port = api_df['C.REQ.headers.Host'].str.rsplit(':', n=1, expand=True)
    if len(api_port.columns) > 1:
        api_df['api.host.port'] = api_port[1]

    renamer = {
        # 'event.id': 'R.ID',    # Just set above
        # 'event.source.name': f"caber:{CFG.modhome.lower()}:etl",
        # 'event.source.version': 'R.VERSION',
        'event.time': 'event.time',
        'event.code': 'C.RSP.code',
        'event.latency': 'event.latency',
        # 'event.method.name': 'C.REQ.method',      # Set @ process.py 444
        # 'object.copysource': '',
        # 'event.headers': "C.REQ.headers",
        # 'event.headers': "C.RSP.headers",
        'event.query': 'C.REQ.query',
        'event.params': 'C.REQ.params',

        # 'user.type': "",          # Set @ process.py 537
        # 'user.name': "user.name",    # Set @ process.py 535
        # 'user.auth_to_process': "user.auth_to_process",
        'user.ua': 'C.REQ.headers.User-Agent',
        # 'user.from.host.name': "user.from.host.name",
        # 'user.acceptor':          # Set @ process.py 496
        # 'user.acct_id': "",
        # 'user.access_key': "",
        # 'user.session': 'user.session',

        'api.scheme': 'C.REQ.headers.Origin',  # .transform(lambda x: urlsplit(x).scheme)
        # 'api.host.type': api.host.type",                 # Set @ API_Tap.main
        # 'api.name': 'R.API',                   # Set @ API_Tap.main
        # 'api.host.port': 'C.REQ.headers.Host',   # lit(':', 1, expand=True)[1]
        # 'api.path': "C.REQ.path",             # Set @ API_Tap.main
        'api.host.type': "C.RSP.headers.Server",

        # 'object.sha256': 't',
        # 'object.host.name': provider_host,
        # 'bucket.name': t_bkt,
        # 'object.name': t_obj,
        # 'object.id': cori,
        # 'object.etag': 'C.RSP.headers.ETag',
        # 'object.region': 'awsRegion',
        # 'object.mime_type': dtype,
        # 'object.time.last_modified': "C.RSP.headers.Last-Modified",

        # 'data.bytes': 'C.REQ.headers.Content-Length',
        # 'data.mime_type': 'C.REQ.headers.Content-Type',
        # 'data.sha256': 'C.REQ.sha256',
        # 'data.base64': 'C.REQ.base64',
        # 'data.body': 'C.REQ.body',
        #
        # 'data.bytes': 'C.RSP.headers.Content-Length',
        # 'data.mime_type': 'C.RSP.headers.Content-Type',
        # 'data.sha256': 'C.RSP.sha256',
        # 'data.base64': 'C.RSP.base64',
        # 'data.body': 'C.RSP.body.'
    }

    renamer1 = {v: k for k, v in renamer.items() if v in api_df.columns}  # Swap keys and values
    df_api = api_df.copy().rename(columns=renamer1)

    api_df = columns_to_dict_series(api_df, base="C.REQ.headers", replace_in_df=True)
    api_df = columns_to_dict_series(api_df, base="C.RSP.headers", replace_in_df=True)
    api_df = columns_to_dict_series(api_df, base="C.REQ.cookies", replace_in_df=True)

    k = [k for k in df_api.columns if k.split('.', 1)[0] in ['event', 'object', 'bucket', 'user', 'data', 'api', 'host']]

    api_df = update_then_concat(api_df, df_api[k], axis=1, skip_dindex_empty=False)
    renamer2 = {"C.REQ.headers": 'event.headers.req', "C.RSP.headers": 'event.headers.rsp'}
    api_df.rename(columns=renamer2, inplace=True)

    # api_df = columns_to_dict_series(api_df, base="user", replace_in_df=True)
    api_df = columns_to_dict_series(api_df, base="event.headers", replace_in_df=True)

    filler = pd.Series('', index=api_df.index, dtype=str)
    api_df['R.ID'] = api_df['event.id']
    api_df['api.path'] = api_df.get('api.path', filler).str.strip('/')
    api_df['api.scheme'] = api_df.get('api.scheme', filler).transform(lambda x: urlsplit(x).scheme)
    api_df['api.host.name'] = api_df.get('api.host.name', filler).str.strip('/')
    api_df.set_index("event.id", drop=False, inplace=True)

    drop_cols = [c for c in api_df.columns if c.startswith('C.')]
    drop_cols.extend(['R.API', 'R.VERSION', 'event.cookies'])
    api_df.drop(columns=in_it(drop_cols, api_df), inplace=True)

    return api_df


def filter_columns_to_link_data(indf, drop_if_endswith='', id_col_name=''):
    """
    One final resting place for aall those columns in ingested DataFrames that we no longer
    need to keep around. For consistency in drops.

    Column names that end with 'drop_if_endswith' will also be dropped.
    """
    xdf = indf.copy()

    r_keeps = {'event.time', 'R.ID'} if not id_col_name else {'event.time', 'R.ID', id_col_name}
    db_keeps = [k for k in xdf.columns if k.split('.', 1)[0] in
                ['event', 'object', 'bucket', 'user', 'data', 'api', 'host']]
    db_drops = ['eventSource', 'eventName', 'eventTime', 'eventVersion']

    r_keeps = r_keeps.union(db_keeps).difference(db_drops)

    if drop_if_endswith:
        r_keeps = [r for r in r_keeps if not r.endswith(drop_if_endswith)]

    drop_cols = xdf.columns.difference(r_keeps)
    xdf.drop(columns=in_it(drop_cols, xdf), inplace=True)

    xdf[xdf.isna()] = nan
    xdf[xdf.isin([''])] = nan

    return xdf.sort_index(axis=1)


def fill_id_dat(evdf, fill_na_only=False, col_cori='object.id', col_sha='object.sha256',
                col_nmers_pri='data.nmers.primary', col_nmers_sec='data.nmers.total'):

    if isinstance(evdf, pd.DataFrame):
        missing_columns = {col_sha, col_nmers_pri, col_nmers_sec}.difference(evdf.columns)
        if missing_columns:
            if DEBUG:
                print(f"[WARNING] fill_id_dat: DataFrame missing required columns {missing_columns}")
            return evdf

        # Check if there is an object in target_cori, but it doesn't have a good SHA-256
        null_sha = evdf[col_sha].isna() | evdf[col_sha].isin(CFG.G.get("nullMsgSha256s", {}).values())
        bad_sha = evdf[col_sha].isin(CFG.G.get("badMsgSha256s", {}).values())
        true_column = pd.Series(True, index=evdf.index, dtype=bool)

        nmers_pri = evdf[col_nmers_pri].copy().fillna(0).astype(int).astype(str)
        nmers_sec = evdf[col_nmers_sec].copy().fillna(0).astype(int).astype(str)

        if col_cori not in evdf.columns:
            no_cori = true_column
        else:
            no_cori = evdf[col_cori].isna()

        if 'data.id' not in evdf.columns or not fill_na_only:
            fill_ok = true_column
        else:
            fill_ok = evdf['data.id'].isna()

        evdf.loc[~null_sha & ~bad_sha & fill_ok, 'data.id'] = evdf[col_sha] + '-' + nmers_pri + '-' + nmers_sec

        evdf.loc[null_sha & fill_ok & ~no_cori, 'data.id'] = evdf[col_sha] + "-0-0"
        evdf.loc[null_sha & fill_ok & ~no_cori, [col_nmers_pri, col_nmers_sec]] = [0, 0]

        evdf.loc[bad_sha & fill_ok & ~no_cori, 'data.id'] = 'redacted!' + evdf[col_sha]

        evdf.loc[null_sha & fill_ok & no_cori, 'data.id'] = '(no_content!no_target)'
        evdf.loc[bad_sha & fill_ok & no_cori, 'data.id'] = '(redacted!no_target)'

        evdf['valid_id_dat'] = evdf['data.id'].str.count('!').gt(0)

        return evdf

    elif isinstance(evdf, dict):
        missing_keys = {col_sha, col_nmers_pri, col_nmers_sec}.difference(evdf.keys())
        if missing_keys:
            if DEBUG:
                print(f"[WARNING] fill_id_dat: Input dict missing required keys {missing_keys}")
            return evdf

        # Check if there is an object in target_cori, but it doesn't have a good SHA-256
        null_sha = not evdf.get(col_sha) or evdf.get(col_sha) in CFG.G.get("nullMsgSha256s", {}).values()
        bad_sha = evdf.get(col_sha) in CFG.G.get("badMsgSha256s", {}).values()
        no_cori = not evdf.get(col_cori)

        valid_sha = not null_sha and not bad_sha

        def _check_int(n):
            if isinstance(n, str) and n.isnumeric() or isinstance(n, (int, float)):
                return str(int(n))
            else:
                return '0'

        nmers_pri = _check_int(evdf.get(col_nmers_pri))
        nmers_sec = _check_int(evdf.get(col_nmers_sec))

        if valid_sha:
            id_dat = evdf[col_sha] + '-' + nmers_pri + '-' + nmers_sec
        elif not no_cori:
            if null_sha:
                id_dat = evdf[col_sha] + '-0-0'
            elif bad_sha:
                id_dat = 'redacted!' + evdf[col_sha]
        else:
            if null_sha:
                id_dat = 'no_content!no_target'
            else:
                id_dat = 'redacted!no_target'
        return id_dat, valid_sha

    else:
        if DEBUG and evdf is not None:
            print(f"[WARNING] fill_id_dat: Input must be type DataFrame or Dict not {type(evdf).__qualname__}")
        return evdf

s3_event_map = {k.lower(): v for k, v in CFG.G.get("s3EventMap").items() if v and v != "ignore"}
s3_event_map |= {k.lower(): v for k, v in CFG.G.get("apiEventMap").items() if v and v != "ignore"}


def _process_method_code(method, code='', headers='', ):
    # Post operations can be gets and/or puts - mark as 'dir' and resolve later

    # map_3 = {'get': 'get', 'put': 'put', 'mov': 'put', 'pos': 'dir', 'mkc': 'put_meta', 'cop': 'copy',
    #          'unl': 'put_meta', 'pat': 'put_meta', 'del': 'delete', 'hea': 'get_meta', 'pro': 'map_5',
    #          'loc': 'put_meta', 'tra': 'get_meta', 'opt': 'get_meta', 'lis': 'get_meta', 'cre': 'put_meta',
    #          'com': 'put', 'upl': 'put'}
    # map_5 = {'propp': 'put_meta', 'propf': 'get_meta'}

    if isinstance(method, str) and isinstance(code, str):
        r = None
        p = False

        r = s3_event_map.get(method.lower(), "ignore")
        #
        # if len(method) >= 3:
        #     r = map_3.get(method[0:3].lower(), None)
        #     if r == 'map_5' and len(method) >= 5:
        #         r = map_5.get(method[0:5].lower(), None)
        if not r.endswith("meta") and code == '304':
            r = r + "_meta"
        if code != '304' and code.startswith('3') or code.startswith('4') or code.startswith('5'):
            r = 'drop'
        if code == '206':   # Partial content response https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/206
            p = True
        if isinstance(headers, dict):
            p = headers.get('req', {}).get('Range', headers.get('req', {}).get('range'))
            if not p:
                p = headers.get('rsp', {}).get('Content-Range', headers.get('rsp', {}).get('content-range'))
            if not p:
                p = False
        if code == '201':   # Created response code https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/201
            r = 'create'
        return r, p

    elif isinstance(method, pd.Series):
        out = method.str.lower().map(s3_event_map)
        # len3 = method.str.len().ge(3)
        # len5 = method.str.len().ge(5)
        # out = method[len3].str.lower().str.slice(0, 3).map(map_3)
        # map5 = out.eq('map_5')
        # if map5.any():
        #     out[map5] = method[len5].str.lower().str.slice(0, 5).map(map_5)

        out = out.to_frame('event.method.type')
        out['indx'] = out.index
        p = out['indx'].str.endswith('P')
        g = out['indx'].str.endswith('G')
        post = out['event.method.type'].eq('dir')
        out.loc[post & p, 'event.method.type'] = 'put'
        out.loc[post & g, 'event.method.type'] = 'get'
        out.loc[post & ~g & ~p, 'event.method.type'] = 'put_meta'
        out = out['event.method.type'].astype('str')

        null = pd.Series(nan, dtype='O')
        false = pd.Series(False, dtype=bool)
        rsp_version = pd.Series(name='rsp_version', dtype=str)
        create = pd.Series(dtype=bool)
        partial = pd.Series(dtype=bool)
        no_data = pd.Series(dtype=bool)
        in_cache = pd.Series(dtype=bool)
        delete_marker = pd.Series(dtype=bool)

        if isinstance(code, pd.Series) and not code.empty:
            create = code[code.notna()].astype(str).eq('201')
            in_cache = code[code.notna()].astype(str).eq('304')      # Treat GETs that return 304 as a regular GET

            drop = (code[code.notna()].astype(str).ne('304') &
                    code[code.notna()].astype(str).str.startswith('30')) | \
                    code[code.notna()].astype(str).str.startswith('4') | \
                    code[code.notna()].astype(str).str.startswith('5')

            is_meta = out.str.endswith('meta')
            partial = code[code.notna()].astype(str).eq('206')           # Response has only partial content of object
            no_data = code[code.notna()].astype(str).eq('204')           # Response has no content

            # out[is_cached & ~is_meta] = out[is_cached & ~is_meta] + "_meta"
            out[drop] = "drop"

        if isinstance(headers, pd.Series) and not headers.empty and headers.notna().any():
            byte_range = headers.copy()
            byte_range.name = 'byte_range'
            delete_marker = headers.copy()
            delete_marker.name = 'delete_marker'
            rsp_version = headers.copy()
            rsp_version.name = 'rsp_version'

            byte_range[headers.notna()] = headers[headers.notna()].apply(
                lambda H: H.get('req', {}).get('Range', H.get('req', {}).get('range')))

            byte_range[byte_range.isna()] = headers[headers.notna()].apply(
                lambda H: H.get('rsp', {}).get('Content-Range', H.get('rsp', {}).get('content-range')))

            byte_range[byte_range.eq("bytes=0-")] = nan     # Range request that returns all the bytes
            if not byte_range.empty and byte_range.notna().any():
                partial[headers.notna()] = byte_range[headers.notna()].notna().copy()
                partial.name = 'event.flag.partial'

            delete_marker[headers.notna()] = headers[headers.notna()].apply(
                lambda H: H.get('rsp', {}).get('x-amz-delete-marker',
                                               H.get('rsp', {}).get('X-Amz-Delete-Marker')))

            rsp_version[headers.notna()] = headers[headers.notna()].apply(
                lambda H: H.get('rsp', {}).get('x-amz-version-id',
                                               H.get('rsp', {}).get('X-Amz-Version-Id')))

        out = pd.concat([out, out.eq('get'), out.eq('put'), out.eq('copy'), out.eq('get_meta'), out.eq('put_meta'),
                         out.eq('delete'), create, partial, rsp_version, delete_marker, no_data, in_cache, out.eq('drop')], axis=1)

        out.columns = ['event.method.type', 'event.type.gets', 'event.type.puts', 'event.type.copies', 'event.type.gets_meta',
                       'event.type.puts_meta', 'event.type.deletes', 'event.flag.creates', 'event.flag.partial',
                       'rsp_version', 'event.flag.delete_marker', 'event.flag.no_data', 'event.flag.in_cache', 'drop']

        return out


def normalize_event_records(node, drops=True, fillnans=False):
    """
    Cast columns to bool, str, int, float as appropriate.  Fill nans in those columns with type-appropriate
    values if parameter 'fillnans' is True (default=False).  Time values will have been converted when
    read from the datebase (elastic_search_init.fix_times)

    Pick out and normalize events the input data frames from the 'event.method.name', 'event.code',
    and certain 'event.headers'.

    Output a copy of the input data frame with new column 'event.method.type' and boolean columns
    'event.type.gets', 'event.type.puts', 'event.type.gets_meta', 'event.type.puts_meta', 'event.type.deletes',
    'event.flag.creates', 'event.flag.partial', 'drop'

    If an event is not useful (certain 3xx sttus codes) mark the event as 'drop' and, if parameter 'drops'
    is True (default=True), drop all columns so marked.

    """

    # # The following columns typically are in the input data frame (no guarantees!)
    # node.columns.to_list()
    # ['R.ID', 'RecordModifiedBy', 'api.host.name', 'api.host.port', 'api.host.type', 'api.path', 'api.scheme',
    #  'bucket.name', 'data.bytes', 'data.content.length.key_val', 'data.content.length.text', 'data.id',
    #  'data.index.de_dupe', 'data.index.name', 'data.index.time.scanned', 'data.mime_type', 'data.nmers.primary',
    #  'data.nmers.total', 'data.sha256', 'event.code', 'event.compressed_data', 'event.direction', 'event.id',
    #  'event.latency', 'event.method.name', 'event.source.name', 'event.source.version', 'event.time',
    #  'object.etag', 'object.host.name', 'object.id', 'object.mime_type', 'object.name', 'object.sha256',
    #  'object.time.last_modified', 'object.use_hash', 'user.access_key', 'user.acct_id', 'user.acceptor',
    #  'user.auth_to_process', 'user.type', 'user.from.host.name', 'user.name', 'user.ua']
    
    if not isinstance(node, pd.DataFrame) or node.empty:
        return node

    # Drop columns we don't need.
    drop_cols = ['RecordModifiedBy']
    node.drop(columns=in_it(drop_cols, node), inplace=True)

    # Fix data types of each column.  Start by assuming all columns are objects, then update with specifics
    time_cols = node.dtypes[node.dtypes.eq('datetime64[ns, UTC]')].index.to_list()
    as_typer = {k: 'O' for k in node.columns if k not in time_cols}

    str_cols = {k: 'string' for s in ['id', 'arn', 'name', 'sha256', 'version'] for k in node.columns if k.endswith(s)}
    as_typer.update(str_cols)

    t_special = {'event.code': 'int32',
                 'object.bytes': 'int64',
                 'data.bytes': 'int64',
                 'data.nmers.primary': 'int32',
                 'data.nmers.total': 'int32',
                 'data.content.length.key_val': 'int64',
                 'data.content.length.text': 'int64',
                 'api.host.port': 'int32',
                 'data.index.de_dupe': 'float32',
                 'event.latency': 'float32',
                 'event.compressed_data': 'bool',
                 'object.use_hash': 'bool',
                 'event.direction': ev_dir_cat_type}
    as_typer.update(t_special)

    new_typer = {'event.method.type': ev_class_cat_type,
                 'event.type.gets': 'bool',
                 'event.type.puts': 'bool',
                 'event.type.copies': 'bool',
                 'event.type.gets_meta': 'bool',
                 'event.type.puts_meta': 'bool',
                 'event.type.deletes': 'bool',
                 'event.flag.creates': 'bool',
                 'event.flag.partial': 'bool',
                 'event.flag.delete_marker': 'bool',
                 'event.flag.in_cache': 'bool',
                 'event.flag.no_data': 'bool',
                 'drop': 'bool'}

    fill_key = {'string': '', 'O': '', 'int64': 0, 'float64': 0.0, 'bool': False,
                ev_dir_cat_type: '-', ev_class_cat_type: 'drop'}

    node = node.astype(in_it(as_typer, node), errors='ignore')

    if fillnans:
        fillna = {k: fill_key.get(v, nan) for k, v in as_typer.items()}
        node = node.fillna(fillna)

    if not {'event.method.name', 'event.code', 'event.headers'}.difference(node.columns):
        e_op = _process_method_code(node['event.method.name'],
                                    node['event.code'],
                                    node['event.headers'])
    elif not {'event.method.name', 'event.code'}.difference(node.columns):
        e_op = _process_method_code(node['event.method.name'],
                                    node['event.code'])
    elif not {'event.method.name'}.difference(node.columns):
        e_op = _process_method_code(node['event.method.name'])
    else:
        row_vals = ['drop', False, False, False, False, False, False, False, False, False, False, False, True]
        e_op = pd.DataFrame([row_vals] * node.index.shape[0], columns=list(new_typer.keys()), index=node.index)

    # This function is the only one where 'event.method.type' and the index Selectors are created.
    # So if they are present in the input data frame it's safe to remove them and re-add as done below.
    outdf = pd.concat([node[node.columns.difference(e_op.columns)].copy(), e_op], axis=1)

    outdf = outdf.astype(in_it(new_typer, outdf), errors='ignore')

    # Post operations can be gets and/or puts
    ldir = outdf['event.method.type'].eq('dir')
    lget = outdf['event.direction'].eq('<')     # Post operations can be gets or puts
    lput = outdf['event.direction'].eq('>')     # Post operations can be gets or puts
    outdf.loc[ldir & lget, ['event.method.type', 'event.type.gets']] = ['get', True]
    outdf.loc[ldir & lput, ['event.method.type', 'event.type.puts']] = ['put', True]
    outdf.loc[ldir & ~lput & ~lget, ['event.method.type', 'event.type.puts_meta']] = ['put_meta', True]

    if fillnans:
        fillna = {k: fill_key.get(v, nan) for k, v in new_typer.items()}
        outdf.fillna(value=fillna, inplace=True)

    message = '{"Events": {'
    for k in in_it(new_typer.keys(), outdf):
        typ = k.rsplit('.', 1)[-1]
        if typ not in ['name', 'drop']:
            num = outdf[k].value_counts().get(True, 0)
            message += f'"{typ}": "{num}", '
    print(message[:-3] + '}}') if len(message) > 12 else None

    # Drop events that were marked to drop (redirects, errors, etc)
    if 'drop' in outdf.columns and drops:
        num = outdf['drop'].value_counts().get(True, 0)
        outdf.drop(index=outdf.loc[outdf.get('drop', False)].index, inplace=True)
        outdf.drop(columns=['drop'], inplace=True)
        print(f"Dropped {num} events that were HTTP redirects or bad status")

    return outdf


def merge_objects_into_events(events, objdf=None):
    # This function is intended to be run after the object indices have been scanned and
    # CFG.G["dbTables"]["objScanTable"] has been populated

    global esp
    if esp is None:
        esp = ESP(CFG)

    # FIXME: Expensive way to do merge.  Leverage ElasticSearch to merge directly maybe using
    #    https://stackoverflow.com/questions/63027343/elasticsearch-merge-multiple-indexes-based-on-common-field

    if not isinstance(events, pd.DataFrame) or events.empty or \
            {'target_cori', 'target_sha256'}.difference(events.columns):
        if DEBUG and not isinstance(events, pd.DataFrame):
            print(f"[DEBUG] Objects DataFrame is not a DataFrame. It's a {type(events).__qualname__}")
        elif DEBUG:
            is_missing = 'is missing ' + str({'target_cori', 'target_sha256'}.difference(events.columns))
            print(f"[DEBUG] Event DataFrame {'is empty ' if events.empty else is_missing}")
        return events

    if objdf is None:
        query = {"query": {"match_all": {}}}
        table = CFG.G["dbTables"]["objScanTable"]
        objdf = esp.esp_query(table, query)

    if not isinstance(objdf, pd.DataFrame) or objdf.empty or \
            {'object.use_hash', 'data.nmers.total', 'object.sha256', 'data.sha256'}.difference(objdf.columns):
        if DEBUG and not isinstance(objdf, pd.DataFrame):
            print(f"[DEBUG] Objects DataFrame is not a DataFrame. It's a {type(objdf).__qualname__}")
        elif DEBUG:
            is_missing = 'is missing ' + str({'object.use_hash', 'data.nmers.total', 'object.sha256',
                                              'data.sha256'}.difference(objdf.columns))
            print(f"[DEBUG] Objects DataFrame {'is empty ' if objdf.empty else is_missing}")
        return events

    objdf['object.use_hash'] = objdf['object.use_hash'].astype(bool)

    # There should be no duplicate values of hashes for the objects identified by hash
    assert not objdf.loc[objdf['object.use_hash'], 'object.sha256'].value_counts().gt(1).any()

    # if 'index' not in objdf.columns and 'data.index.name' in objdf.columns:
    #     objdf.rename(columns={'data.index.name': 'index'}, inplace=True)
    # if 'nmers' not in objdf.columns and 'data.nmers.total' in objdf.columns:
    #     objdf.rename(columns={'data.nmers.total': 'nmers'}, inplace=True)

    locp = events.index.str.startswith(CFG.D["Process_API"]["filePrefix"])
    apidf = events.loc[locp].copy()

    locs = events.index.str.startswith(CFG.D["S3_Scanner"]["filePrefix"])
    s3sdf = events.loc[locs].copy()

    events = events.loc[~locp & ~locs]

    dcols = {'data.nmers.primary', 'data.nmers.total', 'data.index.name', 'object.sha256', 'data.sha256'}.intersection(apidf.columns)
    apidf.drop(columns=list(dcols), inplace=True)
    dcols = {'data.nmers.primary', 'data.nmers.total', 'data.index.name', 'object.sha256', 'data.sha256'}.intersection(s3sdf.columns)
    s3sdf.drop(columns=list(dcols), inplace=True)

    if not s3sdf.empty:
        cols = ['data.nmers.primary', 'data.index.name', 'object.sha256', 'data.sha256']
        s3 = pd.merge(s3sdf, objdf.loc[~objdf['object.use_hash'], cols],
                      left_on='target_cori', right_index=True, how='left')

        s3['data.sha256'] = s3['data.sha256'].astype(str)
        if "data.nmers.total" in s3.columns:
            s3.fillna({'data.nmers.primary': s3['data.nmers.total']}, inplace=True)
            s3.drop(columns=['data.nmers.total'], inplace=True)
        events = pd.concat([s3, events], axis=0)

    if not apidf.empty:
        cols = ['data.nmers.primary', 'data.index.name', 'object.sha256', 'data.sha256']
        apidf = pd.merge(apidf, objdf.loc[objdf['object.use_hash'], cols],
                         left_on='target_sha256', right_on='object.sha256', how='left')

        apidf.set_index('R.ID', drop=False, inplace=True)

        apidf['data.sha256'] = apidf['data.sha256'].astype(str)
        if "data.nmers.total" in apidf.columns:
            apidf.fillna({'data.nmers.primary': apidf['data.nmers.total']}, inplace=True)
            apidf.drop(columns=['data.nmers.total'], inplace=True)

    out = pd.concat([apidf, events], axis=0)
    out = categorical_to_object(out)

    if not out.empty:
        # Now create a consistent identifier for data nodes that uses the concatenation of target_sha256,
        # nmers_pri (data.nmers.primary), and nmers_sec (N.LenSec) we used in sequence.py to create the CQF index names.
        # Leave be lines where target_sha256 starts with '<no_content...' from normalize_event_class_from_event_df above

        # out["target_sha256"].fillna('0'*64, inplace=True)

        fill_na = {'data.nmers.primary': 0, 'object.sha256': out['target_sha256'], 'data.sha256': out['target_sha256']}
        out.fillna(fill_na, inplace=True)
        out = fill_id_dat(out)

    return out


def update_api_ids(indf):
    """
    Updates the API IDs in the given pandas DataFrame.

    Args:
        indf (pandas.DataFrame): The input DataFrame containing API data.

    Returns:
        pandas.DataFrame: The updated DataFrame with API IDs.
        pandas.Series: A series containing the API IDs.

    Raises:
        None

    This function takes a pandas DataFrame as input and performs various operations to update the API IDs in the DataFrame.
    It checks if the input DataFrame has the required columns and is not empty. It then copies the DataFrame and performs
    several transformations such as filling in host IDs, renaming columns, and generating new columns based on API names and paths.
    Finally, it generates unique IDs and names for the APIs, performs aggregations, and updates Elasticsearch lists.

    If the input DataFrame does not meet the required conditions, it is returned as is along with an empty API ID series.
    """
    global esp
    if esp is None:
        esp = ESP(CFG)

    def _shortest_string(row):
        # Filter the values that have more than 5 characters
        filtered_values = [value for value in row if (isinstance(value, str) and len(value) > 3)]
        if filtered_values:
            # Return the shortest among them
            return min(filtered_values, key=len)
        return ''

    cols = {"api.host.name", "event.time", "api.path", "event.method.name"}

    if isinstance(indf, pd.DataFrame) and not cols.difference(indf.columns) and not indf.empty:
        xdf = indf.copy()

        if 'api.name' not in xdf.columns:
            xdf['api.name'] = nan

        # Get the host.id for the api host name
        xdf = fill_in_host_ids(xdf, base_col='api.host', host_col='name', include_cols=['host', 'host_full'])
        host_cols = in_it(['api.host.host', 'api.host.host_full'], xdf)
        xdf['api.host.name'] = xdf[host_cols].apply(_shortest_string, axis=1)
        xdf.rename(columns={'api.host.host_id': 'api.host.id'}, inplace=True, errors='ignore')

        xdf['api.time.last_called'] = xdf['event.time'].apply(pd.to_datetime)

        w_api = xdf['api.name'].notna() & xdf['api.name'].ne('') 
        w_pth = xdf['api.path'].notna() & xdf['api.path'].ne('')
        if w_api.any():
            xdf.loc[w_api & w_pth, 'api_name'] = xdf.loc[w_api & w_pth, 'api.name'] + '/' + xdf.loc[w_api & w_pth, 'api.path']
            xdf.loc[w_api & ~w_pth, 'api_name'] = xdf.loc[w_api & ~w_pth, 'api.name']
            xdf.loc[~w_api & w_pth, 'api_name'] = xdf.loc[~w_api & w_pth, 'api.path']
            xdf.loc[~w_api & ~w_pth, 'api_name'] = ''
        else:
            xdf.loc[w_pth, 'api_name'] = xdf.loc[w_pth, 'api.path']
            xdf.loc[~w_pth, 'api_name'] = ''

        xdf['api_name'] = xdf['api_name'].str.strip('/')

        api_ext = pd.concat([xdf['api.host.name'], xdf['api_name'].str.split("/", expand=True)], axis=1)
        # While path parameters in API calls may be url quoted, elements in API paths will not be.  The lines
        # below will clear out any path elements with '%' and all the succeeding path elements.
        for c in range(0, api_ext.shape[1] - 1):
            loco = api_ext[c].str.contains('%')
            api_ext.loc[loco, c] = pd.NA
        for c in range(1, api_ext.shape[1] - 1):
            loco = api_ext[c - 1].isna()
            api_ext.loc[loco, c] = pd.NA

        api_ext.rename(columns={c: f'api.path.{c}' for c in api_ext.columns if isinstance(c, int)}, inplace=True)
        must_cols = api_ext.columns.to_list()

        xdf = pd.concat([xdf.drop(columns=in_it(must_cols, xdf)), api_ext], axis=1)

        names = ['api.id', 'api.name']
        xdf, ids = generate_id_name_and_key(xdf, must_have_id_cols=must_cols[0:2], include_id_cols=must_cols[2:],
                                            id_prefix='API-', id_col_name=names[0], id_name_name=names[1],
                                            separator_list='/')

        aggs = {"event.method.name": "set_x", "event.query": "set_x", "event.params": "set_x",
                "user.id": "set_x", "event.source.name": "set_x", 'api.time.last_called': "max"}
        tcols = ['api.time.last_called']
        no_do = [c for c in xdf.columns if c not in aggs.keys() and
                 c.split('.')[0] in ['user', 'event', 'data', 'object', 'bucket', 'R', 'M']]
        no_do.extend(['RecordModifiedBy', 'api_name', 'api.path', 'drop', 'creates', 'deletes', 'gets',
                      'gets_meta', 'partial', 'puts', 'puts_meta', 'api.host.ports', 'api.host.type'])

        index = CFG.G["dbTables"].get("apiMapTable", "csi_api_map")

        return esp.update_es_lists(xdf, id_col_name='api.id', agg_dict=aggs,
                               exclude_cols=no_do, time_cols=tcols, index=index)

    else:
        return indf, pd.Series(name='api.id', dtype='object')


def generate_id_name_and_key(indf, must_have_id_cols=None, include_id_cols=None, id_prefix='ID',
                             id_col_name='', id_name_name='', separator_list='/'):
    """
    Concatenate strings in all of must_have_id_cols and include_id_cols, then hash to create a
    hopefully unique identifier to use as an index value in OpenSearch.  Returns the string
    used to create the ID in column id_name_name, and the ID itself in id_name_name.

    The ordering of columns in must_have_id_cols, and include_id_cols is preserved.  However,
    the must_have_id_cols always preceed the include_id_cols when creating the id_name.

    Any include_id_cols not present in the input dataframe xdf will be created, and all NAN/None
    values in the dataframe will be filled using na_fill (passed to pd.DataFrame.fillna())
    before contatenation.

    In creating the string id_name, use string na_fill to fill empty values in xdf, and
    use srparator when concatenating the elements in the columns.

    id_name is then hashed and the result with id_prefix prepended is put in id_col.

    """

    def _join_with_separator_list(value_list, separators):
        if isinstance(separators, str):
            separators = [separators]

        # There need to be n-1 separators for n values.  If there are fewer, the last (or only),
        # separator will be used
        nmax = len(separators) - 1

        outval = value_list[0]
        for n in range(1, len(value_list)):
            s = min(n - 1, nmax)
            # print(f"({s}:{n}) {outval}, {value_list[n]}")
            outval = separators[s].join([outval, value_list[n]])
        return outval.strip(separators[-1])

    if not isinstance(indf, pd.DataFrame):
        raise TypeError(f"Argument 'indf' must be of type pandas.DataFrame")

    idpf_pd = isinstance(id_prefix, (pd.Series, pd.DataFrame, pd.Index))
    idpf_ok = (idpf_pd and not id_prefix.empty) or (not idpf_pd and id_prefix)
    
    id_prefix = "ID" if not idpf_ok else id_prefix
    id_col_name = "out.id" if not id_col_name else id_col_name
    id_name_name = "out.name" if not id_name_name else id_name_name

    # Try to convert all columns to string dtype, and keep only those columns that end up being strings
    incols = [(must_have_id_cols, indf.columns.to_list()), (include_id_cols, [])]
    outcols = []
    for ic, default in incols:
        if isinstance(ic, pd.DataFrame):
            ic = ic.columns
        if isinstance(ic, (pd.Series, pd.Index)):
            ic = ic.to_list()
        if isinstance(ic, Iterable):
            ic = in_it(ic, indf)
        outcols.append(ic if ic else default)

    must_have_id_cols = in_it(outcols[0], indf)
    include_id_cols = in_it([c for c in outcols[1] if c not in must_have_id_cols], indf)

    mhic = indf[must_have_id_cols].astype({c: 'string' for c in must_have_id_cols}, errors='ignore')
    incl = indf[include_id_cols].astype({c: 'string' for c in include_id_cols}, errors='ignore')

    must_have_id_cols = [c for c in must_have_id_cols if c in mhic.dtypes[mhic.dtypes.eq('string')].index]
    include_id_cols = [c for c in include_id_cols if c in incl.dtypes[incl.dtypes.eq('string')].index]

    xdf = indf.copy()

    good_id = xdf[must_have_id_cols].notna().all(axis=1) & xdf[must_have_id_cols].ne('').all(axis=1)

    sorted_cols = must_have_id_cols
    if include_id_cols:
        sorted_cols.extend(include_id_cols)

    cols_to_create = list(set(sorted_cols).difference(xdf.columns))
    xdfc = xdf.loc[good_id].copy()
    if cols_to_create:
        xdfc[cols_to_create] = nan

    id_name = xdfc[sorted_cols]
    # id_name[id_name.eq('')] = nan   # Must fill empty values with '' so that we can strip the separators off
    if not id_name.empty:
        id_name = id_name.fillna('').astype('str')
        id_name = id_name.apply(_join_with_separator_list, separators=separator_list, axis=1)
        id_name.name = id_name_name
    else:
        id_name = pd.Series(name=id_name_name, dtype='O')

    id_col = pd.util.hash_pandas_object(id_name, index=False, hash_key='91BC8B2C08341B49').astype('str')
    id_col = id_prefix + id_col
    id_col.name = id_col_name

    xdf_cols = xdf.columns.difference([id_col_name, id_name_name])
    xdf_rows = xdf.index.difference(id_col.index)
    ids = pd.concat([xdf.loc[id_col.index, xdf_cols], id_col, id_name], axis=1)
    xdf = pd.concat([xdf.loc[xdf_rows], ids], axis=0)  # pandas.errors.InvalidIndexError: Reindexing only valid with uniquely valued Index objects

    out = pd.concat([id_col, id_name], axis=1).drop_duplicates().set_index(id_col_name, drop=False)

    if id_name.str.startswith('internet').any():
        raise ValueError(f"Found 'internet' in id_name.  This is a reserved word and cannot be used in id_name")

    return xdf, out


# def update_es_lists(indf, id_col_name='', agg_dict=None, exclude_cols=None, time_cols=None, index='', keep_all=False):
#     """
#     Deduplicate entries in input DataFrame XDF, and create unique IDs from the values. Read from index
#     to see if these unique IDs were already entered and update them with the new entries.
#
#     This is different than a post_df_to_es in that columns name in param agg_dict's keys whose values
#     are 'set' will be aggregated into lists before updating OpenSearch.  This allows OpenSearch to
#     have a growing set of new values in these columns.
#
#     agg_dict is a standard {column: function} dictionary that would be passed to pd.DataFrame.groupby().agg(agg_dict)
#     except the function names as strings will be replaced with the actual function names if needed.
#
#     If keep_all is False (default) only columns that start with the following will be sent to OpenSearch:
#                ['R', 'event', 'user', 'object', 'bucket', 'host', 'api', 'data']
#     """
#     global esp
#     if esp is None:
#         esp = ESP(CFG)
#
#     if not isinstance(indf, pd.DataFrame) or not isinstance(agg_dict, dict) or not index or not id_col_name \
#             or id_col_name not in indf.columns:
#         print(f"[DEBUG] update_es_lists: Bad arguments")
#         return indf, pd.DataFrame()
#
#     xdf = indf.copy()
#
#     # Check for innapropriate columns in xdf and get rid of them unless keep_all = True
#     if not keep_all:
#         xdf = filter_columns_to_link_data(xdf, id_col_name=id_col_name)
#
#     id_api = xdf.get(id_col_name, pd.Series(index=xdf.index, name=id_col_name, dtype='O'))
#
#     # no_dupes has only unique values for querying OpenSearch
#     no_dupes = id_api.drop_duplicates().dropna()
#     no_dupes = pd.DataFrame(no_dupes.dropna(), columns=[id_col_name])
#     no_dupes = no_dupes.set_index(id_col_name, drop=False)
#
#     # Now query the DB to get the previously discovered records.
#     from_esp = esp.get_self_from_es(index, no_dupes)
#
#     time_cols = in_it(time_cols, from_esp)
#     if not from_esp.empty and time_cols:
#         for tcol in time_cols:
#             from_esp[tcol] = from_esp[tcol].apply(pd.to_datetime)
#
#     to_esp = []
#     aggs = in_it(agg_dict, xdf)
#     no_do = in_it(exclude_cols, xdf)
#     no_do.append(id_col_name)
#
#     # Aggregate values for each unique value of id_col_name
#     for col in xdf.columns.difference(no_do):
#         if not from_esp.empty and in_it(col, from_esp):
#             if aggs.get(col) in [set_x, "set", "set_x", "list"]:
#                 texp = from_esp.explode(col)
#                 texp = texp.loc[texp[col].notna()]
#                 before_len = texp.shape[0]
#                 xexp = xdf.explode(col)
#                 xexp = xexp.loc[xexp[col].notna()]
#                 texp = pd.concat([xexp[[id_col_name, col]], texp[[id_col_name, col]]], ignore_index=True).drop_duplicates()
#                 after_len = texp.shape[0]
#                 if before_len < after_len:  # ('user.from.host.id', 'user.id')
#                     notify_alert(xdf, thing_col=id_col_name, in_thing_col=col, category=id_col_name.capitalize().split('.')[0])
#             else:
#                 texp = pd.concat([xdf[[id_col_name, col]], from_esp[[id_col_name, col]]], ignore_index=True)
#         else:
#             texp = xdf[[id_col_name, col]]
#
#         if aggs.get(col) in [set_x, "set", "set_x", "list"]:
#             texp = texp.groupby(id_col_name, as_index=True, sort=False).agg({col: set_x})
#         elif aggs.get(col) in [max, "max"]:
#             texp = texp.groupby(id_col_name, as_index=True, sort=False).max()
#         else:
#             texp = texp.groupby(id_col_name, as_index=True, sort=False).last()
#
#         to_esp.append(texp)
#
#     # Each columns' result is in a separate series and to_esp holds them in a list.  So concatentate them all into a DF
#     to_esp = pd.concat(to_esp, axis=1)
#     to_esp[id_col_name] = to_esp.index
#     to_esp['R.ID'] = to_esp.index
#
#     # The first time we enter a value in a column that is supposed to be a list/array in OpenSearch
#     # that value must be in a list, otherwise OpenSearch will treat it as a single value forever more.
#     to_list = lambda L: [L] if isinstance(L, str) else L if L else nan
#     do_nada = lambda N: N
#     to_esp = to_esp.apply({c: to_list if aggs.get(c) == set_x else do_nada for c in to_esp.columns})
#     to_esp = to_esp.fillna(nan).sort_index(axis=1, ascending=True)
#
#     to_esp = delete_dangling_base_columns(to_esp, "'to_esp' in function update_es_lists")
#     ret = esp.post_df_to_es(index, to_esp)
#
#     new_apis = to_esp.index.difference(from_esp.index)
#     if len(new_apis) and DEBUG:
#         notify_alert(to_esp, thing_col=id_col_name, msg='endpoint', category='API')
#
#     return xdf, to_esp


def fill_in_host_ids(indf, base_col='', host_col='', include_cols=None, host_only=False, user_col=''):
    """
    Given a DataFrame with a column named prefix.host_col that contains unknown host names or ids, lookup
    and return the host names results from OpenSearch index = CFG.G["dbTables"]["serviceMapTable"]

    if prefix is a column name, then it will explode the column using explode_dict_column before looking
    for the host name.

    For an unknown series of hosts in indf[prefix.host_col] lookup the actual host in OpenSearch and
    return the results in columns prefixes by prefix.
    
    The columns returned will only be 'prefix.host' if the hostname was not found
    else the columns will be ['prefix.host', 'prefix.hid'].extend(prefix.[include_cols])

    If include_cols is set to the special value 'all', then all columns from the db will be returned.
    """
    
    xdf = indf.copy()

    base_col = base_col if isinstance(base_col, str) else ''
    host_col = host_col if isinstance(host_col, str) else ''
    return_cols = ["host_id", "host"]  # Default columns to return in the result from get_sid_from_name

    base_col_host = f"{base_col}.{host_col}" if base_col and host_col else base_col
    x_col_host = f"{base_col}.lookup"

    if not xdf.columns.intersection([base_col, base_col_host]).empty:
        xdf[x_col_host] = xdf.get(base_col_host).copy()
        if base_col_host and base_col_host in xdf.columns:
            hosts = get_sid_from_name(xdf.get(base_col_host), host_only=host_only)
            new_base = base_col
        elif host_col in xdf.columns:
            hosts = get_sid_from_name(xdf.get(host_col), host_only=host_only)
            new_base = host_col if not base_col else base_col
        else:
            temp = explode_dict_column(xdf, base_col)
            if base_col_host in temp.columns:
                hosts = get_sid_from_name(temp[base_col_host], host_only=host_only)
                new_base = base_col_host
            else:
                return xdf

        all_cols = False
        if include_cols is not None:
            if isinstance(include_cols, str):
                if include_cols == 'all':
                    all_cols = True
                else:
                    include_cols = [include_cols]
            elif not isinstance(include_cols, list) and isinstance(include_cols, Iterable):
                include_cols = [c for c in include_cols]
            elif not isinstance(include_cols, list):
                include_cols = []
            return_cols.extend(include_cols)

        hosts.name = ''
        hosts_exp = explode_dict_column(hosts)  # explode_dict_column will only return rows with dicts in them
        if not hosts_exp.empty:
            if not all_cols:
                hosts_exp.drop(columns=hosts_exp.columns.difference(return_cols), inplace=True)
            renamer = {c: f"{base_col}.{c}" for c in hosts_exp.columns}
            hosts = hosts_exp.rename(columns=renamer, errors='ignore')
        elif isinstance(hosts, pd.Series):
            hosts.name = new_base

        # If Only the short host name was asked for, return only the short host name.
        if host_only:
            return hosts

        # If we found the user in the database_col, then load the ID of the from host.
        if isinstance(hosts, (pd.DataFrame, pd.Series)) and not hosts.empty:
            if isinstance(hosts, pd.Series):
                hosts = hosts.to_frame()
            xdf = pd.concat([xdf[xdf.columns.difference(hosts.columns).difference([base_col_host])], hosts], axis=1)

        return xdf

    else:
        return indf


def lookup_user_host_id(name):
    """
    If a serviceName of a host is the same as the user_name coming from that host then
    this function will retrieve the host ID.
    :param name:
    :return:
    """
    global esp
    esp = ESP(CFG) if esp is None else esp

    # Define the search query
    query = {
        "query": {
            "bool": {
                "should": [
                    {"prefix": {"host.keyword": name}},
                    {"prefix": {"serviceName.keyword": name}}
                ],
                "minimum_should_match": 1
            }
        }
    }

    table = CFG.G['dbTables']['serviceMapTable']
    response = esp.esp_search(table, query)
    ids = [hit.get('_source', {}).get('R.ID') for hit in response.get('hits', {}).get('hits', [])]

    return ids[0] if len(ids) else None


# def delete_dangling_base_columns(df, name=''):
#     """
#     Clean-up Hack:  If there is a base column name, say 'user', and child keys of that base like 'user.id'
#     in the input DataFrame df, then drop the base column 'user' and keep the child columns 'user.id'.
#     This is very specific to the current code path.
#
#     Note this is not a good general solution since the function does not expand the 'user' column, nor update
#     the 'user' column with 'id'.  That means it could throw away columns that you might otherwise want to keep.
#     """
#
#     nosplit = set(df.columns.to_list())
#     splits = pd.DataFrame(df.columns.to_list(), index=df.columns, columns=['splits'])
#     splits = splits['splits'].str.split('.', expand=True)
#
#     bad_list = []
#     test = splits[0]
#     for n in range(1, splits.shape[1]):
#         has_n = splits[n].notna()
#         bad = nosplit.intersection(test[has_n].to_list())
#         bad_list.extend(list(bad))
#         test[has_n] = test[has_n] + '.' + splits.loc[has_n, n]
#
#     if bad_list:
#         print(f"Removing {f'from {name} ' if name else ''}previously expanded columns {bad_list}")
#         df.drop(columns=bad_list)
#
#     return df


def score_from_to_nmers(indf, from_nmers='from.data.nmers.total', time_col='data.first_seen.time',
                        to_nmers='to.data.nmers.total', score='link.score', scale=1000):
    """
    Relative nmers between from and to nodes is irrelevant.  What matters to scoring is the absolute
    number of nmers in the from node, and the time order in which the to nodes were seen.

    Create the score corresponding to how many relative nmers (and bytes) there are in the
    from and to nodes. The relationships will always have the node with the fewer Nmers point to
    the node with the greater Nmers.  If node A has 10 Nmers and 100% of those Nmers are found in
    node B that has 100 Nmers, then A -[:IN] -> B (using Neo4j syntax) and the strength of the
    relationship is 10 / 100 or .1 multiplied them by the 'scale' parameter.

    The Input DataFrame must have columns for from and to node nmers.  These column names can be specified
    in the parameters 'from_nmers' and 'to_nmer'.  The resulting score will be written to the column specified
    by the parameter 'score'.

    Defaults are:
        from_nmers  =   'from.data.nmers.total'
        to_nmers    =   'to.data.nmers.total'
        score       =   'link.score'
        base_score  =   1000
    """
    global esp
    if esp is None:
        esp = ESP(CFG)


    if not isinstance(indf, pd.DataFrame) or indf.empty or {from_nmers, to_nmers}.difference(indf.columns):
        return indf

    zf = indf[from_nmers].eq(0)
    zt = indf[to_nmers].eq(0)
    noz = ~zf & ~zt

    # if score not in indf.columns:
    #     indf[score] = scale
    #
    # indf.loc[noz, score] = (indf.loc[noz, score] * indf.loc[noz, to_nmers]) / (
    #                         indf.loc[noz, from_nmers] * scale)

    indf.loc[noz, score] = max(scale, 100) / indf.loc[noz, [from_nmers, to_nmers]].min(axis=1)

    indf.loc[zf & zt, score] = 1e8
    indf.loc[zf, score] = 1e10

    # When using the link.score to determine the dominant auth source for edges we should take into account when
    # the data node the edge points to was first_seen.  In case the links between an edge and two data nodes have
    # the same score based on NMERS we can break the tie based on which data node was seen first.

    indf['when_seen'] = indf.sort_values(time_col).groupby('from.data.id', as_index=False, sort=False).cumcount()
    indf['when_seen'] = indf['when_seen'].mul(.2).add(1).astype('float64')

    indf[score] = indf[score].mul(indf['when_seen'])

    score_stats = f"Data relationship score stats: max={indf.loc[noz, score].max():.2f} mean={indf.loc[noz, score].mean():.2f}" \
                  f" median={indf.loc[noz, score].median():.2f} min={indf.loc[noz, score].min():.2f}"

    print(score_stats)

    return indf


def match_in_index(ydf, id_col='', return_cols=None, index='', op='endswith', col_filters='index'):
    """
    Find all the rows/documents in the OpenSearch index 'index' that contain values from the specified
    column in the input dataframe or series.

    :param ydf: Input dataframe or Series, or list.
    :param id_col: If 'ydf' is a DataFrame, id_col specifies which column to use.  Otherwise ignored.
    :param return_cols: If a list, fnmatch patterns to select which columns from the lookup are returned.
                        If a dict, rename the columns in the dict keys to those in the values.
                        If None, returns all columns.
    :param index: Which OpenSearch index to lookup from.
    :param op: If not using fnmatch patterns, op specifies if the return_cols value should be 'in'
               the column name, be an exact match ('is'), 'endswith', or 'startswith'.  If 'filter',
               treat return_cols as a list of fnmatch patterns.  Default 'endswith'.
    :param col_filters: If equal to 'index' then only return rows if the _id column in the index
               matches the values in ydf.  A list of values (fnmatch patterns) can be specified which
               will force an advanced search to see if any of the matching columns contain *ANY* of
               the values in ydf.
    :return: dataframe with return_cols and rows that match the values in ydf.
    """
    global esp
    if esp is None:
        esp = ESP(CFG)

    # --------------------------------------------------------------------------

    def check_keyword_field(properties, field):
        parts = field.split('.')
        if parts[0] not in properties:
            return False
        if len(parts) == 1:
            field_type = properties[parts[0]].get('type')
            if field_type == 'keyword':
                return True
            if 'fields' in properties[parts[0]] and 'keyword' in properties[parts[0]]['fields']:
                return True
            return False
        else:
            if 'properties' in properties[parts[0]]:
                return check_keyword_field(properties[parts[0]]['properties'], '.'.join(parts[1:]))
            return False

    def can_use_keyword_suffix(index_name, field_names):
        # Get the mappings for the index
        mapping = esp.esp.es.indices.get_mapping(index=index_name)
        properties = mapping[index_name]['mappings']['properties']

        # Check each field
        results = {}
        for field in field_names:
            results[field] = check_keyword_field(properties, field)

        return results
    # --------------------------------------------------------------------------

    if isinstance(ydf, pd.DataFrame) and in_it(id_col, ydf):
        qry_df = pd.Index(ydf[id_col].drop_duplicates().dropna())
    elif isinstance(ydf, pd.Series):
        qry_df = pd.Index(ydf.drop_duplicates().dropna())
    elif isinstance(ydf, (set, list)):
        qry_df = pd.Index(list(ydf)).drop_duplicates().dropna()
    else:
        return pd.DataFrame()

    if col_filters != 'index':
        if col_filters:
            fields = esp.get_matching_fields(index, col_filters if isinstance(col_filters, list) else [col_filters])
        else:
            fields = esp.get_matching_fields(index, ["*"])

        if not fields:
            return pd.DataFrame()

        kfields = can_use_keyword_suffix(index, fields)
        warn_fields = [f for f, v in kfields.items() if not v]
        if warn_fields:
            print(f"[WARNING] match_in_index: Cannot use keyword suffix for fields: {warn_fields}")

        kfields = [f for f, v in kfields.items() if v]
        should_clauses = []
        for field in kfields:
            should_clause = {
                "bool": {
                    "should": [
                        {
                            "terms": {f"{field}.keyword": qry_df.to_list()}
                        }
                    ]
                }
            }
            should_clauses.append(should_clause)

        if not should_clauses:
            print(f"[DEBUG] match_in_index: No keyword fields found in index matching {col_filters}")
            return pd.DataFrame()

        query = {"query": {"bool": {"should": should_clauses}}}
        # print("[DEBUG] match_in_index: Constructed query is: ", query)
        qry_out = esp.esp_search(index, query, return_type='dataframe', size=4*qry_df.shape[0])
    else:
        qry_out = esp.get_self_from_es(index, qry_df)

    # If I was better at writing OpenSearch queries I probably could avoid all this code...
    if not qry_out.empty:

        qry_df = qry_out

        if return_cols is not None and isinstance(return_cols, str):
            if return_cols in ['all', '*', '']:
                return_cols = qry_df.columns.to_list()
                op = 'is'
            elif ',' in return_cols:
                return_cols = [c.strip for c in return_cols.split(',')]
            else:
                return_cols = [return_cols]
        elif return_cols is None or not isinstance(return_cols, Iterable):
            return_cols = ['id', 'name']

        if op not in ['in', 'startswith', 'endswith', 'is', 'filter']:
            op = 'is'

        if isinstance(return_cols, list):
            if op == 'in':
                clm = [c for p in return_cols for c in qry_df.columns if p in c]
            elif op == 'startswith':
                clm = [c for p in return_cols for c in qry_df.columns if c.startswith(p)]
            elif op == 'endswith':
                clm = [c for p in return_cols for c in qry_df.columns if c.endswith(p)]
            elif op == 'filter':
                rcs = fnfilter_list(qry_df.columns, return_cols)
                return_cols = list(set(rcs))
                clm = [c for p in return_cols for c in qry_df.columns if p in c]
            else:
                clm = in_it(return_cols, qry_df)
            if clm:
                clm = list(set(clm))
                return qry_df[clm].sort_index(axis=1)
        elif isinstance(return_cols, dict) and op != 'filter':
            if op == 'in':
                clm = {c: v for p, v in return_cols.items() for c in qry_df.columns if p in c}
            elif op == 'startswith':
                clm = {c: v for p, v in return_cols.items() for c in qry_df.columns if c.startswith(p)}
            elif op == 'endswith':
                clm = {c: v for p, v in return_cols.items() for c in qry_df.columns if c.endswith(p)}
            else:
                clm = in_it(return_cols, qry_df)

            if clm:
                return qry_df[clm.keys()].rename(columns=clm).sort_index(axis=1)
        else:
            raise ValueError("Cannot use op='filter' with rename columns (i.e, when return_cols is a dict)")

    # print(f"[DEBUG] match_in_index: Query on {qry_df.shape} rows/cols returned {qry_out.shape} rows/cols")
    return pd.DataFrame()


def bin_score(dmdf, incol='', outcol='bins', bin_names: list=None, df_out=True):
    if bin_names is None or not isinstance(bin_names, Iterable):
        bin_names = ['High', 'Med', 'Low']

    num_bins = len(bin_names) - 1
    out_df = pd.DataFrame()

    if isinstance(dmdf, pd.DataFrame) and incol in dmdf.columns:
        qry_series = dmdf[incol].copy().drop_duplicates().dropna().sort_values(ascending=False)
        out_df = dmdf.copy()
    elif isinstance(dmdf, pd.Series):
        qry_series = dmdf.copy().drop_duplicates().dropna().sort_values(ascending=False)
        if not incol:
            incol = dmdf.name
        out_df = pd.DataFrame(dmdf.copy(), columns=[incol])
    else:
        return out_df

    try:
        qry_series = qry_series.astype("float64")
    except Exception as err:
        print(f"[WARNING] Exception bin_score: {err} ")
        return out_df

    foo, bins = pd.qcut(qry_series, q=num_bins, retbins=True, duplicates='drop')

    # Start by filling output with the last bin name in the list
    out_df[outcol] = bin_names[-1]

    n = num_bins -1
    for b in range(0, len(bins)):
        in_bin = out_df[incol].astype(int).gt(bins[b])
        out_df.loc[in_bin, outcol] = bin_names[n]
        # print(f"n={n}:{bin_names[n]}  b={b}:{bins[b]}")
        n = (n-1) if n > 0 else 0

    if df_out:
        return out_df
    else:
        lv = {k: 0 for k in bin_names}
        lv.update(out_df[outcol].value_counts().to_dict())
        return lv


def fix_dangles(dmdf):
    """
        DETECT AND CONNECT 'DANGLING ENDS'
        Dangling ends are nodes that
          1. appear only in the 'from_name' column or only in the 'to_name' column
          2. Are not at the start or end of the time series of events
          3. Are allowed to connect to each other ?
    """

    # TODO: Unknown or unseen mechanisms that move data must be included in alerts

    dmdf['sequence'] = dmdf['sequence'].astype('int64')
    x = dmdf[['edges', 'event.time_min', 'event.time_max', 'event.method.type', 'from_type', 'to_type', 'from_name', 'to_name']]
    x = x.loc[~x['event.method.type'].isin(['get_meta', 'put_meta'])].explode('edges').reset_index()

    with open('dmdf.csv', 'w') as f:
        f.write(x.to_csv(index=False))

    fun = dmdf['from_name'].unique()
    tun = dmdf['to_name'].unique()
    f_dangle = list(set(fun).difference(tun))
    t_dangle = list(set(tun).difference(fun))

    from_orphans = dmdf.loc[dmdf['from_name'].isin(f_dangle)]
    to_orphans = dmdf.loc[dmdf['to_name'].isin(t_dangle)]

    fun = from_orphans.groupby(['from_name', 'Source'], as_index=False, sort=False).last()
    tun = to_orphans.groupby(['to_name', 'Source'], as_index=False, sort=False).last()

    fun = fun.loc[fun['sequence'].ne(dmdf['sequence'].min())]
    tun = tun.loc[tun['sequence'].ne(dmdf['sequence'].max())]

    time_col = 'sequence'
    mean_cols = in_it(['event.time', 'event.time_min', 'event.time_max', 'sequence'], dmdf)
    if "event.time_min" in mean_cols:
        time_col = 'event.time_min'
    elif "event.time" in mean_cols:
        time_col = 'event.time'
    elif "event.time_max" in mean_cols:
        time_col = 'event.time_max'

    if not fun.empty:
        fun = fun.drop(columns=['to_type', 'to_name', 'to_parent']).rename(columns={'from_type': 'to_type', 'from_name': 'to_name', 'from_parent': 'to_parent'})
        tun = tun.drop(columns=['from_type', 'from_name', 'from_parent']).rename(columns={'to_type': 'from_type', 'to_name': 'from_name', 'to_parent': 'from_parent'})

        # Connect dangling froms and dangling tos with no intermediate node
        # sequnce tun < sequence fun and source tun == source fun
        # Should be checking if sequence number of the new from node is less than the sequence number of the new to node

        fun = pd.concat([tun, fun]).sort_values(time_col).explode('edges')

        fromna = fun['from_name'].isna()
        dangles = fun.loc[fromna].groupby('edges', as_index=False, sort=False).first()
        tun = fun.loc[fromna].groupby('edges', as_index=False, sort=False).mean(numeric_only=False)
        dangles[mean_cols] = tun[mean_cols].astype(dmdf[mean_cols].dtypes)

        loc1 = dangles['object.nmers'].ne(0)
        dangles.loc[loc1, 'percent'] = 100 * dangles.loc[loc1, 'edge.nmers'] / dangles.loc[loc1, 'object.nmers']

        dangles.dropna(subset=['to_name'], inplace=True)
        loc2 = dangles['from_name'].isna() & dangles['event.method.type'].eq('put')

        # Handle unseen movement of data from one object to another.
        loc3 = dangles['from_name'].isna() & dangles['event.method.type'].ne('put') & dangles["Source"].ne(dangles["to_name"])
        dangles.loc[loc3, 'from_name'] = dangles.loc[loc3, 'Source']

        dangles.loc[loc3 & dangles["Source"].str.contains(CFG.token), 'from_type'] = 'Object'
        dangles.loc[loc3 & dangles["Source"].str.contains('USER'), 'from_type'] = 'Service'
        dangles.loc[loc3, 'event.method.type'] = 'put'

        dangles = dangles.loc[loc2 | loc3]

        if not dangles.empty:
            # Create and insert an Unknown service that moves data from the source to the dangling node
            # Unknown --gets data-> User/Service
            # Name the unknown nodes from the event.id which should alway starts with a 4 character uppercase string.
            # Being liberal with the regex here to allow for future changes in the event.id format.
            ev_id = dangles["event.id"].apply(lambda x: x[0] if isinstance(x, list) else x)
            dangles["unkwn_id"] = ev_id.str.replace(r'^[A-Z0-9]{3,5}-', 'UNKN-', regex=True, n=1)
            dangles["HostUnknown"] = ev_id.str.replace(r'^[A-Z0-9]{3,5}-', 'HUNK-', regex=True, n=1)

            k_get_o = dangles.copy()
            if not k_get_o.empty:
                # k_get_o["from_type"] = "Object"
                k_get_o["to_type"] = "Unknown"

                k_get_o["from_name"] = k_get_o["Source"]
                k_get_o["to_name"] = k_get_o["unkwn_id"]

                lobj = k_get_o["Source"].eq("Object")
                k_get_o.loc[lobj, "from_parent"] = k_get_o.loc[lobj, "Source"].transform(lambda C: parse_cori(C)[1])
                k_get_o.loc[~lobj, "from_parent"] = k_get_o.loc[~lobj, "Host_U"]

                k_get_o["to_parent"] = k_get_o["HostUnknown"]
                k_get_o["R.ID"] = k_get_o["R.ID"] + "KGO"
                # k_get_o["edge.nmers"] = k_get_o["object.nmers"]

            s_get_k = dangles.copy()
            if not s_get_k.empty:
                s_get_k["to_type"] = s_get_k["to_type"]
                s_get_k["from_type"] = "Unknown"

                s_get_k["from_name"] = s_get_k["unkwn_id"]
                s_get_k["to_name"] = s_get_k["to_name"]

                s_get_k["from_parent"] = s_get_k["HostUnknown"]
                s_get_k["to_parent"] = s_get_k["to_parent"]

                s_get_k["R.ID"] = s_get_k["R.ID"] + "SGK"
                s_get_k[time_col] = s_get_k[time_col] + timedelta(microseconds=.5)

            dangles = pd.concat([k_get_o, s_get_k], ignore_index=True)
            dangles['event.method.name'] = 'Unknown'
            dangles['event.method.type'] = 'unknown'
            dangles = dangles.sort_values(time_col)

            # Put the common edges back into lists
            set_cols = ["edges", "from_name", "to_name"]
            first_cols = dangles.columns.difference(["edges"])
            e = dangles[set_cols].groupby(["from_name", "to_name"], as_index=False, sort=False).agg({"edges": set_x})
            o = dangles[first_cols].groupby(["from_name", "to_name"], as_index=False, sort=False).first()
            dangles = pd.concat([o, e["edges"]], axis=1)

            dangles.drop(columns=["unkwn_id"], inplace=True)
            dangles = dangles.set_index('R.ID', drop=False)
            dangles.index.name = 'index'

            assert dmdf.index.intersection(dangles.index).shape[0] == 0, "Dangling edges index overlaps with dmdf index"

            dmdf = pd.concat([dmdf, dangles], ignore_index=True).sort_values(time_col)
            dmdf = dmdf.set_index('R.ID', drop=False)
            dmdf.index.name = 'index'

    return dmdf


def fix_object_map_tika_problem(omap):
    """
    HACK: In the abscence of doing the fix me below, there can be two, possibly 3, CQFs with the same sha256 and
    primary nmer count but different secondary nmer counts. This happens when extraction fails when indexing
    the object.  So the code below replaces the sec-nmers in data.ids where extraction failed and picks the
    most useful version of the CQF for a given data.sha256.
    """

    # FIXME: Create separate indices for an object's main CQF, extracted text CQF, and extracted keys CQF.

    def _fix_mime(x):
        if x.shape[0] > 1:
            y = x.unique().tolist()
            z = fnfilter_list(y, CFG.G["alwaysCheckTypes"])
            y = list(set(y).difference(z))
            if len(y):
                return y[0]
            return z[0]
        return x

    maxcols = in_it(['event.time', 'event.latency', 'data.nmers.primary', 'data.nmers.total',
                     'data.index.de_dupe', 'data.sha256','data.bytes', 'data.content.length.key_val',
                     'data.content.length.text', 'data.index.time.scanned'], omap)

    lstcols = in_it(['data.sha256', 'data.content.key_vals', 'data.content.text'], omap)

    m = omap[maxcols].groupby('data.sha256', sort=False).max()
    l = omap[lstcols].groupby('data.sha256', sort=False).last()
    t = omap[['data.sha256', 'data.mime_type']].groupby('data.sha256', sort=False).agg(_fix_mime)
    fixed = pd.concat([m, l, t], axis=1)
    if omap.shape[0] - fixed.shape[0] > 0:
        print(f"[DEBUG] Found {omap.shape[0] - fixed.shape[0]} rows in omap with Tika fail/no-fail problem")
    kcols = omap.columns.difference(fixed.columns)
    omap = omap[kcols].merge(fixed, left_on='data.sha256', right_index=True, how='left')
    
    omap['data.id'] = (omap['data.sha256'] + 
                       '-' + omap['data.nmers.primary'].astype('string') +
                       '-' + omap['data.nmers.total'].astype('string'))

    omap['data.index.name'] = (CFG.rem_cori_prefix() + '/' + omap['data.id'] + CFG.G['filenameSuffixes']['index'])

    return omap


def find_significant_api_levels():
    # This section of code handles the collapsing of the name hierarchy for APIs by finding the most
    #    variable path component and dropping it and all path components that follow it.
    global esp
    if esp is None:
        esp = ESP(CFG)

    table = CFG.G["dbTables"].get("apiMapTable", "csi_api_map")
    query = {"size": 5000, "query": {"match_all": {}}}
    name_df = esp.esp_search(table, query, return_type='dataframe')

    apilevels = 6
    columns = ['api.host.name']
    columns.extend([c for c in name_df.columns if c.startswith('api.path.')])

    if not name_df.empty:
        gbcols = []
        # columns = columns.to_list()
        name_df = name_df[columns]

        for n in range(0, len(columns) - 1):
            gbcols.append(columns[n])
            uniques = name_df.groupby(gbcols, sort=False).nunique()
            counts = name_df.groupby(gbcols, sort=False).count()
            significant = counts.gt(5)
            uniques[~significant] = 0
            uniques[significant] = uniques[significant] / counts[significant]
            uniques = uniques.ge(.65)

            for m in range(n, len(columns) - 1):
                drop_next = uniques.loc[uniques[columns[m + 1]]].index.get_level_values(n).to_list()
                name_df.loc[name_df[columns[n]].isin(drop_next), columns[m + 1]] = None

        # For the short API name treat CreateMultipartUpload, UploadPart, and CompleteMultipartUpload as equivalent
        pattern = re.compile(r'^.*upload.*$', re.IGNORECASE)
        name_df['api.path.0'] = name_df['api.path.0'].str.replace(pattern, 'UPLOAD')

        # For S3 operations only keep the method and bucket in the short name.
        s3loc = name_df['api.host.name'].astype('string', errors='ignore').str.startswith('s3')
        name_df.loc[s3loc, [f'api.path.{n}' for n in range(2, apilevels)]] = None

        # name_df now has the path elements in columns with any high-variance path elements removed
        # Next put an absolute limit on how many levels in the api path hierarchy is apilevels is specified.
        path_max = max([int(n.rsplit('.', 1)[-1]) for n in name_df.columns if n.startswith('api.path')])
        if apilevels > 1:
            apilevels = min(apilevels, path_max + 1)
        else:
            apilevels = path_max + 1
        path_cols = [f'api.path.{n}' for n in range(0, apilevels)]
        api_name = pd.Series(name_df[path_cols].fillna('').T.to_dict(orient='list'), name='api.short_name')
        api_name = api_name.str.join('/').transform(lambda x: x[:x.find('//')] if x.find('//') > 0 else x)
        api_name = api_name.str.strip('/').to_frame()
        api_name['api.host.name'] = name_df['api.host.name']

        xdf, ids = generate_id_name_and_key(api_name, id_prefix='SAPI-', id_col_name='api.short_id', id_name_name='X')

        ret = esp.post_df_to_es(table, xdf.drop(columns=['X', 'api.host.name']), op="update")

        return ret

def deadbad(df_with_dead_objects):
    deadbad = df_with_dead_objects["object.id"].str.encode('utf-8')
    deadbad = deadbad.transform(lambda H: sha256(H).hexdigest()).str.slice(0, 54)
    df_with_dead_objects["data.sha256"] = "deadbad000" + deadbad
    df_with_dead_objects["data.id"] = "deadbad000" + deadbad + "-1-1"
    df_with_dead_objects["object.flag.deleted"] = True
    return df_with_dead_objects


def _join_obj_version(obj_in, ver):
    if isinstance(obj_in, pd.Series) and isinstance(ver, pd.Series):
        # Make sure that the indices of both series are identical.
        if obj_in.index.symmetric_difference(ver.index).empty:
            obj = obj_in.copy()
            lnb = ver.notna() & ver.ne('')
            obj.loc[lnb] = obj.loc[lnb].str.rsplit(CFG.G["objVersSeparator"], 1, expand=True).get(0)
            return obj.loc[lnb] + CFG.G["objVersSeparator"] + ver.loc[lnb]
        return obj_in
    if isinstance(obj_in, str) and isinstance(ver, str):
        if obj_in.count(CFG.G["objVersSeparator"]):
            obj_in = obj_in.rsplit(CFG.G["objVersSeparator"], 1)[0]
        return f'{obj_in}{CFG.G["objVersSeparator"]}{ver}'
    else:
        return obj_in


def fix_event_objects_without_versions(events):
    """
    As a consequence of CloudTrail logs delivering events with unversioned objects at times, there may be
    versioned and unversioned objects in the events.  Sometimes we get unversioned objects with sha256
    values as a result of indexing them only later to find the versioned version of the said object.  We
    corrected for this in the Object Scan Table in OpenSearch, but cannot easily do it globally across all
    events.  So, this function fixes the versions based on the object.ids merged from the Object Scan Table
    into events (the 'api_content' column) and fixes the object.id, object.version, and data.sha256 values
    in the events df.

    :param events: DataFrame with columns ['api_content', 'object.id', 'data.sha256', 'object.version']
    :return:
    """
    if not validate_df(events, "(api_content | object.id) & data.sha256"):
        return events
    # f373cc7b6640c1f4eb781c5a010f1fb5b5cab006e03810fe202b6bf3b1d92175
    # If api_content has a version and object.id does not, then make object.id equal to api_content
    if 'api_content' in events.columns and 'object.id' not in events.columns:
        boof = events.explode('api_content')
        boof['object.id'] = boof['api_content']
    else:
        boof = events.copy()

    if 'object.version' not in events.columns:
        boof['object.version'] = boof['object.id'].str.split(CFG.G["objVersSeparator"], expand=True).get(1)

    loca = (boof['object.id'].notna() &
            ~boof['object.id'].astype('string', errors='ignore').str.startswith(CFG.sspfx))

    # Fix when Objects come in without versions, but have the same SHA-256 as the same object with a version.

    goof = boof.loc[loca]
    foog = pd.DataFrame(goof['object.id'].apply(parse_cori).to_list(), columns=['h', 'b', 'm', 'o', 'v'], index=goof.index)
    goof['object.base'] = foog['h'] + CFG.token + foog['b'] + '/' + foog['o']
    del foog

    # Gather the versions for objects with the same base and sha256.  There should be only one version of an
    # object that has the same SHA-256.
    ob_ver_check = goof.groupby(['data.sha256', 'object.base'],
                                as_index=False, sort=False).agg({'object.version': set_x})

    # Sometimes we find that there are multiple versions of the same object with the same SHA-256.  It's not
    # clear how this can happen within s3. More likely is S3_Scanner.track_versions.cloudtrail_s3_version_tracker
    # is doing the wrong thing.
    lerr = ob_ver_check['object.version'].apply(len).gt(1)
    v_problems = ob_ver_check.loc[lerr].copy()
    if lerr.any():
        print(f"[DEBUG] {v_problems.shape[0]} Objects have multiple versions pointing to the same SHA-256." )

    lnov = ob_ver_check['object.version'].apply(len).eq(0)
    ob_ver_check = ob_ver_check.loc[~lerr & ~lnov].explode('object.version')
    # Set up a merge key to merge the corrected versions back into goof
    ob_ver_check['MK'] = ob_ver_check['data.sha256'] + ob_ver_check['object.base']
    goof['MK'] = goof['data.sha256'] + goof['object.base']
    gcols = goof.columns.difference(['object.version'])
    goof = goof[gcols].merge(ob_ver_check[['MK', 'object.version']], on='MK', how='left')

    lfix = ~goof['object.version'].isna()
    new_oids = goof.loc[lfix, "object.base"] + CFG.G["objVersSeparator"] + goof.loc[lfix, 'object.version']
    goof.loc[lfix, "object.id"] = new_oids
    goof.drop(columns=['MK'], inplace=True)
    goof.set_index('R.ID', drop=False, inplace=True)

    boof = pd.concat([boof.loc[~loca], goof]).drop(columns=['object.base'])
    return boof

    # boof.loc[loca, 'object.id'] = boof.loc[loca, 'api_content']
    # boof.loc[loca, 'object.name'] = boof.loc[loca, 'object.id'].str.split('/',1, expand=True).get(1)
    # boof.loc[loca, 'object.name'] = boof.loc[loca, 'object.name'].str.split(CFG.G['objVersSeparator'], expand=True).get(0)
    #
    # obj_no_ver = boof['object.name'].notna() & \
    #              boof['object.version'].fillna('').astype('string', errors='ignore').str.len().le(4)
    #
    # if obj_no_ver.any():
    #     cols = ['object.id', 'object.name', 'bucket.name', 'event.time', 'R.ID']
    #     versions = boof.loc[obj_no_ver, cols].apply(search_nearest_version, allow_over_seconds=1, axis=1)
    #     versions = pd.DataFrame(versions.to_list(), index=boof.loc[obj_no_ver].index)
    #     boof = update_then_concat(boof,versions)
    #     loco = obj_no_ver & ~boof['object.version'].isna()
    #     new_oids = _join_obj_version(boof.loc[loco, "object.id"], boof.loc[loco, 'object.version'])
    #     boof.loc[loco, "object.id"] = new_oids
    #     loca = obj_no_ver & boof['object.version'].isna()
    #     boof = boof.loc[~loca]
    #
    # # Across the df, gather all the api_content values that have the same sha256, then if an unversioned
    # # object.id has the same sha256 as a versioned object.id, we can be pretty sure it's the same object so
    # # back fill the version in object.version, and make sure api_content and object.id have the version.
    # loco = boof['data.sha256'].notna()
    # foob = boof.loc[loco].groupby('data.sha256').agg({'api_content': set_x})
    # foob = foob.explode('api_content').reset_index(drop=False)
    # notsha = boof.columns.difference(['data.sha256'])
    # boof = boof[notsha].merge(foob, on='api_content', how='left').set_index('R.ID',  drop=False)
    # boof.index.name = 'index'
    #
    # boof.loc[loca, 'object.base'] = boof.loc[loca, 'object.id'].str.split(CFG.G['objVersSeparator'], expand=True).get(0)
    # beef = boof.loc[loca].groupby(['object.base', 'data.sha256'], as_index=False).agg(
    #     {'object.version': top_x, 'R.ID': set_x}).explode('R.ID')
    #
    # lver = beef['object.version'].notna() & beef['object.version'].ne('')
    # beef.loc[~lver, 'object.id'] = beef.loc[~lver, 'object.base'] + CFG.G["objVersSeparator"] + beef.loc[~lver, 'object.version']
    #
    # beef.set_index('R.ID', inplace=True)
    # beef.index.name = 'index'
    # beef = check_df_indices(beef)
    # boof.loc[beef.index, ['object.id', 'object.version']] = beef[['object.id', 'object.version']]
    # loce = boof[['data.sha256', 'object.id']].notna().all(1)
    # boof.loc[loce, 'api_content'] = boof.loc[loce, 'object.id']
    # ob_ver = boof.loc[loca, 'object.id'].str.split(CFG.G['objVersSeparator'], expand=True).get(1)
    # boof.loc[loca, 'object.version'] = ob_ver
    #
    # # Lastly, handle the case where the data.sha256 for a versioned object is NaN.  We need to make it a
    # # deadbad sha256.
    #
    # loci = boof[['object.version', 'object.id']].notna().all(1) & boof['data.sha256'].isna()
    # boof.loc[loci] = deadbad(boof.loc[loci])
    # boof.drop(columns=['object.base'], inplace=True)
    #
    # return boof


def update_es_with_fixed_objects(objects_df):
    """
    After finding and fixing objects without versions using fix_event_objects_without_versions(events),
    we want to merge the properties of the fixed objects and delete the objects without versions
    that we fixed.  This function is not part of fix_event_objects_without_versions because this step
    is only useful when run on the objects_df, not the events dataframe.

    :param objects_df:
    :return:
    """
    global esp
    esp = ESP(CFG) if esp is None else esp

    # Merge the rows in objects that were fixed, picking the earliest last_mod and event times
    # but the latest intersector build and last indexed time.
    lcori = ~objects_df['object.use_hash'].astype(bool)
    min_cols = in_it(['object.time.last_modified', 'event.time', 'object.id'], objects_df)
    max_cols = objects_df.columns.difference(min_cols).difference(['R.ID']).union(['object.id'])
    lst_cols = in_it(['bucket.acl', 'bucket.auth', 'object.acl', 'object.auth.claimed',
                      'object.auth.determined', 'object.auth.enforced', 'object.id'], objects_df)
    objs_min = objects_df.loc[lcori, min_cols].groupby('object.id', as_index=False, sort=False).min()
    objs_max = objects_df.loc[lcori, max_cols].groupby('object.id', as_index=False, sort=False).max()
    objs_lst = objects_df.loc[lcori, lst_cols].groupby('object.id', as_index=False, sort=False).last()
    fixed_coris = pd.concat([objs_max, objs_min.drop(columns=['object.id']),
                             objs_lst.drop(columns=['object.id'])], axis=1)
    fixed_coris["R.ID"] = fixed_coris["object.id"]
    fixed_coris.set_index("R.ID", drop=False, inplace=True)
    fixed_coris.index.name = objects_df.index.name

    # # Now delete the rows in OpenSearch that had objects with no versions, but now we have found,
    # # so we don't have to keep processing them in future cycles.
    # objs_to_drop = lcori & objects_df['R.ID'].ne(objects_df['object.id'])
    # esp.delete_df_items_from_es(CFG.G["dbTables"]["objScanTable"], objects_df.loc[objs_to_drop])
    #
    # # And update the items that we have fixed with the new times, etc.
    # esp.post_df_to_es(CFG.G["dbTables"]["objScanTable"], fixed_coris, op='update')

    # Finally drop the objects that had no versions by concatenating the non-cori objects and the fixed
    # cori object dataframes together.
    objects_df = pd.concat([objects_df.loc[~lcori], fixed_coris])

    return objects_df


def propagate_version_within_time_limit(df, smax=1):
    """
    Fill the object.version to objects of the same name and same size, if they occured at roughly the same time.
    If an object within the time window is marked deleted, then it's object.bytes will be ignored.

    Group the input DataFrame by object.name and object.bytes. For each group, find the first non-null
    object.version and its corresponding event.time. Assign this object.version to other rows in the group,
    if their event.time falls within the smax limit from the event.time of the first non-null object.version.

    :param df:
    :param smax: seconds around the time of an event with an object version to consider valid.
    :return:
    """
    # This function is applied to each group
    def _fill_version_within_time_limit(group, version_time=None, version_value=None):
        if version_time is None or not version_value:
            # Find the first non-null object.version and its event.time
            loco = group['object.version'].ne('') & group['object.version'].notna()
            first_non_null_version = group.loc[loco, 'object.version'].head(1)
            if not first_non_null_version.empty:
                version_time = group.loc[first_non_null_version.index, 'event.time'].iloc[0]
                version_value = first_non_null_version.iloc[0]
            else:
                return group  # if no non-null version, return unchanged group
        # Find rows where event.time is within smax of version_time
        mask = (group['event.time'] >= (version_time - pd.Timedelta(seconds=smax))) & \
               (group['event.time'] <= (version_time + pd.Timedelta(seconds=smax)))
        # Assign the version value to those rows
        group.loc[mask, 'object.version'] = version_value if version_value else None
        return group
    # ===============================================================================================

    # Fill empty string as NaN
    df.loc[df['object.version'].eq(''), 'object.version'] = pd.NA

    # Handle rows with object.flag.deleted set to True
    deleted_rows = df[df['object.flag.deleted']]
    for _, row in deleted_rows.iterrows():
        event_time = row['event.time']
        object_name = row['object.name']
        affected_rows_mask = (
                (df['object.name'] == object_name) &
                (df['event.time'] >= (event_time - pd.Timedelta(seconds=smax))) &
                (df['event.time'] <= (event_time + pd.Timedelta(seconds=smax)))
        )
        version_time = row['event.time']
        version_value = row['object.version']
        df.loc[affected_rows_mask, 'object.version'] = version_value if not pd.isna(version_value) else df.loc[
            affected_rows_mask, 'object.version']

    # Group by object.name and object.size (excluding the deleted ones) and apply the function
    df = df.groupby(['object.name', 'object.bytes'], group_keys=False).apply(_fill_version_within_time_limit)
    df = df.reset_index(drop=True).fillna({'object.version': ''})
    return df


def search_nearest_version(clnt_or_series, bkt=None, obj=None, access_time=None, r_id=None, sha_256=None, allow_over_seconds=0):
    """
    THIS DOES NOT WORK FOR ANY OBJECT THAT GET UPDATED MORE THAN ONCE PER SECOND.

    Check if the object has a VersionId associated with it.  If so, return the obj argument unchanged. Otherwise,
    this code will iterate through the versions and find the version whose LastModified timestamp is closest to
    the provided access time.  Apparently there is no ETAG provided in CloudTrail log files...

    Assumptions:
    - The access_time, if it comes from the event.time, has a precision equivalent to the LastModified time.
      This is not always the case for CloudTrail S3 Data Event logging.

    - The version with a timestamp closest to, but not later than, the access time is the most likely
      version that was accessed.

    :param allow_over_seconds: Seconds, if greater than 0, that an object's last_modified_time may be OVER access
            time and still be considered valid.
    :param clnt_or_series: Storage host client (like boto3.client('s3')) or an input series with all variables.
    :param bkt: The name of the bucket the object is in.
    :param obj: The name of the object, potentially with the VersionId concatenated to it.
    :param access_time: The event.time of the record
    :param r_id: The 'R.ID' of the record
    :return: The name of the object with the VersionId concatenated to it.
    """
    global esp
    esp = ESP(CFG) if esp is None else esp

    def _cache_versions(client, bucket_name, object_key, length=-1):
        """
        The cache_versions function fetches and caches object versions and delete markers.
        :param client: Boto3('s3') client for the customer object source corresponding to bucket_name
        :param bucket_name: Name of the bucket where the object resides
        :param object_key: Key or name of the object
        :param length: Size of object to store in cache if size is not returned.
        :return: Dataframe of objects and their versions that match
        """

        response = client.list_object_versions(Bucket=bucket_name, Prefix=object_key)
        object_versions = pd.DataFrame(columns=['Bucket', 'ObjectKey', 'VersionId', 'LastModified', 'IsDeleteMarker'])

        # Cache regular versions
        for version in response.get('Versions', []):
            object_versions = object_versions.append({
                'Bucket': bucket_name,
                'ObjectKey': object_key,
                'VersionId': version.get('VersionId') if version.get('VersionId', '') != 'null' else None,
                'LastModified': version.get('LastModified', pd.NaT),
                'Size': version.get('Size', length),
                'ETag': version.get('ETag'),
                'IsDeleteMarker': False
            }, ignore_index=True)

        # Cache delete markers
        for marker in response.get('DeleteMarkers', []):
            object_versions = object_versions.append({
                'Bucket': bucket_name,
                'ObjectKey': object_key,
                'VersionId': marker.get('VersionId') if marker.get('VersionId', '') != 'null' else None,
                'LastModified': marker.get('LastModified', pd.NaT),
                'Size': marker.get('Size', length),
                'ETag': marker.get('ETag'),
                'IsDeleteMarker': True
            }, ignore_index=True)

        key_cols = ['Bucket', 'ObjectKey', 'VersionId', 'LastModified']
        object_versions, _ = generate_id_name_and_key(object_versions, must_have_id_cols=key_cols,
                                                      id_prefix='VERS-', id_col_name='R.ID')
        object_versions = object_versions.set_index('R.ID', drop=False)

        table = CFG.G["dbTables"]["objVersionTable"]
        object_versions = object_versions.loc[object_versions['R.ID'].notna()]
        if not object_versions.empty:
            num = esp.post_df_to_es(table, object_versions)

        return object_versions

    # ==============================================================================================

    if isinstance(clnt_or_series, pd.Series):
        needed_cols = 'object.id & bucket.name & object.name & (event.time | object.time.last_modified)'
        if not validate_df(clnt_or_series, needed_cols, series_ok=True):
            return '', None, None       # version = '' and deleted = None

        try:
            clnt =  get_object_store_client(clnt_or_series['object.id'])
        except:
            clnt = None
        bkt = clnt_or_series['bucket.name']
        obj = clnt_or_series['object.name']
        r_id = clnt_or_series.get('R.ID', None)
        size = clnt_or_series.get('object.bytes', -1)
        access_time = first_valid(clnt_or_series.get('event.time'),
                                  clnt_or_series.get('object.time.last_modified'), oftype=datetime)
    elif type(clnt_or_series).__qualname__.count("S3"):
        clnt = clnt_or_series
        size = -1
    else:
        raise TypeError(f"'clnt_or_series' can be only pd.Series or boto3.client not {type(clnt_or_series).__qualname__}")

    # Return the latest version if there is no valid access_time
    access_time = access_time if access_time is not None else datetime.now(tz=timezone.utc)

    # Query OpenSearch for the relevant records
    query = {
        "query": {
            "bool": {
                "must": [
                    {"term": {"Bucket.keyword": bkt}},  # .keyword ensures exact match
                    {"term": {"ObjectKey.keyword": obj}}  # .keyword ensures exact match
                ]
            }
        },
        "sort": [
            {"LastModified": "desc"}
        ]
    }

    # Filter by bucket and object key
    table = CFG.G["dbTables"]["objVersionTable"]
    filtered_df = esp.esp_search(table, query, return_type='dataframe')

    # If cache is empty or access_time is later than the latest version in the cache, update the cache
    if clnt and filtered_df.empty or access_time > filtered_df['LastModified'].max():
        filtered_df = _cache_versions(clnt, bkt, obj, size)

    # Filter versions earlier than or equal to access_time
    upper_bound_time = access_time + timedelta(seconds=allow_over_seconds)
    valid_df = filtered_df[filtered_df['LastModified'].le(upper_bound_time) ]

    closest_version = pd.Series(index=['VersionId', 'LastModified', 'IsDeleteMarker', 'Size', 'Sha256'])

    min_difference = float('inf')

    for _, row in valid_df.iterrows():
        difference = abs((access_time - row['LastModified']).total_seconds())
        if sha_256 and row.get("Sha256") == sha_256:
            closest_version = row
            break

        if difference < min_difference:
            min_difference = difference
            closest_version = row

    if not closest_version.empty and not closest_version.isna().all():
        if sha_256 and not closest_version.get('Sha256'):
            # Update the OpenSearch record with sha_256
            esp.esp.es.update(index=table,
                      id=closest_version['R.ID'],
                      body={"doc": {"Sha256": sha_256}})
            closest_version['Sha256'] = sha_256

    return {"R.ID": r_id, 'object.version': closest_version.get('VersionId'),
            'object.flag.deleted': closest_version.get('IsDeleteMarker'),
            'object.time.last_modified': closest_version.get('LastModified'),
            'object.bytes': closest_version.get('Size'),
            'object.sha256': closest_version.get('Sha256')}


def post_index_sha_alias(alias_sha, index_sha):
    """
    Add a document to Opensearch with the _id equal to the alias_sha, typically the sha256 of an object before
    it has been decompressed, and the sha256 of the final indexed object in the data.sha256 field.
    """

    global esp
    esp = ESP(CFG) if esp is None else esp
    table = CFG.G["dbTables"]["dataAliasTable"]

    index_alias = pd.Series(index_sha, index=[alias_sha]).to_frame('data.sha256')
    return esp.post_df_to_es(table, index_alias)
