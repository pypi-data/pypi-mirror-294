# ##################################################################################################
#  Copyright (c) 2022.    Caber Systems, Inc.                                                      #
#  All rights reserved.                                                                            #
#                                                                                                  #
#  CABER SYSTEMS CONFIDENTIAL SOURCE CODE                                                          #
#  No license is granted to use, copy, or share this software outside of Caber Systems, Inc.       #
#                                                                                                  #
#  Filename:  elastic_search_init.py                                                               #
#  Authors:  Rob Quiros <rob@caber.com>  rlq                                                       #
# ##################################################################################################

from datetime import datetime, timezone, timedelta
import os
import time
import json
# import boto3
import requests
import pandas as pd
from urllib.parse import urlsplit
from opensearchpy import OpenSearch as Elasticsearch, AWSV4SignerAuth
from opensearchpy import RequestsHttpConnection, helpers
from opensearchpy import TransportError, ConnectionError, ConnectionTimeout, RequestError

from types import ModuleType

from csiMVP.Dependencies import es_mappings
from csiMVP.Toolbox.retry import retry
from csiMVP.Common.remote_open import ropen
from csiMVP.Toolbox.goodies import b_if_not_a, fnfilter_list, first_valid
from csiMVP.Toolbox.pandas_tools import in_it, set_x, NoNanDict
from csiMVP.Toolbox.notifier import notify_alert
from csiMVP.Toolbox.aws_init import new_aws_client, AWS

try:
    from csiMVP.Common.init import CFG, beginning_of_time
    DEBUG = (CFG.logLevel == "verbose" or CFG.logLevel == "debug")
except ImportError:
    beginning_of_time = datetime.fromisoformat("2000-01-01T00:00:01.011001+00:00")
    CFG = None
    DEBUG = True


AWS_ES_NAME = "es.amazonaws.com"
SupportedElasticsearchTypes = [AWS_ES_NAME, 'elasticsearch', 'opensearch']
ESP_RETRY_ATTEMPTS = 20


def which_cfg(cfg):
    if cfg is None:
        if CFG is not None:
            return CFG
        else:
            raise ImportError("CFG couldn't be imported.  You must pass it as an argument.")
    else:
        return cfg


def check_es_name(name):
    eslist = ['es', 'aws', 'amazon', AWS_ES_NAME]
    if isinstance(name, str) and name.lower() in eslist or any([1 for x in eslist if x in name.lower()]):
        return AWS_ES_NAME
    else:
        return name


def find_es(cfg=None):
    cfg = which_cfg(cfg)
        
    target = cfg.D["Dependencies"]["elastic-search"].get("useTarget", '')
    config = cfg.D["Dependencies"]["elastic-search"]["targets"].get(target) or {}
    error = ''

    if not config:
        error = f"No Elasticsearch configuration found for target '{target}'"
    elif not config.get('urls', []):
        port = f":{config.get('port')}" if config.get('port') else ""
        config.update({'urls': [target + port]})

    if check_es_name(config.get('type', '')) == AWS_ES_NAME:
        urls =  b_if_not_a(config.get("url"), config.get("urls"))
        if isinstance(urls, str):
            urls = [urls]
        for url in urls:
            if AWS_ES_NAME in url:
                us = urlsplit(url)
                if not config.get("scheme", ''):
                    config.update({"scheme": us.scheme})
                ush = us.hostname.split('.', 2)
                if len(ush) == 3 and ush[2] == AWS_ES_NAME:
                    if not config.get("domain", ''):
                        config.update({"domain": ush[0]})
                    if not config.get("region", ''):
                        config.update({"region": ush[1]})
                    return config
                else:
                    error = f"URL configured for AWS OpenSearch must be the 'Domain endpoint (VPC)'"
            elif config.get("domain", '') and config.get("scheme", '') and config.get("region", ''):
                url = f"{config['scheme']}://{config['domain']}.{config['region']}.{AWS_ES_NAME}"
                config.update({"url": url})
                return config
            else:
                error = f"URL configured for AWS OpenSearch must be the 'Domain endpoint (VPC)'"

    elif b_if_not_a(config.get("url"), config.get("urls")):
        urls =  b_if_not_a(config.get("url"), config.get("urls"))
        if isinstance(urls, str):
            urls = [urls]

        # Pop the first URL, and append to the end of the url list, then update CFG. That way if
        # we get a ConnectionError and retry kicks in, the next time we will try the next URL in
        # the list.  Then we'll keep cycling through them until we sucessfully connect.
        url = urls.pop(0)
        urls.append(url)
        config.update({'urls': urls})
        return config
    
    elif config.get('host_full') and config.get('scheme'):
        eurls = config.get('urls') or []
        if isinstance(eurls, str):
            eurls = [eurls]
        if '://' not in config.get('host_full'):
            eurls.append(f"{config.get('scheme')}://{config.get('host_full')}")
            config.update({"urls": eurls})
        else:
            eurls.append(config.get('host_full'))
            config.update({"urls": eurls})
        return config

    elif config.get('ipv4') and not config.get('ipv4', '') == '0.0.0.0':
        eurls = config.get('urls') or []
        if isinstance(eurls, str):
            eurls = [eurls]
        if isinstance(config.get('ipv4'), str):
            config.update({'ipv4': [config.get('ipv4')]})
        for ip in config.get('ipv4'):
            eurls.append(f"{ip}:{config.get('port', 9200)}")
        config.update({"urls": eurls})
        return config
        
    else:
        error = f"Cannot find valid URL in OpenSearch target '{target}'"
        print(error)
        return config

    raise ValueError(error)


def delete_dangling_base_columns(df, name=''):
    """
    Clean-up Hack:  If there is a base column name, say 'user', and child keys of that base like 'user.id'
    in the input DataFrame df, then drop the base column 'user' and keep the child columns 'user.id'.
    This is very specific to the current code path.

    Note this is not a good general solution since the function does not expand the 'user' column, nor update
    the 'user' column with 'id'.  That means it could throw away columns that you might otherwise want to keep.
    """

    nosplit = set(df.columns.to_list())
    splits = pd.DataFrame(df.columns.to_list(), index=df.columns, columns=['splits'])
    splits = splits['splits'].str.split('.', expand=True)

    bad_list = []
    test = splits[0]
    for n in range(1, splits.shape[1]):
        has_n = splits[n].notna()
        bad = nosplit.intersection(test[has_n].to_list())
        bad_list.extend(list(bad))
        test[has_n] = test[has_n] + '.' + splits.loc[has_n, n]

    if bad_list:
        print(f"Removing {f'from {name} ' if name else ''}previously expanded columns {bad_list}")
        df.drop(columns=bad_list)

    return df


def delete_es_indices(table_fnfilter=None, cfg=None):
    
    cfg = which_cfg(cfg)
    esp = ESP(cfg)

    try:
        ret = esp.init_esp_if_needed()
    except ConnectionError as err:
        print(err)
        return False

    if table_fnfilter is None or not len(table_fnfilter):
        print(f"[WARNING] delete_es_indices: No index match filter specified.")
        return True

    table_vals = None
    e_tabs = esp.esp.es.indices.get('*').keys()
    e_tabs = [f for f in e_tabs if not f.startswith(".kib")]

    if not e_tabs:
        print(f"delete_es_indices: No indices in OpenSearch to delete")
        return True

    if isinstance(table_fnfilter, str):
        table_fnfilter = [table_fnfilter]

    if isinstance(table_fnfilter, list):
        table_vals = fnfilter_list(e_tabs, table_fnfilter)

    if table_vals:
        for t in table_vals:
            try:
                esp.esp_delete_index(t)
            except Exception as err:
                print(f"[WARNING] Failed to delete database table '{t}':  {err}")

    return True


class Up:
    df = pd.DataFrame()
    got_start = True
    last_write = 0
    num_calls_seen = 0


upDF = Up()


