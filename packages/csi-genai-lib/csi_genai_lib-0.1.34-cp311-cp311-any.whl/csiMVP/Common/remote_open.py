# ##################################################################################################
#  Copyright (c) 2022.    Caber Systems, Inc.                                                      #
#  All rights reserved.                                                                            #
#                                                                                                  #
#  CABER SYSTEMS CONFIDENTIAL SOURCE CODE                                                          #
#  No license is granted to use, copy, or share this software outside of Caber Systems, Inc.       #
#                                                                                                  #
#  Filename:  remote_open.py                                                                       #
#  Authors:  Rob Quiros <rob@caber.com>  rlq                                                       #
# ##################################################################################################


"""
This module attempts to abstract away the complexities of dealing with multiple types of AWS_S3-like object
store services.  Even though https://pypi.org/project/smart-open/ gives us the ability to read and write objects
and files from many types of sources, there are source-dependent quirks that have to be dealt with.

For example, although Min.io is supposed to be completely S3 compatible, it requires a username:password
combo to be passed and the S3 client must have the URL of the Minio host defined.

The other quirk is that for use internal to Caber services we can use AWS_S3 or another source, and customers
can define multiple types of hosts simultaneously.  All of these we keep track of here.

First thing we need to do is patch smart-open's parse_uri function so that it recognizes our schemes that
look like

    pointer<CFG.token>bucket/prefix    where pointer=pointer to Object_Source config

instead of

    scheme://bucket/prefix

"""

from time import sleep
from urllib.parse import urlsplit
from pathlib import Path, PurePath, PosixPath
from fnmatch import fnmatch
from smart_open import open as smart_open_open

from botocore.exceptions import ClientError, EndpointConnectionError
from botocore.parsers import ResponseParserError
from urllib3.exceptions import NewConnectionError

from csiMVP.Common.init import CFG, post_status_message
from csiMVP.Toolbox.retry import retry
from csiMVP.Toolbox.goodies import first_valid, normalize_host_config, fnfilter_list
from csiMVP.Toolbox.aws_init import boto3, boto3config, AWS, check_s3_name, AWS_S3_NAME, new_aws_client, S3C


# ############# INCLUDE HERE THE NAMES OF TESTED OBJECT STORE TYPES ################ #
#   These form the possible choices for:
#          CFG.D['Object_Sources'][<host-name>]['type']
#          CFG.D["Dependencies"]["shared-storage"]["targets"][<host-name>]['type']
#
SupportedS3likeStoreTypes = ['minio']
cs3idp = f"cs3aws"
# ################################################################################## #


default_configs = {AWS_S3_NAME: {"type": "s3",
                                 "url": "https://s3.amazonaws.com",
                                 "smartOpenPfx": "s3://",
                                 "client_type": "boto3.s3",
                                 "client": None,
                                 "transport_params": None
                                 },
                        "minio": {"type": "minio",
                                  "url": "http://csi-dep-minio:9000",
                                  "smartOpenPfx": "s3://",
                                  "region": "",
                                  "accessKey": "<user>",
                                  "secretKey": "<psswd>",
                                  "client_type": "boto3.s3",
                                  "client": None,
                                  "transport_params": {"client": None}
                                  }
                   }


# TODO: Implement object versions, Implement decryption for encrypted objects