def updateDF(indf):
    global upDF

    indf_sz = indf.shape[0]

    df = upDF.df
    outdf_sz = df.shape[0]

    if indf_sz and not outdf_sz:
        upDF.df = indf
        num = indf_sz
    elif indf_sz and outdf_sz:
        upDF.df = pd.concat([df, indf], axis=0, ignore_index=True)
        num = upDF.df.shape[0]
    elif not indf_sz and outdf_sz:
        num = outdf_sz
    else:
        num = 0

    upDF.num_calls_seen = num
    return num


# Replaces Process_API.upstream.record() but does not include the post to SQS
# Works for Data_merge record_to_s3()
def record_to_S3(CFG, xDF=None, format='pkl.gz', clear=True, cfg=None):
    '''
    Call this function with a dataframe as the argument and it will append the dataframe to the global
    dataframe and then write the global dataframe to S3.
    If called without a dataframe argument, it will get the global dataframe and, so long as it is not empty,
    write it to S3.
    Once written to S3 the dataframe is NOT cleared in case it is also being sent to another destination,
    for example, elasticsearch.

    Arguments:
        indf    Input pandas dataframe.  If not specified defaults to 'None' and the function behaves as
                described above.

        format  Output file format, defaults to 'pkl.gz'.  Options are:
                'pkl' -> Pickle format. Preserves all dataframe element object attributes.
                'csv' -> Comma-separated-values. All dataframe elements are converted to strings.
                'xls' -> Microsoft Excel format. Some dataframe elements are converted to strings.
                '.gz' -> Suffix to any of the above to gzip compress the file

    '''
    global upDF
    dfrows = 0

    cfg = which_cfg(cfg)

    # if xDF is not None is taken care of by updateDF
    if xDF is not None:
        dfrows = updateDF(xDF)
    df = upDF.df
    if df is not None:
        dfrows = df.shape[0]

    allowed = ['csv', 'xls', 'pkl', 'csv.gz', 'xls.gz', 'pkl.gz']
    if format not in allowed:
        raise ValueError(f"Format can only be one of {allowed} not '{format}")
    ftype = format.split('.')[0]

    if dfrows and df is not None:
        gssob = f'{CFG.rem_cori_prefix(module=CFG.me("pathPrefix"))}/{CFG.me("filePrefix")}' \
                f'[{upDF.last_write + 1}-{upDF.num_calls_seen + upDF.last_write + 1}].'
        gssob += format
        # Write the df to a temp pickle file then copy that to S3
        file = f'{CFG.localdir}/dataframe_out.pkl'
        if ftype == "csv":
            df.to_csv(file)
        elif ftype == "xls":
            df.to_excel(file)
        else:
            df.to_pickle(file)
        with open(file, 'rb') as fin:                # ALWAYS LOCAL - USING SMART_OPEN.OPEN
            with ropen(gssob, 'wb') as fout:
                fout.write(fin.read())
        # os.remove(file)    # will get removed anyway when Lambda exits
        f = gssob.split('/')
        print(f"...Wrote {upDF.num_calls_seen} rows to output file {f[-1]}")
        if clear:
            os.remove(file)    # will get removed anyway when Lambda exits
            upDF.df = pd.DataFrame()
        upDF.last_write += upDF.num_calls_seen + 1
    else:
        print(f"...Empty data frame. No output file written")
    return dfrows


def doc_generator(df, index_name):
    df_iter = df.iterrows()
    for index, document in df_iter:
        yield {
                "_index": index_name,
                "_type": "images",
                "_id": document['R.ID'],
                "_source": document.to_json()
            }
    # raise StopIteration


def fix_times(dmdf, op='', cols=None, extend=True, fill=None):
    """
    Collected all of the various fix time routines I had here.  Input is a DataFrame, Series, or dict.

    parameter 'op' can be one of:
        'from_opensearch': normalize time to pandas datetime.
        'to_opensearch': normalize time to opensearch compatible timestamp
        'to_neo': normalize time to Neo4j timestamp.

    parameter 'cols' and 'extend':
        By default any column name that, ignoring case, contains 'time', 'lastmod', or 'last_mod' is converted.
        Any items in list 'cols' will be appended to the default cols if param 'extend' is True.
        If 'extend' is False then items in cols will replace the default cols.

    """
    dt_kwargs = {"infer_datetime_format": True, "utc": True, "errors": "coerce"}

    if isinstance(dmdf, datetime):
        return pd.to_datetime(dmdf, **dt_kwargs)

    if not isinstance(dmdf, (pd.DataFrame, pd.Series)) or dmdf.empty:
        return dmdf

    # Generate default column list
    tcols = [c for c in dmdf.columns if 'time' in c.lower() or 'last_mod' in c.lower() or 'lastmod' in c.lower()]
    if isinstance(cols, list) and cols:
        if extend:
            tcols.extend(cols)
        else:
            tcols = cols

    if isinstance(fill, str):
        if fill.lower() == 'bot':
            fill = beginning_of_time
        elif fill.lower() == 'now':
            fill = datetime.now(tz=timezone.utc)
        else:
            fill = None

    if op == 'from_opensearch' and tcols:
        fill = pd.NaT if fill is None else fill
        dmdf[tcols] = dmdf[tcols].fillna(fill).transform(pd.to_datetime, **dt_kwargs)
        if 'event.time' in dmdf.columns:
            dmdf.drop(columns=['R.TIME'], inplace=True)
        else:
            dmdf['event.time'] = dmdf['R.TIME']
            dmdf.drop(columns=['R.TIME'], inplace=True)

    elif op == 'to_opensearch':
        # Ensure we have an R.TIME column (for TTL) and that all colums that have a time are in the correct format
        fill = datetime.now(tz=timezone.utc) if fill is None else fill
        if "R.TIME" not in dmdf.columns:
            if "event.time" in dmdf.columns:
                dmdf["R.TIME"] = dmdf['event.time']
            else:
                dmdf["R.TIME"] = datetime.now(tz=timezone.utc)
            tcols.append("R.TIME")

        # Add the expires time for time-to-live
        ttl_sec = CFG.G.get("openSearchTTLsec", 0)
        if ttl_sec > 0:
            dmdf['expires.time'] = dmdf['R.TIME'] + timedelta(seconds=ttl_sec)
            tcols.append('expires.time')

        if tcols:
            dmdf[tcols] = dmdf[tcols].fillna(fill).transform(pd.to_datetime, **dt_kwargs)
    elif tcols:
        print(f"[WARNING] fix_times: Unknown op '{op}'")

    return dmdf


# ############################################################################ #
#     Direct interface to Elasticsearch using Elasticsearch python module      #
# ############################################################################ #
class ES:
    _CFG = None
    esStarted = False
    esClient = None
    _awsauth = None
    _DEBUG = False

    def __init__(self, cfg=None):
        self._CFG = which_cfg(cfg)
        self._DEBUG = (self._CFG.logLevel in ["verbose", "debug"])
        region = self._CFG.D['AWS']['es']['Region']
        credentials = AWS.get_credentials()
        self._awsauth = AWSV4SignerAuth(credentials, region)

    def connectES(self, es_config):
        surl = urlsplit(es_config["url"])
        host = surl.hostname
        implied_port = (surl.scheme == 'https') * 443 + (surl.scheme == 'http') * 80
        port = b_if_not_a(surl.port, b_if_not_a(es_config.get('port', 0), implied_port))
        user = b_if_not_a(surl.username, es_config.get('accessKey', ''))
        pswd = b_if_not_a(surl.password, es_config.get('secretKey', ''))

        if check_es_name(es_config["type"]) == AWS_ES_NAME:
            print('.  ELASTICSEARCH: Connecting to {0}...'.format(host[-20:]))
            try:
                self.esClient = Elasticsearch(
                    hosts=[{'host': host, 'port': 443}],
                    use_ssl=True, verify_certs=False, ssl_show_warn=False,
                    http_auth=self._awsauth, http_compress=True,
                    timeout=10, max_retries=3, retry_on_timeout=True,
                    connection_class=RequestsHttpConnection)
            except Exception as E:
                raise Exception(f"Unable to connect to {host[-20:]}: {E}")
        else:
            n = 1
            while n < 10:
                print(f".  Connecting to Elasticsearch (attempt #{n})")
                # for host in self._CFG.D['Elasticsearch']['hosts']:
                #     print(f".  .  Trying {host['URI']}:{host['port']}")
                #     uri = host['URI'].replace('http://', '').replace('https://', '')
                try:
                    self.esClient = Elasticsearch(
                        hosts=[{'host': host, 'port': port}],
                        use_ssl=False, verify_certs=False, ssl_show_warn=False,
                        http_compress=True, http_auth=(user, pswd),
                        timeout=5, max_retries=4, retry_on_timeout=True,
                        connection_class=RequestsHttpConnection)
                except Exception as E:
                    print(f".  .  DEBUG: Got exception {E}")
                    pass
                    # print(".  .  Unable to connect")
                else:
                    if self.esClient is not None:
                        print(f".  : Success connecting to {es_config['type']}")
                n += 1
                time.sleep(2)
            raise ConnectionError(f"ERROR...Connecting to Elasticsearch host failed")

    def connect_if_needed(self):
        if not self.esStarted:
            es_config = find_es(self._CFG)
            self.connectES(es_config)
            if self.esClient is not None:
                self.esStarted = True
                print(f".  ELASTICSEARCH: Success connecting to {self.esClient.info()['cluster_name']}")
            else:
                raise ConnectionError(f"ERROR...Connecting to Elasticsearch host failed")

    def initializeIndex(self, es_index, esmap=es_mappings):
        self.connect_if_needed()
        if self.esClient.indices.exists(es_index):
            # self.check_reset_index_block(es_index)
            ret = self.esClient.indices.delete(es_index, ignore=[404])
            print(f".  Deleted index {es_index}.  ack={ret['acknowledged']}")
        time.sleep(1)
        if isinstance(esmap, ModuleType):
            ret = self.esClient.indices.create(es_index, body=esmap.es_mappings[es_index])
            # ret = self.esClient.indices.create(es_index, esmap.es_mappings[es_index], include_type_name=True)
        elif isinstance(esmap, dict):
            ret = self.esClient.indices.create(es_index, body=esmap[es_index])
            # ret = self.esClient.indices.create(es_index, esmap[es_index], include_type_name=True)
        else:
            raise TypeError("Mapping for Elasticsearch must be a dict.")

        # Check that there are zero items in the index
        bdy = {"query": {"match_all": {}}}
        count = self.esClient.count(index=es_index, body=bdy)['count']

        print(f".  Created index {es_index}. ack={ret['acknowledged']} count={count}")

    def check_createIndex(self, es_index, esmap=es_mappings):
        self.connect_if_needed()
        if not self.esClient.indices.exists(es_index):
            time.sleep(.5)
            if isinstance(esmap, ModuleType):
                ret = self.esClient.indices.create(es_index, body=esmap.es_mappings[es_index])
                # ret = self.esClient.indices.create(es_index, esmap.es_mappings[es_index], include_type_name=True)
            elif isinstance(esmap, dict):
                ret = self.esClient.indices.create(es_index, body=esmap[es_index])
                # ret = self.esClient.indices.create(es_index, esmap[es_index], include_type_name=True)
            else:
                raise TypeError("Mapping for Elasticsearch must be a dict.")
            print(f".  Created index {es_index}. ack={ret['acknowledged']}")
            return "created"
        else:
            return "exists"

    def check_reset_index_block(self, es_index):
        self.esClient.cluster.put_settings(body={"persistent.cluster.blocks.read_only": False})
        self.esClient.indices.put_settings(index=es_index, body={
            "index.blocks.read_only_allow_delete": None
        })

    def post_DF_to_ElasticSearch(self, index_name, df=None):
        # https://towardsdatascience.com/exporting-pandas-data-to-elasticsearch-724aa4dd8f62
        # # odf['ImportantDate'] = odf['ImportantDate'].apply(safe_date)
        global upDF

        self.connect_if_needed()
        self.check_createIndex(index_name)

        if df is None:
            df = upDF.df

        length = df.shape[0]
        success = True
        retval = [0, 0]
        try:
            retval = helpers.bulk(self.esClient, doc_generator(df, index_name),
                                  stats_only=True, raise_on_error=True, raise_on_exception=True,
                                  max_retries=4, initial_backoff=1, max_backoff=15)
        except requests.exceptions.ReadTimeout as err:
            print(f"WARNING: ELASTICSEARCH Http Read Timeout")
            success = False
        except Exception as err:
            print(f"ERROR: Bulk upload exception - {str(err):.60s}")
            success = False

        if success and retval[0] == length:
            print(f".  ELASTICSEARCH: Success wrote {length}/{retval[0]} records")
        elif success and retval[0] != length:
            print(f".  ELASTICSEARCH: Succeeded writing {retval[0]} and failed at {retval[1]} records")

        # As a backup to saving the DFs to elasticSearch, should we save a copy of DF to S3?
        tos3 = self._CFG.D["global"]["dfOutToS3"]
        if (not success and tos3 != "never") or tos3 == "always":
            record_to_S3(self._CFG, df)           # will also clear the DF
        else:
            upDF.df = pd.DataFrame()     # clear the DF
        return retval[0]

    def get_all_in_window(self, indx, num=100, oldest_time=None, newest_time=None, time_col='event.time'):
        self.connect_if_needed()
        if self.check_createIndex(indx) == "created":
            return None

        if newest_time is None and oldest_time is None:
            bdy = {"query": {"match_all": {}}}
        elif newest_time is None and oldest_time is not None:
            bdy = {"query": {"range": {time_col: {"gte": oldest_time}}}}
        elif newest_time is not None and oldest_time is not None:
            if newest_time > oldest_time:
                bdy = {"query": {"range": {time_col: {"gte": oldest_time, "lte": newest_time}}}}
            else:  # Correct the ordering mistake is caller swapped newest and oldest
                bdy = {"query": {"range": {time_col: {"gte": newest_time, "lte": oldest_time}}}}
        else:
            bdy = {"query": {"range": {time_col: {"gte": beginning_of_time, "lte": newest_time}}}}

        try:
            retval = self.esClient.search(index=indx, size=num, sort=f'{time_col}:asc', body=bdy)
            nhits = len(retval["hits"]["hits"])
            thits = retval["hits"]["total"]["value"]
            if self._DEBUG:
                print(f'.  Search "{indx}" success: returned {nhits} out of {thits} records')
        except Exception as err:
            print("ERROR: Exception in call to search:  ", err)
            return None
        try:
            if not len(retval['hits']['hits']):
                return None
        except KeyError as err:
            print("ERROR: Search return value had no key hits  ", err)
            return None
        return [rec['_source'] for rec in retval['hits']['hits']]

    def get_S3_accesses_in_window(self, oldest_time, newest_time, time_col='event.time'):
        self.connect_if_needed()
        indx = self._CFG.G["dbTables"].get('objScanTable', 'object-indices')
        if self.check_createIndex(indx) == "created":
            return None

        if newest_time == "all":
            bdy = {"query": {"match_all": {}}}
        else:
            bdy = {"query": {"range": {time_col: {"gte": oldest_time, "lte": newest_time}}}}
        fields = [time_col, "bucket", "key"]

        try:
            retval = self.esClient.search(index=indx, size=100, body=bdy, _source_includes=fields)
            if self._DEBUG:
                print(f'.  Search "{indx}" success: returned={json.dumps(retval)[0:240]}')
        except Exception as err:
            print("ERROR: Exception in call to search:  ", err)
            return None
        try:
            if not len(retval['hits']['hits']):
                return None
        except KeyError as err:
            print("ERROR: Search return value had no key hits  ", err)
            return None
        objhits = {}
        for rec in retval['hits']['hits']:
            s3Url = f"s3://{self._CFG.bucket}/{self._CFG.D['S3scanner']['pathPrefix']}/{rec['_source']['bucket']}" \
                    f"/{rec['_source']['key']}{self._CFG.G['filenameSuffixes']['index']}"
            objhits.update({rec['_source'][time_col]: {'s3Url': s3Url}})
        objhits = pd.DataFrame(objhits)
        objhits.sort_index(inplace=True)
        return objhits.T