def _build_map(host='*', port='*', bkt_lst=None, id_prefix=''):
    if not id_prefix:
        id_prefix = CFG.D["Dependencies"]["shared-storage"].get("prefix", "gss")
    if not bkt_lst:
        bkt_lst = ['*']
    elif isinstance(bkt_lst, str):
        bkt_lst = [bkt_lst]

    if ':' in host:
        hs = host.split(':')
        host = hs[0]
        if hs[1]:
            port = hs[1]

    # Make an entry in the host map for each bucket with hostname with and without the port
    # The keys in the map will be fnmatch patterns so the lookup can take a wider variety of
    # imputs.  For example: looking up 'http://myhost:80/mybucket/someobject/somewhere'
    # when the hostMap key is '*myhost*mybucket*' will match.

    # If a port is specified, then we are saying port must be used to match.  This would only
    # be required in the case of two storage sources on the same host but with different ports.
    # Here we set up a exact match list to see if we've put the key in before.  We enter patterns
    # (emap) potentially with wildcards in the check_overlaps list, but compare them against
    # values (chke) that have wildcards replaces by ' '.
    emap = [f"{host}:{port}:{c}:{id_prefix}" for c in bkt_lst]
    chke = [f"{host}:{port}:{c}:*" for c in bkt_lst]

    if CFG.D['Object_Sources'].get('check_overlaps'):
        check = fnfilter_list(chke, CFG.D['Object_Sources']['check_overlaps'])
        if check and [c for c in check if c.split(':')[-1] != id_prefix]:
            raise ValueError("We've already inserted a storage host item that matches")
        else:
            CFG.D['Object_Sources']['check_overlaps'].extend(emap)
    else:
        CFG.D['Object_Sources'].update({'check_overlaps': emap})

    hmap = [f"*{host}*{port}*{c}*" for c in bkt_lst]

    if CFG.D['Object_Sources'].get('hostMap'):
        CFG.D['Object_Sources']['hostMap'].update({m: id_prefix for m in hmap})
    else:
        CFG.D["Object_Sources"].update({"hostMap": {m: id_prefix for m in hmap}})

    return


def _lower_key_and_get_config(tcfg: dict, trgt: str):
    if check_s3_name(trgt) == AWS_S3_NAME:
        scfg = tcfg.pop(trgt)
        tcfg.update({AWS_S3_NAME: scfg})
        trgt = AWS_S3_NAME
    elif trgt != trgt.lower():
        scfg = tcfg.pop(trgt)
        tcfg.update({trgt.lower(): scfg})
        trgt = trgt.lower()

    if isinstance(tcfg, dict) and isinstance(tcfg.get(trgt), dict):
        scfg = normalize_host_config(tcfg[trgt], trgt, svc_domain=CFG.svc_domain)
    else:
        print(f"[ERROR] For target {trgt} tcfg[target] is not of type dict")
        scfg = {}
    return scfg, trgt


def _extract_bucket_list(bkts, addin=None) -> list:
    out = []
    if isinstance(bkts, list):
        for b in bkts:
            if isinstance(b, str):
                out.append(b)
            elif isinstance(b, dict):
                out.extend(list(b.keys()))
    elif isinstance(bkts, dict):
        out.extend(list(bkts.keys()))
    elif isinstance(bkts, str):
        out = [bkts]
    if isinstance(addin, str):
        out.append(addin)
    elif isinstance(addin, list):
        out.extend(addin)
    out = set(out)
    out.discard('')
    out.discard(None)
    return list(out)


def _put_bkt_versioning(sclnt, bkt, minio=False):
    '''
    Turn object versioning on in customer bucket, deal with error, retry if necessary.
    TODO: this function should be performed by Terraform in the future so that state is properly maintained.
    :param sclnt: The boto3.client("s3")
    :param bkt: The name of the bucket to put versioning on
    :return: True if operation succeeds.
    '''
    n = 10
    while n > 0:
        n -= 1
        try:
            if minio:
                response = sclnt.put_bucket_versioning(Bucket=bkt,
                                VersioningConfiguration={'MFADelete': 'Disabled', 'Status': 'Enabled'})
            else:  # AWS S3
                response = sclnt.put_bucket_versioning(Bucket=bkt, ChecksumAlgorithm='SHA256',
                                VersioningConfiguration={'MFADelete': 'Disabled', 'Status': 'Enabled'})
        except ClientError as err:
            e = repr(err).split("botocore.exceptions.ClientError: An error occurred (", 1)[-1]
            e = e[:e.find(")")]
            print(f"[WARNING] Boto3 ClientError ({e}) while tyring to set versioning on bucket '{bkt}'")
            if n > 0:
                print(f"[DEBUG] Retrying in 5 sec")
                sleep(5)
        else:
            print(f"[INFO] Enabled versioning on customer bucket {bkt}")
            return True
    return False


def validate_all_store_configs(which='all', force=False):
    """
    Validates the configuration for remote storage in the raw config file and test that we can read and, in
    the case of Caber global shared storage, write to the storage host. Called whenever remote_open is imported.

    :param which: which storage configuration to validate. Default is all
    :param force: Force revalidation of configs if True
    :return: None
    """

    rev_map = {cs3idp: AWS_S3_NAME}
    new_sources = {}

    if not CFG.D.get("Object_Sources", {}):
        CFG.D.update({"Object_Sources": {"revMap": rev_map}})
    elif not CFG.D.get("Object_Sources", {}).get("revMap", ''):
        CFG.D["Object_Sources"].update({"revMap": rev_map})
    else:
        CFG.D["Object_Sources"]["revMap"].update(rev_map)

    # The id_prefix for Caber shared store is always the same: 'gss' for global shared store
    # Note that this default cannot start with 'c' as customer stores will start with that.

    # RANT: Using '://' as the separator between the 'scheme' and 'host' as with urls creates problems
    # when appending the prefix to other strings.  It's hard to ensure there are the proper number of /'s
    # without stripping and re-adding the slashes, and special case-ing file:///directory that always must
    # have three slashes not two. So, internally we will always use the unicode Caber-token (CFG.token) to
    # represent the '://'

    # ---------- START Validating global storage source
    if which == 'all' or which.startswith('g'):

        target = CFG.D["Dependencies"]["shared-storage"]["useTarget"]
        scfg, target = _lower_key_and_get_config(CFG.D["Dependencies"]["shared-storage"].get("targets") or {}, target)
        CFG.D["Dependencies"]["shared-storage"].update({"useTarget": target})

        if not target:
            return False

        print(f"{target.upper()}: Validating configuration (Caber shared storage)")

        # There must be a shared storage bucket name configured
        buckets = CFG.D["Dependencies"]["shared-storage"].get("buckets", '') or ''
        csib = first_valid(CFG.bucket, scfg.get("csiBucket"), CFG.G.get("csiBucket"))
        scfg.update({"csiBucket": csib})
        buckets = _extract_bucket_list(buckets, csib)
        scfg.update({"buckets": buckets})

        idp = CFG.D["Dependencies"]["shared-storage"].get("prefix", "gss")
        scfg.update({"id_prefix": f"{idp}{CFG.token}"})
        # Todo: Support different client types in the future.
        scfg.update({"client_type": f"boto3.s3"})

        _build_map(scfg.get('host', ''), '*', buckets, idp)
        # _build_map(scfg.get('host', ''), scfg.get('port', ''), buckets, idp)

        # Update the storage source config and instantiate the client. Update of revMap must happen
        # before the call to get object store client.
        CFG.D["Object_Sources"]["revMap"].update({idp: target})
        get_object_store_client()

    # ---------- Done Validating global storage source

    # ---------- START Validating customer storage sources
    if which == 'all' or which.startswith('c'):

        oss = [s for s in CFG.D["Object_Sources"].keys() if s not in ["revMap", "doc", "Buckets", 'hostMap', 'check_overlaps']]
        all_customer_buckets = CFG.D["Object_Sources"].get("Buckets", [])

        # below is to check in CFG.D['ApiMap'] to see if any of the sources are being proxied by Caber
        # and, if so, create a configuration for them.
        tap_name = CFG.G["caberModuleContainerNames"]["API_Tap"]
        if isinstance(tap_name, dict):
            tap_name = tap_name.get("host", "")

        tap_name = tap_name.lower()
        taps = {f"{tap_name}:{urlsplit(k).port}": urlsplit(v.get("upstrm", "")).hostname
                for k, v in CFG.D["ApiMap"].items()
                if k.lower().count("self") or k.lower().count(tap_name)}

        new_sources = {}
        for src in oss:
            print(f"Validating customer object source configuration '{src}'")
            scfg, src = _lower_key_and_get_config(CFG.D["Object_Sources"], src)

            buckets = _extract_bucket_list(scfg.get('buckets'))
            all_customer_buckets.extend(buckets)

            if src == AWS_S3_NAME:
                idp = cs3idp
                # new_sources.update({AWS_S3_NAME: default_configs.get(AWS_S3_NAME, {})})

            else:
                idp = src.lower()
                for ch in "/!@#$%^&*()}{_-=+[]<>.,?~`\\|:;'\"":
                    idp = idp.replace(ch, '')
                idp = f"c{idp}"
                if len(idp) > 10:
                    idp = idp[:10]

            scfg.update({"id_prefix": f"{idp}{CFG.token}"})
            scfg.update({"client_type": "boto3.s3"})

            _build_map(scfg.get('host', ''), '*', buckets, idp)

            # Now add any api-tap ports to the list if we happen to be proxying the API to the storage
            # system as we are doing in the demo.
            if scfg.get('host', ''):
                tap_match = [k for k, v in taps.items() if v and v in scfg.get('host', '')]
                for tm in tap_match:
                    _build_map(tm, '', buckets, idp)

            # Update the storage source config and instantiate the client. Update of revMap must happen
            # before the call to get object store client.
            CFG.D["Object_Sources"]['revMap'].update({idp: src})
            sclnt = get_object_store_client(idp)

            # We need bucket versioning to track  data in objects that may be written to multiple times before
            # we get notified of the first write to them.  Here we need to check if bucket versioning is enabled
            # on each bucket and, if it is not, enable it if configuation allows.
            # Minio does not support versioning of objects in 'FileSystem' mode -- one Minio instance and
            # one local disk.  But there is no way to find out if it's in FileSystem mode except try and
            # get the exception.
            envers = scfg.get("enableBktVersioning", False)
            for bkt in buckets:
                try:
                    vers = sclnt.get_bucket_versioning(Bucket=bkt)
                except ClientError as err:
                    print(f"[WARNING] Checking versioning on bucket '{bkt}':  Bucket does not exist")
                else:
                    if envers and (not vers or isinstance(vers, dict) and vers.get('Status', '') != 'Enabled'):
                        response = _put_bkt_versioning(sclnt, bkt, minio=(src == 'minio'))

        CFG.D["Object_Sources"].update({"Buckets": list(set(all_customer_buckets))})

    # ---------- DONE Validating customer storage sources

    return True