# ############################################################################ #
#      Interface to Elasticsearch using ES-Pandas python module                #
# ############################################################################ #
class ESP:
    _awsauth = None
    esStarted = False
    esp = None
    host = ''
    connect_url = None
    version = "?.?.?"
    flavor = "unknown"
    cluster_name = "unknown"
    ttl_field = 'expires'
    _hit_trigger = False

    def __init__(self, cfg=None, retries=20):
        global ESP_RETRY_ATTEMPTS
        ESP_RETRY_ATTEMPTS = int(retries)
        self._CFG = which_cfg(cfg)
        if self._CFG.platform.lower().startswith('aws'):
            self._awsauth = AWSV4SignerAuth(AWS.get_credentials(), AWS.region_name)

    def create_index_if_needed(self, es_index, esmap=es_mappings):
        """
        Returns False if the index already exists, True if the index was just created.
        """
        ret = self.esp.ic.exists(es_index)
        if not ret:
            if isinstance(esmap, ModuleType):
                ret = self.esp.ic.create(es_index, body=esmap.es_mappings.get(es_index))
            elif isinstance(esmap, dict):
                ret = self.esp.ic.create(es_index, body=esmap.get(es_index))
            else:
                raise TypeError("Mapping for Elasticsearch must be a dict.")
            print(f".  Created index {es_index}. ack={ret['acknowledged']}")
            self.esp.ic.refresh(index=es_index)
            ret = self.esp.ic.exists(index=es_index)
            return ret

    def get_version(self):
        self.init_esp_if_needed()
        info = self.esp.es.info()
        if isinstance(info, dict):
            self.cluster_name = info.get('cluster_name') or "unknown"
            info = info.get("version", {})
            self.version = info.get("number") or "?.?.?"
            self.flavor = info.get("build_flavor") or "unknown"
            print(f"Connected to OpenSearch cluster '{self.cluster_name}' type '{self.flavor}' version '{self.version}'")
        else:
            print(f"[WARNING] Call to esp.es.info() returned unexpected result {info}")


    @retry(RuntimeError, total_tries=ESP_RETRY_ATTEMPTS, initial_wait=10, backoff_factor=1.2, no_print=True)
    def init_esp_if_needed(self):
        if not self.esStarted:
            es_config = find_es(self._CFG)

            urls = [u.strip('. -') for u in (self.connect_url, es_config.get('url'),
                                *es_config.get('urls', []), es_config.get("host_full")) if u]

            if len(urls) == 0:
                raise ValueError(f"No URL or domain configured for {es_config.get('host')} Host")

            for url in urls:
                if '://' not in url:
                    surl = urlsplit("http://" + url)
                else:
                    surl = urlsplit(url)
                host = surl.hostname
                self.host = host

                # print(f"[DEBUG] Trying OpenSearch URL {url}")

                implied_port = (surl.scheme == 'https') * 443 + (surl.scheme == 'http') * 80
                port = b_if_not_a(surl.port, b_if_not_a(es_config.get('port', 0), implied_port))
                user = b_if_not_a(surl.username, es_config.get("accessKey", ''))
                pswd = b_if_not_a(surl.password, es_config.get("secretKey", ''))

                if check_es_name(es_config["type"]) == AWS_ES_NAME:
                    prhost = surl.hostname.split('.', 1)[0].rsplit('-', 1)[0]
                    region = b_if_not_a(surl.hostname.split('.')[-4], es_config.get('region', ''))
                    credentials = AWS.get_credentials()
                    self._awsauth = AWSV4SignerAuth(credentials, region)
                    print(f'{self.host}: Initiating connection ')
                    try:
                        self.esp = es_pandas(
                            hosts=[{'host': host, 'port': 443}],
                            use_ssl=True, verify_certs=False, ssl_show_warn=False,
                            http_auth=self._awsauth, http_compress=True,
                            timeout=20, max_retries=3, retry_on_timeout=True,
                            connection_class=RequestsHttpConnection)
                    except ConnectionTimeout as err:
                        if host.lower().startswith('vpc-'):
                            raise ValueError(f"Cannot connect to AWS Opensearch domain '{prhost}' ... Am I not running inside the domain configured VPC?")
                    except Exception as err:
                        print(f"Opensearch: Got error connecting {err}")
                    else:
                        self.esStarted = True
                        es_config.update({'url': url, 'is_up': True, 'initialized': True})
                        self.get_version()
                        return True
                else:
                    try:
                        self.esp = es_pandas(
                            hosts=[{'host': host, 'port': port}],
                            use_ssl=False, verify_certs=False, ssl_show_warn=False,
                            http_compress=True, http_auth=(user, pswd),
                            timeout=10, max_retries=3, retry_on_timeout=True,
                            connection_class=RequestsHttpConnection)
                    except (ConnectionTimeout, ConnectionError) as err:
                        pass
                    else:
                        self.esStarted = True
                        if self.esp is not None:
                            es_config.update({"host_full": f"{host}:{port}"})   # This will update the main CFG object
                            es_config.update({'url': url, 'is_up': True, 'initialized': True})
                            self.get_version()
                            return self.esp

            raise RuntimeError(f"OpenSearch connect failed to all in {urls}")

        else:
            self.check_resources(show=False)
            return self.esp

    @retry((TransportError, ConnectionError, ConnectionTimeout), total_tries=3)
    def post_df_to_es(self, index_name, df=None, op="auto", clean='none'):
        """
        Post dataframe 'df' to ElasticSearch index 'index_name'.  Default operation 'op' is 'auto' meaning
        rows in df that do not exist in index_name will be created, and rows that do exist will be updated.
        'auto' differs from 'index' in that the latter will completely replace existing documents with
        new documents.

        Clean specifies what to do with values that are empty but not None, NaN, NaT, etc.  If clean = all,
        any value where bool(value) = False will be replaced by None to allow for a future update that has a value
        to replace the None.

        :param index_name:
        :param df:
        :param op: 'create', 'update', 'delete', 'index', or 'auto'
        :param clean: 'all', 'str_only', 'except_numbers', 'none' (default)
        :return:
        """
        global upDF

        df = upDF.df if df is None else df
        if not isinstance(df, (pd.DataFrame, pd.Series)) or df.empty:
            return 0

        self.init_esp_if_needed()
        self.create_index_if_needed(index_name)

        doctype = index_name + '-doc'

        # Make R.ID the index if we haven't already
        if df.get('R.ID', None) is not None:
            df.set_index('R.ID', inplace=True, drop=False)

        nulls = pd.DataFrame()
        numa = 0
        numb = 0
        df = df.copy()

        # Ensure we have an event.time column (for TTL) and that all colums that have a time are in the correct format
        df = fix_times(df, op='to_opensearch')

        if clean == 'all':
            nulls = df.applymap(lambda x: not isinstance(x, (int, float, bool)) and not x) | df.isna()
        elif clean == 'str_only':
            nulls = df.applymap(lambda x: isinstance(x, str) and x == '') | df.isna()
        elif clean == 'except_numbers':
            nulls = df.applymap(lambda x: not isinstance(x, (int, float)) and not x) | df.isna()

        if clean in ['all', 'str_only', 'except_numbers']:
            df.mask(nulls, np.nan, inplace=True)

        df.dropna(axis=1, how='all', inplace=True)
        df['RecordModifiedBy'] = CFG.user_agent

        df.fillna(np.nan, inplace=True)
            
        try:
            oper = op if op != 'auto' else 'create'
            numa = self.esp.to_es(df, index_name, doc_type=doctype, use_index=True, _op_type=oper,
                                  thread_count=2, chunk_size=500, show_progress=False,
                                  use_pandas_json=False)

        except helpers.errors.BulkIndexError as err1:
            # If 'create' fails then try 'update' with the failed records
            if op == 'auto':
                err_ids = [x.get('create', {}).get('_id', '') for x in err1.errors]
                try:
                    numb = self.esp.to_es(df.loc[df.index.intersection(err_ids)], index_name,
                                          doc_type=doctype, use_index=True, _op_type='update',
                                          thread_count=2, chunk_size=500, show_progress=False,
                                          use_pandas_json=False)
                except helpers.errors.BulkIndexError as err:
                    msg = err.errors[0].get('update', {}).get('error', {}).get('reason', '')
                    msg1 = {x.get('create', {}).get('_id', '<err>'): x.get('create', {}).get('error', {}).get('reason', '') for x in err1.errors if 'document already exists' not in x.get('create', {}).get('error', {}).get('reason', '')}
                    print(f"[WARNING] Upload to ES failed after update: {msg}\n{msg1}")
            else:
                msg = err1.errors[0].get('update', {}).get('error', {}).get('reason', '')
                msg = err1 if not msg else msg
                print(f"[WARNING] Upload to ES failed: {msg}")

        return numa + numb

    def update_es_lists(self, indf, id_col_name='R.ID', agg_dict=None, exclude_cols=None, time_cols=None, index=''):
        """
        Deduplicate entries in input DataFrame XDF, and create unique IDs from the values. Read from index
        to see if these unique IDs were already entered and update them with the new entries.

        This is different than a post_df_to_es in that columns name in param agg_dict's keys whose values
        are 'set' will be aggregated into lists before updating OpenSearch.  This allows OpenSearch to
        have a growing set of new values in these columns.

        agg_dict is a standard {column: function} dictionary that would be passed to pd.DataFrame.groupby().agg(agg_dict)
        except the function names as strings will be replaced with the actual function names if needed.

        """

        if not isinstance(indf, pd.DataFrame) or not isinstance(agg_dict, dict) or not index or not id_col_name \
                or id_col_name not in indf.columns:
            print(f"[DEBUG] update_es_lists: Bad arguments")
            return indf, pd.DataFrame()

        xdf = indf.copy() # Make a copy so we don't modify the original.

        # # Check for innapropriate columns in xdf and get rid of them unless keep_all = True
        # if not keep_all:
        #     xdf = filter_columns_to_link_data(xdf, id_col_name=id_col_name)

        id_api = xdf.get(id_col_name, pd.Series(index=xdf.index, name=id_col_name, dtype='O'))

        # no_dupes has only unique values for querying OpenSearch
        no_dupes = id_api.drop_duplicates().dropna()
        no_dupes = pd.DataFrame(no_dupes.dropna(), columns=[id_col_name])
        no_dupes = no_dupes.set_index(id_col_name, drop=False)

        # Now query the DB to get the previously discovered records.
        from_esp = self.get_self_from_es(index, no_dupes) if not no_dupes.empty else no_dupes

        time_cols = in_it(time_cols, from_esp)
        if not from_esp.empty and time_cols:
            for tcol in time_cols:
                from_esp[tcol] = from_esp[tcol].apply(pd.to_datetime)

        to_esp = []
        aggs = in_it(agg_dict, xdf)
        no_do = in_it(exclude_cols, xdf)
        no_do.append(id_col_name)

        # Aggregate values for each unique value of id_col_name
        for col in xdf.columns.difference(no_do):
            if not from_esp.empty and in_it(col, from_esp):
                if aggs.get(col) in [set_x, "set", "set_x", "list"]:
                    texp = from_esp.explode(col)
                    texp = texp.loc[texp[col].notna()]
                    before_len = texp.shape[0]
                    xexp = xdf.explode(col)
                    xexp = xexp.loc[xexp[col].notna()]
                    texp = pd.concat([xexp[[id_col_name, col]], texp[[id_col_name, col]]],
                                     ignore_index=True).drop_duplicates()
                    after_len = texp.shape[0]
                    if before_len < after_len:  # ('user.from.host.id', 'user.id')
                        notify_alert(xdf, thing_col=id_col_name, in_thing_col=col,
                                     category=id_col_name.capitalize().split('.')[0])
                else:
                    texp = pd.concat([xdf[[id_col_name, col]], from_esp[[id_col_name, col]]], ignore_index=True)
            else:
                texp = xdf[[id_col_name, col]]

            if aggs.get(col) in [set_x, "set", "set_x", "list"]:
                texp = texp.groupby(id_col_name, as_index=True, sort=False).agg({col: set_x})
            elif aggs.get(col) in [max, "max"]:
                texp = texp.groupby(id_col_name, as_index=True, sort=False).max()
            elif aggs.get(col) in [min, "min"]:
                texp = texp.groupby(id_col_name, as_index=True, sort=False).min()
            elif aggs.get(col) in [any, "any"]:
                texp = texp.groupby(id_col_name, as_index=True, sort=False).any()
            else:
                texp = texp.groupby(id_col_name, as_index=True, sort=False).last()

            to_esp.append(texp)

        # Each columns' result is in a separate series and to_esp holds them in a list.  So concatentate them all into a DF
        to_esp = pd.concat(to_esp, axis=1)
        to_esp[id_col_name] = to_esp.index
        to_esp['R.ID'] = to_esp.index

        # The first time we enter a value in a column that is supposed to be a list/array in OpenSearch
        # that value must be in a list, otherwise OpenSearch will treat it as a single value forever more.
        to_list = lambda L: [L] if isinstance(L, str) else L if isinstance(L, list) else None
        do_nada = lambda N: N
        to_esp = to_esp.apply({c: to_list if aggs.get(c) == set_x else do_nada for c in to_esp.columns})
        to_esp = to_esp.sort_index(axis=1, ascending=True)

        to_esp = delete_dangling_base_columns(to_esp, "'to_esp' in function update_es_lists")
        ret = self.post_df_to_es(index, to_esp)

        new_apis = to_esp.index.difference(from_esp.index)
        if len(new_apis) and DEBUG:
            notify_alert(to_esp, thing_col=id_col_name, msg='endpoint', category='API')

        return xdf, to_esp

    @retry((TransportError, ConnectionError, ConnectionTimeout), total_tries=3)
    def esp_delete_index(self, index_name):
        self.init_esp_if_needed()
        if not self.esp.ic.exists(index_name):
            print(f"{self.host}: No index '{index_name}' exists")
            return True

        bdy = {"query": {"match_all": {}}}
        count = self.esp.es.count(index=index_name, body=bdy)['count']
        print(f"Deleting Elasticsearch index '{index_name}' containing {count} records")

        ret = self.esp.ic.delete(index_name)
        if isinstance(ret, dict):
            if 'acknowledged' in ret.keys():
                if ret['acknowledged']:
                    try:
                        count = self.esp.es.count(index=index_name, body=bdy)['count']
                    except Exception as err:
                        print(f"{self.host}: Deleted index '{index_name}' containing {count} records")
                    else:
                        print(f"[WARNING] Delete un-successful count = {count}")
                    return True
        else:
            raise ConnectionError
        return False

    @retry((TransportError, ConnectionError, ConnectionTimeout), total_tries=3)
    def _delete_expired_records(self, index_name):
        """
        Implement time-to-live for records in ElasticSearch by using the expiry time added by
        post_df-to_es as a way of determining which records (documents) have exipred.
        Function is disabled if CFG.G.get("openSearchTTLsec", 0) doesn't exist or is <= 0.
        :param index_name:
        :return:
        """
        self.init_esp_if_needed()

        # Function is
        ttl_sec = CFG.G.get("openSearchTTLsec", 0)
        if isinstance(ttl_sec, int) and ttl_sec <= 0:
            return {}

        # Calculate the current time in the format used by OpenSearch
        current_time = fix_times(datetime.now(tz=timezone.utc))

        # Query to find documents where the ttl_field is less than the current time
        query = {
            "query": {
                "range": {
                    'expires.time': {
                        "lt": current_time
                    }
                }
            }
        }

        # Delete the documents that match the query
        try:
            response = self.esp.es.delete_by_query(index=index_name, body=query)
        except Exception as err:
            print(f"[DEBUG] While deleting expired records in {index_name}: {err}")
            response = {}
        return response

    @retry((TransportError, ConnectionError, ConnectionTimeout), total_tries=3)
    def get_self_from_es(self, index_name, df=None):
        global upDF

        if df is None:
            df = upDF.df

        if isinstance(df, pd.DataFrame) and df.shape[0]:
            ids_to_lookup = list(df.index)
        elif isinstance(df, pd.Index) and df.shape[0]:
            ids_to_lookup = list(df)
        elif isinstance(df, (list, set)) and len(df):
            ids_to_lookup = list(df)
        else:
            # print(f"[DEBUG] (get_self_from_es) Empty dataframe or index argument")
            return pd.DataFrame()

        ids_to_lookup = [i for i in ids_to_lookup if isinstance(i, str) and i != '']
        ret_df = pd.DataFrame()

        self.init_esp_if_needed()
        if self.create_index_if_needed(index_name):
            return ret_df      # don't bother with a lookup if the index was just created.

        # Expire records in the index if TTL is enabled
        self._delete_expired_records(index_name)

        # Query to get the existing items in the index
        bdy = {"query": {"ids": {"values": ids_to_lookup}}}
        count = self.esp.es.count(index=index_name, body=bdy)
        # print(f"[DEBUG] (get_self_from_es) Count1 is {count} on df with {len(ids_to_lookup)} items")
        count = self.esp.es.count(index=index_name, body=bdy)
        # print(f"[DEBUG] (get_self_from_es) Count2 is {count} on df with {len(ids_to_lookup)} items")
        if count['count'] > 0:
            ret_df = self.esp.to_pandas(index_name, infer_dtype=True, query_rule=bdy, show_progress=False)
        return fix_times(ret_df, op='from_opensearch')

    @retry((TransportError, ConnectionError, ConnectionTimeout), total_tries=3)
    def delete_df_items_from_es(self, index_name, df):
        global upDF

        if df is None or not df.shape[0]:
            print(f".  (delete_df_items_from_es) No items to delete")
            return 0

        self.init_esp_if_needed()
        if self.create_index_if_needed(index_name) == 0:
            return 0

        # Make R.ID the index if we haven't already
        if df.get('R.ID', None) is not None:
            df.set_index('R.ID', inplace=True, drop=False)
        doctype = index_name + '-doc'
        dflen = df.shape[0]

        return self.esp.to_es(df, index_name, doc_type=doctype, use_index=True, _op_type='delete',
                              thread_count=2, chunk_size=500, show_progress=False,
                              use_pandas_json=False)

    @retry((TransportError, ConnectionError, ConnectionTimeout), total_tries=3)
    def get_in_window(self, indx, num=100, oldest_time=None, newest_time=None, min_recs=0, time_col='event.time'):
        global upDF
        ret_df = pd.DataFrame()

        self.init_esp_if_needed()
        if self.create_index_if_needed(indx) == 0:
            return pd.DataFrame()

        if newest_time is None and oldest_time is None:
            bdy = {"query": {"match_all": {}}}
            # count = esp.es.count(index=indx, body=bdy)['count']
            # anl = helpers.scan(esp.es, query=bdy, index=indx, size=num)
        elif newest_time is None and oldest_time is not None:
            if isinstance(oldest_time, float):
                oldest_time = datetime.fromtimestamp(oldest_time, tz=timezone.utc)
            bdy = {"query": {"range": {time_col: {"gte": oldest_time}}}}
        elif newest_time is not None and oldest_time is not None:
            if isinstance(oldest_time, float):
                oldest_time = datetime.fromtimestamp(oldest_time, tz=timezone.utc)
            if isinstance(newest_time, float):
                newest_time = datetime.fromtimestamp(newest_time, tz=timezone.utc)
            if newest_time > oldest_time:
                bdy = {"query": {"range": {time_col: {"gte": oldest_time, "lte": newest_time}}}}
            else:  # Correct the ordering mistake is caller swapped newest and oldest
                bdy = {"query": {"range": {time_col: {"gte": newest_time, "lte": oldest_time}}}}
        else:
            bdy = {"query": {"range": {time_col: {"gte": beginning_of_time, "lte": newest_time}}}}
        # FIXME: es-pandas ignores NUM in queries so I have to pull the entire database then drop
        count = self.esp.es.count(index=indx, body=bdy)['count']
        if count > min_recs:
            ret_df = self.esp.to_pandas(indx, infer_dtype=True, query_rule=bdy, show_progress=False,
                                        size=num, sort=f'{time_col}:asc')
            ret_df.sort_values(by=time_col, axis=0, ascending=True, inplace=True)
        return fix_times(ret_df.tail(max(num, min_recs)), op='from_opensearch')

    @retry((TransportError, ConnectionError, ConnectionTimeout), total_tries=3)
    def esp_delete_older_than(self, indx, oldest_time=None, time_col='event.time'):
        self.init_esp_if_needed()
        if not oldest_time or self.create_index_if_needed(indx) == 0:
            print(f".  (esp_delete_older_than) No items to delete from '{indx}")
            return 0

        bdy = {"query": {"range": {time_col: {"lte": oldest_time}}}}

        count = self.esp.es.count(index=indx, body=bdy)['count']
        if count > 0:
            self.esp.es.delete_by_query(index=indx, body=bdy)
            print(f".  (esp_delete_older_than) Deleted {count} items from '{indx}' where '{time_col}' is "
                  f"older than {oldest_time.isoformat()}")
        else:
            print(f".  (esp_delete_older_than) No items to delete from '{indx}")
        return count

    @retry((TransportError, ConnectionError, ConnectionTimeout), total_tries=3)
    def _delete_oldest_5_percent(self, index_name):
        self.init_esp_if_needed()
        # 1. Get the timestamps of the oldest and newest documents
        body = {
            "size": 0,
            "aggs": {
                "min_timestamp": {
                    "min": {
                        "field": "expires.time"
                    }
                },
                "max_timestamp": {
                    "max": {
                        "field": "expires.time"
                    }
                }
            }
        }

        response = self.esp_search(index=index_name, body=body)
        min_timestamp = datetime.strptime(response['aggregations']['min_timestamp']['value_as_string'],
                                          '%Y-%m-%dT%H:%M:%S.%fZ')
        max_timestamp = datetime.strptime(response['aggregations']['max_timestamp']['value_as_string'],
                                          '%Y-%m-%dT%H:%M:%S.%fZ')

        # 2. Compute the time duration between the oldest and newest timestamps
        time_range = max_timestamp - min_timestamp

        # 3. Calculate 5% of this duration
        five_percent_duration = time_range * 0.05

        # 4. Add this to the oldest timestamp to get the cut-off timestamp
        cutoff_timestamp = min_timestamp + five_percent_duration
        cutoff_timestamp_str = cutoff_timestamp.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

        # Delete the documents older than the cut-off timestamp
        delete_query = {
            "query": {
                "range": {
                    "timestamp": {
                        "lte": cutoff_timestamp_str
                    }
                }
            }
        }
        self.esp_delete_older_than(index=index_name, body=delete_query)

    def get_open_scroll_contexts(self):
        stats = self.esp.es.nodes.stats(metric='indices')
        indx = list(stats.get('nodes', {}).keys())
        if not indx:
            return 0
        return stats.get('nodes', {}).get(indx[0], {}).get('indices', {}).get('search', {}).get('open_contexts', 0)

    def check_resources(self, jvm_mem_max=80, tot_mem_min=900000,  disk_max=80, show=True):
        # Fetch cluster stats
        stats = self.esp.es.cluster.stats()

        # Get memory and disk usage percentages
        total_memory = stats["nodes"]["jvm"]["mem"]['heap_max_in_bytes']
        used_memory = stats["nodes"]["jvm"]["mem"]["heap_used_in_bytes"]
        jvm_mem_used_pcnt = int(100 * used_memory / total_memory)
        total_mem_used_pcnt = stats["nodes"]["os"]["mem"]["used_percent"]
        total_mem_free_bytes = stats["nodes"]["os"]["mem"]["free_in_bytes"]
        total_disk = stats["nodes"]["fs"]["total_in_bytes"]
        free_disk = stats["nodes"]["fs"]['available_in_bytes']
        disk_used_pcnt = int(100 * (total_disk - free_disk) / total_disk)

        message = f"{disk_used_pcnt}% disk, " \
                  f"{jvm_mem_used_pcnt}% JVM memory, " \
                  f"{total_mem_used_pcnt}% total memory " \
                  f"{total_mem_free_bytes/1024}KB total memory free."

        if not self._hit_trigger and total_mem_free_bytes < tot_mem_min:
            self._hit_trigger = True  # Fix recursion problem so only one process does this.
            print(f"[WARNING] OpenSearch Resources at limit: {message} \n"
                  f"[WARNING] OpenSearch Resources at limit: Deleting 5% of all oldest event records.")
            indxs = [v for k,v in CFG.G["dbTables"].items() if 'event' in k.lower() and self.esp.ic.exists(v)]
            # for i in indxs:
            #     self._delete_oldest_5_percent(i)
            self._hit_trigger = False
        elif show:
            print(f"OpenSearch Resources Used: {message}")
        return {"mem_free": total_mem_free_bytes, "jvm_mem": jvm_mem_used_pcnt, "disk": disk_used_pcnt}


    @retry((TransportError, ConnectionError, ConnectionTimeout), total_tries=3)
    def esp_query(self, indx, query, num=100, time_col='event.time'):
        if query is None or indx is None:
            return
        self.init_esp_if_needed()
        if self.create_index_if_needed(indx) == 0:
            return pd.DataFrame()

        err1 = query.pop('_source', None)
        err2 = query.pop('sort', None)
        num = query.pop('size', num)

        ret_df = pd.DataFrame()
        try:
            count = self.esp.es.count(index=indx, body=query)['count']
            if count > 0:
                ret_df = self.esp.to_pandas(indx, infer_dtype=True, query_rule=query, show_progress=False,
                                        size=num, sort=f'{time_col}:asc')
        except RequestError as err:
            print(f"[ERROR] Exception esp_query: {err}")
            return pd.DataFrame()

        return fix_times(ret_df, op='from_opensearch')

    @retry((TransportError, ConnectionError, ConnectionTimeout), total_tries=3)
    def get_matching_fields(self, index_name, columns=None):
        self.init_esp_if_needed()

        if self.create_index_if_needed(index_name) == 0:
            return []

        if columns is None:
            columns = ["*.id", "*.sha256"]

        query = {"query": {"match_all": {}}, "size": 1}
        res = self.esp_search(index_name, query, return_type='dataframe')
        all_fields = res.columns

        # Filter fields based on the given criteria
        matching_fields = fnfilter_list(all_fields, columns)

        return matching_fields


    @retry((TransportError, ConnectionError, ConnectionTimeout), total_tries=3)
    def esp_search(self, indx, search, score=0, return_type='raw', **kwargs):
        empty = None
        if return_type == 'dataframe':
            empty = pd.DataFrame()

        if search is None or indx is None:
            return empty

        self.init_esp_if_needed()
        if self.create_index_if_needed(indx) == 0:
            return empty

        max_scroll_contexts = 500  # This should match the Elasticsearch setting
        max_retries = 5
        retry_delay = 5  # seconds
        for attempt in range(max_retries):
            open_contexts = self.get_open_scroll_contexts()
            if open_contexts < max_scroll_contexts:
                try:
                    ret = self.esp.es.search(index=indx, body=search, **kwargs)
                    dfb = {r['_id']: r['_source'] for r in ret.get('hits', {}).get('hits', []) if
                           r.get('_id') and r.get('_source') and (r.get('_score') if r.get('_score') else score) >= score}
                    sret = fix_times(pd.DataFrame(dfb).T, op='from_opensearch')
                    # print(f"[DEBUG](esp_search): Index {indx} First ret is {sret.shape} query={search}")
                except Exception as err:
                    print(f"[WARNING](esp_search): {err}")
                    return empty

                if return_type != 'dataframe':
                    sret = ret.copy()

                scroll_id = ret.get('_scroll_id', None)
                if scroll_id is not None:
                    # The '3m' is the time value Elasticsearch "scrolls" for: m for milliseconds and s for seconds
                    scroll_val = kwargs.get("scroll", "3m")
                    while len(ret.get('hits', {}).get('hits', [])) > 0:
                        # Fetch the next batch of search hits
                        ret = self.esp.es.scroll(scroll_id=scroll_id, scroll=scroll_val)
                        if return_type != 'dataframe':
                            sret['hits']['hits'].extend(ret.get('hits', {}).get('hits', []))
                        else:
                            dfb = {r['_id']: r['_source'] for r in ret.get('hits', {}).get('hits', []) if
                                   r.get('_id') and r.get('_source') and
                                   (r.get('_score') if r.get('_score') else score) >= score}
                            sret = pd.concat([sret, fix_times(pd.DataFrame(dfb).T, op='from_opensearch')])
                    # print(f"[DEBUG](esp_search): Index {indx} Second ret is {sret.shape}")
                return sret
            else:
                print(f"[WARNING] Too many open scroll contexts ({open_contexts}). Waiting {retry_delay}s before retrying...")
                time.sleep(retry_delay)

        print(f"[WARNING](esp_search): Could not perform search after {max_retries} attempts due to too many open scroll contexts.")
        return empty