class caber_patch_pathlib(object):
    """
    Replace `Path.open` with `remote_open.open`
    Directly from https://github.com/RaRe-Technologies/smart_open/blob/develop/smart_open/smart_open_lib.py
    """

    def __init__(self):
        self.old_impl = _caber_patch_pathlib(ropen)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        _caber_patch_pathlib(self.old_impl)


def _caber_patch_pathlib(func):
    """Replace `Path.open` with `func`"""
    old_impl = Path.open
    Path.open = func
    return old_impl


def ropen(*args, **kwargs):

    """
    uri,                                    positional arg
    mode = 'r',                             positional or keyword arg
    buffering = -1,                         positional or keyword arg
    encoding = None,                        positional or keyword arg
    errors = None,                          positional or keyword arg
    newline = None,                         positional or keyword arg
    closefd = True,                         positional or keyword arg
    opener = None,                          positional or keyword arg
    compression = (infer),                  keyword arg
    transport_params = None                 keyword arg
    """

    transport_params = None

    if len(args):
        args = list(args)
        args[0], transport_params = caber_parse_uri(args[0])

    if transport_params is None:
        transport_params = kwargs.get("transport_params", None)
    if transport_params is not None:
        kwargs.update({"transport_params": transport_params})

    try:
        ret = smart_open_open(*args, **kwargs)
    except ValueError as err:
        print(f"[ERROR] args = {args}")
        print(f"[ERROR] kwargs = {kwargs}")

        if str(err).count('ExpiredToken'):
            print(f"[ERROR] Got ValueError->ExpiredToken Exiting")
            post_status_message(stage="4.0", category="warning",
                                message=f"Expired auth token. Shutting down",
                                status="red")
            S3C.list_buckets()
            # exit(0)

        print(f"[WARNING] Got ValueError trying to open '{args[0]}': {err}")
        print(f"bucket = {CFG.bucket}")
        return
    except ClientError as err:
        print(f"[WARNING] Got Boto3 ClientError trying to open '{args[0]}': {err}")
        return
    # except (FileExistsError, FileNotFoundError, OSError) as err:
    #     print(f"[WARNING] Got OSError trying to open '{args[0]}': {err}")
    #     return
    else:
        return ret


def caber_parse_uri(uri_as_string):
    """
    Parse a Caber object remote identifier (CORI) and return the corresponding smart-open URI and transport params.

    We want the main code to simply call ropen(remote_file), from the class definition below, and get the remote
    file or object from whichever object or file source it came from.  We do this by prefixing the remote file
    with an identifier representing the configuration parameters for the object source.  The configuration
    parameters for each source are kept in CFG.D['Object_Sources'], or CFG.D["Dependencies"]["shared-storage"]["targets"] for
    the object store source that Caber services use to pass objects among themselves.

    When ENV_Manager processes the configuration for each source, it creates an identifier prefix (id_prefix)
    for the source and then creates a reverse mapping of prefix to source in CFG.D['Object_Sources']['revMap']

    Each source's configuration looks like:

    source_config = {"type": "s3",
                      "url": "https://s3.amazonaws.com",
                      "smartOpenPfx": "s3://",
                      "id_prefix": "s3aws",
                      "client": <object reference of client used to access the source>,
                      "transport_params": None}

    So here we strip the id_prefix from the incoming uri_as_string, lookup what source_config it belongs to,
    then, using the parameters in the source_config, call smart_open to read or write the object.  In the case
    of the default configuration, for example, the Caber shared store, the incoming uri_as_string would
    look like:
               'gss⋊⋉csi-mvp-master/x/y/z

    :param uri_as_string: Identifier for the object to access in the form <id_prefix><CFG.token><bucket>/<object_key>.
    :return: Tuple of URI with smart_open appropriate prefix, and transport parameters if needed.
    """

    # If given a uri_as_string without a Caber id_prefix, then just return it.
    if isinstance(uri_as_string, str):
        if uri_as_string.lower().startswith(f"s3://{CFG.bucket}".lower()):
            uri_as_string = uri_as_string.lower().replace("s3://", f"{CFG.sspfx}{CFG.token}")
        if not uri_as_string.count(CFG.token):
            return uri_as_string, None
    elif isinstance(uri_as_string, PosixPath):
        if not uri_as_string.parts[0].count(CFG.token):
            if uri_as_string.parts[0].count(':'):
                if uri_as_string.parts[0].startswith('file'):
                    uri_as_string = str(uri_as_string).replace(':/', ':///')
                else:
                    uri_as_string = str(uri_as_string).replace(':/', '://')
            else:
                uri_as_string = str(uri_as_string)
            return uri_as_string, None
        else:
            uri_as_string = str(uri_as_string)

    scfg = None
    if not CFG.D['Object_Sources'].get('revMap', {}):
        validated = validate_all_store_configs()
    rev_map = CFG.D['Object_Sources'].get('revMap', {})

    uri_split = uri_as_string.split(CFG.token, 1)

    target = rev_map.get(uri_split[0], None)
    if target is None:
        raise ValueError(f"[caber_parse_uri] Processsing URI input '{uri_as_string}':\n"
                         f"\tNo object-store source configuration exists for target {target}")

    # If the first letter of the identifier is 'g' then this is the global-shared source
    if uri_split[0][0].lower() == 'g':
        scfg = CFG.D["Dependencies"]["shared-storage"]["targets"].get(target) or {}
    elif uri_split[0][0].lower() == 'c':
        scfg = CFG.D['Object_Sources'].get(target) or {}
    else:
        raise ValueError(f"Malformed Caber Object_Source identifier prefix '{uri_split[0]}'.  "
                         f"The first letter of the identifier prefix must be either 'g' "
                         f"for the global shared object source, or 'c' for customer object sources")

    # Here get the relevant parameters from scfg to modify open
    scheme = scfg.get("smartOpenPfx", "file://")

    uri_as_string = uri_split[1]
    object_version = ""
    if uri_as_string.count(CFG.G["objVersSeparator"]):
        uri_as_string, object_version = uri_as_string.rsplit(CFG.G["objVersSeparator"], 1)

    uri_as_string = f"{scheme}{uri_as_string}"
    transport_params = scfg.get("transport_params") or {}

    # print(f"[DEBUG] Remote_Open uri_as_string is: {uri_as_string}")
    # print(f"[DEBUG] Remote_Open scfg is: {scfg}")

    if "client" not in transport_params and scfg.get("client", None) is not None:
        # print(f"[DEBUG] Adding client to transport_params")
        transport_params.update({"client": scfg["client"]})

    if object_version:
        if not transport_params:
            transport_params = {'version_id': object_version}
        else:
            transport_params.update({'version_id': object_version})

    return uri_as_string, transport_params