################################################################################################################
# Below code is a fork of es-pandas https://github.com/fuyb1992/es_pandas/blob/master/es_pandas/es_pandas.py
# that removes the 'progressbar' dependency and supports the use of opensearch-py instead of elasticsearch-py
# so we can take advantage of AWS opensearch service.
################################################################################################################

import re
# import warnings
# import progressbar

# if not progressbar.__version__.startswith('3.'):
#     raise Exception('Incorrect version of progerssbar package, please do pip install progressbar2')

import numpy as np
# import pandas as pd

from pandas.io import json as pjson
# from elasticsearch import Elasticsearch, helpers


class es_pandas(object):
    '''Read, write and update large scale pandas DataFrame with Elasticsearch'''

    def __init__(self, *args, **kwargs):
        self.es = Elasticsearch(*args, **kwargs)
        self.ic = self.es.indices
        self.dtype_mapping = {'text': 'category', 'date': 'datetime64[ns]'}
        self.id_col = '_id'
        if self.es.info()['version'].get('distribution', '').lower() == 'opensearch':
            self.es_version_str = self.es.info()['version'].get('minimum_wire_compatibility_version', '<KeyError>')
            self.es_version = [int(x) for x in re.findall("[0-9]+", self.es_version_str)]
            self.es_version[0] += 1
        else:
            self.es_version_str = self.es.info()['version'].get('number', '<KeyError>')
            self.es_version = [int(x) for x in re.findall("[0-9]+", self.es_version_str)]
        if self.es_version[0] < 6:
             raise Exception(f'ElasticSearch <= version 5.x is not supported.  You have version = {self.es_version_str}')

    def to_es(self, df, index, doc_type=None, use_index=False, show_progress=True,
              success_threshold=0.9, _op_type='index', use_pandas_json=False, date_format='iso', **kwargs):
        '''
        :param df: pandas DataFrame data
        :param index: full name of es indices
        :param doc_type: full name of es template
        :param use_index: use DataFrame index as records' _id
        :param success_threshold:
        :param _op_type: elasticsearch _op_type, default 'index', choices: 'index', 'create', 'update', 'delete'
        :param use_pandas_json: default False, if True, use pandas.io.json serialize
        :param date_format: default iso, only works when use_pandas_json=True
        :return: num of the number of data written into es successfully
        '''

        if df.empty:
            return 0

        if self.es_version[0] > 6:
            doc_type = None
        elif self.es_version[0] > 5:
            doc_type = '_doc'
        elif not doc_type:
            doc_type = index + '_type'    # OpenSearch versions start back at 1!
        gen = helpers.parallel_bulk(self.es,
                                    (self.rec_to_actions(df, index, doc_type=doc_type, show_progress=show_progress,
                                                         use_index=use_index, _op_type=_op_type,
                                                         use_pandas_json=use_pandas_json, date_format=date_format)),
                                    **kwargs)

        success_num = np.sum([res[0] for res in gen])
        rec_num = len(df)
        fail_num = rec_num - success_num

        if (success_num / rec_num) < success_threshold:
            raise Exception('%d records write failed' % fail_num)

        return success_num

    def get_source(self, anl, show_progress=False, count=0):
        if show_progress:
            for mes in anl:
                yield {'_id': mes['_id'], **mes['_source']}
            # with progressbar.ProgressBar(max_value=count) as bar:
            #     for i in range(count):
            #         mes = next(anl)
            #         yield {'_id': mes['_id'], **mes['_source']}
            #         bar.update(i)
        else:
            for mes in anl:
                yield {'_id': mes['_id'], **mes['_source']}

    def infer_dtype(self, index, heads):
        if self.es_version[0] > 6:
            mapping = self.ic.get_mapping(index=index)
        else:
            # Fix es client unrecongnized parameter 'include_type_name' bug for es 6.x
            mapping = self.ic.get_mapping(index=index)
            key = [k for k in mapping[index]['mappings'].keys() if k != '_default_']
            if len(key) < 1: raise Exception('No templates exits: %s' % index)
            mapping[index]['mappings']['properties'] = mapping[index]['mappings'][key[0]]['properties']
        dtype = {k: v['type'] for k, v in mapping[index]['mappings']['properties'].items() if k in heads and v.get('type') is not None}
        dtype = {k: self.dtype_mapping[v] for k, v in dtype.items() if v in self.dtype_mapping}
        return dtype

    def to_pandas(self, index, query_rule=None, heads=None, dtype=None, infer_dtype=False, show_progress=True, query_sql=None, **kwargs):
        """
        scroll datas from es, and convert to dataframe, the index of dataframe is from es index,
        about 2 million records/min
        Args:
            index: full name of es indices
            query_rule: dict, default match_all, elasticsearch query DSL
            heads: certain columns get from es fields, [] for all fields
            dtype: dict like, pandas dtypes for certain columns
            infer_dtype: bool, default False, if true, get dtype from es template
            show_progress: bool, default True, if true, show progressbar on console
            query_sql: string or dict, default None, SQL containing query to filter
        Returns:
            DataFrame
        """
        if not query_rule:
            query_rule = {'query': {'match_all': {}}}
        count = self.es.count(index=index, body=query_rule)['count']
        if count < 1:
            return pd.DataFrame()
        query_rule['_source'] = heads if heads is not None else []
        anl = helpers.scan(self.es, query=query_rule, index=index, **kwargs)
        df = pd.DataFrame(self.get_source(anl, show_progress=show_progress, count=count)).set_index('_id')
        if infer_dtype:
            dtype = self.infer_dtype(index, df.columns.values)
        if dtype is not None and len(dtype):
            try:
                df = df.astype(dtype)
            except:
                pass
        return df

    @staticmethod
    def serialize(row, columns, use_pandas_json, iso_dates):
        if use_pandas_json:
            return pjson.dumps(dict(NoNanDict(zip(columns, row))), iso_dates=iso_dates)
        return dict(NoNanDict(zip(columns, [None if np.all(pd.isna(r)) else r for r in row])))

    @staticmethod
    def gen_action(**kwargs):
        return {k: v for k, v in kwargs.items() if v not in [None, np.nan, np.NINF, np.inf]}

    def rec_to_actions(self, df, index, doc_type=None, use_index=False, _op_type='index', use_pandas_json=False, date_format='iso', show_progress=True):
        # if show_progress:
        #     bar = progressbar.ProgressBar(max_value=df.shape[0])
        # else:
        #     bar = BarNothing()
        columns = df.columns.tolist()
        iso_dates = date_format == 'iso'
        if use_index and (_op_type in ['create', 'index']):
            for i, row in enumerate(df.itertuples(name=None, index=use_index)):
                # bar.update(i)
                _id = row[0]
                record = self.serialize(row[1:], columns, use_pandas_json, iso_dates)
                action = self.gen_action(_op_type=_op_type, _index=index, _type=doc_type, _id=_id, _source=record)
                yield action
        elif (not use_index) and (_op_type == 'index'):
            for i, row in enumerate(df.itertuples(name=None, index=use_index)):
                # bar.update(i)
                record = self.serialize(row, columns, use_pandas_json, iso_dates)
                action = self.gen_action(_op_type=_op_type, _index=index, _type=doc_type, _source=record)
                yield action
        elif _op_type == 'update':
            for i, row in enumerate(df.itertuples(name=None, index=True)):
                # bar.update(i)
                _id = row[0]
                record = self.serialize(row[1:], columns, False, iso_dates)
                action = self.gen_action(_op_type=_op_type, _index=index, _type=doc_type, _id=_id, doc=record)
                yield action
        elif _op_type == 'delete':
            for i, _id in enumerate(df.index.values.tolist()):
                # bar.update(i)
                action = self.gen_action(_op_type=_op_type, _index=index, _type=doc_type, _id=_id)
                yield action
        else:
            raise Exception('[%s] action with %s using index not supported' % (_op_type, '' if use_index else 'not'))

    def init_es_tmpl(self, df, doc_type, delete=False, index_patterns=None, **kwargs):
        '''

        :param df: pd.DataFrame
        :param doc_type: str, name of doc_type
        :param delete: bool, if True, delete existed template
        :param index_patterns: list, default None, [doc_type*]
        :param kwargs: kwargs for template settings,
               example: number_of_shards, number_of_replicas, refresh_interval
        :return:
        '''
        tmpl_exits = self.es.indices.exists_template(name=doc_type)
        if tmpl_exits and (not delete):
            return
        if index_patterns is None:
            index_patterns = ['%s*' % doc_type]
        columns_body = {}

        if isinstance(df, pd.DataFrame):
            iter_dict = df.dtypes.to_dict()
        elif isinstance(df, dict):
            iter_dict = df
        else:
            raise Exception('init tmpl type is error, only accept DataFrame or dict of head with type mapping')
        for key, data_type in iter_dict.items():
            type_str = getattr(data_type, 'name', data_type).lower()
            if 'int' in type_str:
                columns_body[key] = {'type': 'long'}
            elif 'datetime' in type_str:
                columns_body[key] = {'type': 'date'}
            elif 'float' in type_str:
                columns_body[key] = {'type': 'float'}
            else:
                columns_body[key] = {'type': 'keyword', 'ignore_above': '256'}

        tmpl = {
            'index_patterns': index_patterns,
            'settings': {**kwargs}
        }
        if self.es_version[0] > 6:
            tmpl['mappings'] = {'properties': columns_body}
        elif self.es_version[0] > 5:
            tmpl['mappings'] = {'_doc': {'properties': columns_body}}
        else:
            tmpl['mappings'] = {'_default_': {'properties': columns_body}}
        if tmpl_exits and delete:
            self.es.indices.delete_template(name=doc_type)
            print('Delete and put template: %s' % doc_type)
        self.es.indices.put_template(name=doc_type, body=tmpl)
        print('New template %s added' % doc_type)

#
# class BarNothing(object):
#     def update(self, arg):
#         pass