def pull_store_config(src_config='', bucket=''):
    """
    Returns the storage configuration for Caber Global Storage Source or one of the customer's
    configured object sources.

    If called with no arguments returns the global storage source configuration.
    Else checks to see if the host name is a CORI id_prefix
        if not, it looks up the CORI id_prefix using CFG.D["Object_Sources"]["hostMap"][(host + bucket)]
    to get the storage source id_prefix.
    Lastly, if the hostname is our own api-tap, then look up in the ApiMap what the upstream host is.

    Gets the store config based on 'global' for internal use
    or 'object_sources' for customer defined object sources

    If no source config given, the Global source is implied.

    Easy to get confused with teh CORI related translators in filenames.py

    """

    scfg = {}
    where = ''

    if not src_config or src_config.startswith(CFG.sspfx) or bucket == CFG.bucket:
        target = CFG.D["Dependencies"]["shared-storage"]["useTarget"]
        scfg = CFG.D["Dependencies"]["shared-storage"]["targets"].get(target) or {}
        where = CFG.sspfx
        if scfg is None:
            raise ValueError(f"[pull_store_config] Processsing src_config '{src_config}':\n"
                             f"\tGlobal storage source target {target}: Configuration does not exist")
        else:
            return scfg, where

    elif CFG.token in src_config:
        src_config = src_config.split(CFG.token)[0]

    elif src_config == AWS_S3_NAME:
        src_config = cs3idp

    loc = CFG.D["Object_Sources"].get("revMap", {}).get(src_config, '')

    if not loc:
        if src_config and bucket and bucket not in src_config:
            src_config = src_config + ':' + bucket
            bucket = ''

        where_list = [v for k, v in CFG.D["Object_Sources"].get("hostMap", {}).items() if fnmatch(src_config, k)]
        for where in where_list:
            loc = CFG.D["Object_Sources"].get("revMap", {}).get(where, '')
            if loc:
                break

    else:
        where = src_config

    if loc in CFG.D["Object_Sources"].keys():
        scfg = CFG.D["Object_Sources"][loc]
        return scfg, where

    else:
        if bucket:
            print(f'[WARNING] Configuration does not exist for object storage source {src_config}:{bucket} -> {where} ')
        return {}, None


def update_store_config(src_config=None, new_config=None):
    """
    Gets the store config based on 'global' for internal use
    or 'object_sources' for customer defined object sources

    If no source config given, the Global source is implied.
    """

    if new_config is None:
        return

    if not src_config or src_config.startswith('g'):
        target = CFG.D["Dependencies"]["shared-storage"]["useTarget"]
        CFG.D["Dependencies"]["shared-storage"]["targets"].update({target: new_config})

    else:
        src_config = src_config.split(CFG.token)[0]
        if src_config in CFG.D["Object_Sources"].get("revMap", {}).keys():
            src_config = CFG.D["Object_Sources"]["revMap"][src_config]

        if src_config in CFG.D["Object_Sources"].keys():
            CFG.D["Object_Sources"].update({src_config: new_config})

    return


# @retry(RuntimeError, total_tries=15, initial_wait=10, backoff_factor=1)
def _test_store_client(scfg, url, obst_client):
    errs = []
    stype = scfg.get('type', '')

    try:
        ctest = obst_client.list_buckets()

    except (NewConnectionError, EndpointConnectionError, ResponseParserError, ClientError) as err:
        print(f"[WARNING] {stype.capitalize()} host '{url}': {err}")
        return False
        # errs.append(f"[WARNING] {stype.capitalize()} host '{url}': {err}")
        # raise RuntimeError(f"[WARNING] {stype.capitalize()} host '{url}': retrying connection")
    else:
        return True


def match_bucket_in_source(host='', bucket='', mod='', objuct='', version=''):
    """
    Each Customer source in Object_sources

    :param host: The name of the customer source in the config
    :param bucket: The name of the bucket to test against
    :param mod: Module name of CORI - not used
    :param objuct: The object to check
    :return: True if the object in the bucket matches the config
    """

    # ENV_Manager creates a list of all buckets in the customer's configuration as a first-pass filter.
    # If there are buckets configured then they can be fnmatch patterns, so we need to check for
    # bucket matching any of the Bucket patterns.
    if not bucket:
        return False

    if not host and CFG.token in bucket:
        bs = bucket.split(CFG.token)
        host = bs[0]
        bucket = bs[1]

    first_pass_filter = any([pat for pat in CFG.D["Object_Sources"].get("Buckets", []) if fnmatch(bucket, pat)])
    if not first_pass_filter:
        return False
    elif not host and first_pass_filter:
        return True

    scfg, _ = pull_store_config(host, bucket)
    configured_buckets = scfg.get("buckets", {})
    if not configured_buckets:
        return False

    matched_bucket_prefixes = []
    # The first matching pattern wins.
    for cbkt in configured_buckets:
        bkt = list(cbkt.keys())[0]
        if fnmatch(bucket, bkt):
            matched_bucket_prefixes = cbkt[bkt].get("prefixes", [])
            break

    # Each configured bucket for a source can also have prefix patterns to match.  Even if no prefix is
    # supplied in the argument, we can still check to see if there is a wildcard match '*'.  If so, then
    # even a null prefix will match.
    #
    #        "buckets": {
    #          "newco-docs": {"prefixes": ["urn:oid:*"]} },
    #          "newco-shared": {"prefixes": ["*"]} }
    #        }
    #
    if matched_bucket_prefixes:
        if not objuct:
            # We found the bucket specified in the source but a prefix was not specified so return true
            return True
        if any([pat for pat in matched_bucket_prefixes if fnmatch(objuct, pat)]):
            return True

    return False


def create_new_bucket(new_bkt, src_config=None):
    """
    Create a new bucket in the specified object store source.  If the source is a volume then a
    directory will be created instead.

    :param new_bkt: Name of the bucket to create
    :param src_config: Creating buckets in any source other than the global storage source is for test and debugging only.
    We should NEVER create buckets in sources owned by the customer.
    :return: bucket name 'new_bkt' if sucessful, None otherwise
    """
    obj_source, where = pull_store_config()

    if obj_source.get('type', None) in ['file', 'local', 'volume']:
        bkt_path = PurePath(obj_source.get('directory', Path.home()), new_bkt)
        pbp = Path(bkt_path)
        if not pbp.exists():
            pbp.mkdir(mode=obj_source.get("mode", 754), parents=True)
            print(f"Created local directory: {bkt_path.as_uri()}")
        return bkt_path.as_uri()

    obst_client = obj_source.get('client', None)
    if not obst_client:
        return

    try:
        evb = obst_client.head_bucket(Bucket=new_bkt)
    except ClientError as err:
        if src_config == AWS_S3_NAME:
            response = obst_client.create_bucket(Bucket=new_bkt, ACL='private',
                                                 CreateBucketConfiguration={'LocationConstraint': AWS.region_name},
                                                 ObjectLockEnabledForBucket=False,
                                                 ObjectOwnership='BucketOwnerEnforced')
        else:
            response = obst_client.create_bucket(Bucket=new_bkt, ACL='private',
                                                 CreateBucketConfiguration={'LocationConstraint': AWS.region_name},
                                                 ObjectLockEnabledForBucket=False,
                                                 ObjectOwnership='BucketOwnerEnforced')

        waiter = obst_client.get_waiter('bucket_exists')
        try:
            waiter.wait(Bucket=new_bkt)
        except Exception as err:
            print(f"[CONFIG ERROR] In config: {err}")
            return
        print(f"Created new bucket '{new_bkt}' in {where} ({obj_source.get('url', '?')}) ")
    return new_bkt


@retry(ConnectionError, total_tries=15, initial_wait=10, backoff_factor=1)
def get_object_store_client(src_config=None):
    """
    Returns client only if we can connect to the source_name and the bucket is in the source_name and configured
    The configurations for the storage source targets are keyed by the hostname of the target. The hostname for
    AWS S3 is always 's3.amazonaws.com'.

    :param src_config: If no source config given, the Global source is implied.
            Else name of config in 'object_sources' for customer defined object sources
    :return: client object for given source config
    """

    scfg, where = pull_store_config(src_config)
    if type(scfg.get("client", None)).__qualname__ == 'S3':
        return scfg['client']

    adv_config = boto3config(s3={'addressing_style': 'path'},
                             user_agent=str(CFG.user_agent),
                             connect_timeout=7,
                             read_timeout=15)

    host_type = scfg.get('type', '')

    if check_s3_name(host_type) == AWS_S3_NAME:

        # Creating the client always succeeds so long as the boto3config parameters are of the correct type
        obst_client = new_aws_client('s3', config=adv_config)
        scfg.update({"client": obst_client})

        if not _test_store_client(scfg, host_type, obst_client):
            raise ConnectionError(f"Failed to connect to {host_type} host")

        for k in set(default_configs[AWS_S3_NAME].keys()).difference(scfg.keys()):
            scfg.update({k: default_configs[AWS_S3_NAME][k]})

    elif host_type.lower() in SupportedS3likeStoreTypes:
        # A non-S3 host without a url is an error since the url is needed to set up the client
        urls = first_valid(scfg.get('url'), scfg.get('urls'), oftype='any')

        if urls is None:
            scfg.update({'client': False})
            print(f"[ERROR] In config '{where}': No URL(s) configured for {host_type} Host")
            return scfg

        if isinstance(urls, str):
            urls = [urls]

        # If no client, then set one up for each URL in the URL list and quit when we find one that works
        if scfg.get('client', None) is None or scfg.get('client', '') == 'retry':
            for url in urls:
                # Creating the client always succeeds so long as the boto3config parameters are of the correct type
                obst_client = boto3.client('s3', endpoint_url=url,
                                           use_ssl=scfg.get('use_ssl', False),
                                           aws_access_key_id=scfg.get('accessKey', ''),
                                           aws_secret_access_key=scfg.get('secretKey', ''),
                                           region_name=scfg.get('region', ''),
                                           config=adv_config)

                if _test_store_client(scfg, url, obst_client):
                    scfg.update({'client': obst_client})
                    scfg.update({'url': url})
                    print(f"Instantiated {scfg.get('client_type', 'default')} client for {host_type} host")

                    if host_type.lower() == 'minio':
                        # Need to get the minio HostId to match in the logs minio puts out
                        # Boto3 has a dependency on the python requests module
                        import requests
                        from requests_aws4auth import AWS4Auth
                        auth = AWS4Auth(scfg.get('accessKey', ''), scfg.get('secretKey', ''), scfg.get('region', ''), 's3')
                        rsp = requests.get(f"{scfg['url']}/minio/admin/v3/info", auth=auth)
                        minio_id = rsp.json().get('HostId', '')
                        _build_map(minio_id, '*', _extract_bucket_list(scfg.get("buckets")),
                                   scfg.get("id_prefix").split(CFG.token)[0])
                    break

            if not scfg.get('client', None):
                raise ConnectionError(f"Failed to connect to {host_type} host")

        # For Smart-Open, all S3-like object stores get the s3:// prefix and client in the transport params
        scfg.update({"smartOpenPfx": "s3://"})
        scfg.update({"transport_params": {"client": scfg['client']}})

    elif host_type in ['local', 'file', 'volume']:
        scfg.update({"smartOpenPfx": "file://"})
        scfg.update({"client": "file"})

    update_store_config(src_config=src_config, new_config=scfg)
    return scfg.get('client', None)


# Keep at the end so all other iunctions are read in
# validate_all_store_configs()
_ = caber_patch_pathlib()

