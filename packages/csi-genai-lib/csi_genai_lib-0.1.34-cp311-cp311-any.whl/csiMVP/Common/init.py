# ##################################################################################################
#  Copyright (c) 2022.    Caber Systems, Inc.                                                      #
#  All rights reserved.                                                                            #
#                                                                                                  #
#  CABER SYSTEMS CONFIDENTIAL SOURCE CODE                                                          #
#  No license is granted to use, copy, or share this software outside of Caber Systems, Inc.       #
#                                                                                                  #
#  Filename:  init.py                                                                              #
#  Authors:  Rob Quiros <rob@caber.com>  rlq                                                       #
# ##################################################################################################

# import re below must be here since we use in an exec statement
# noinspection PyUnresolvedReferences
import re
import tempfile
import os
import time
import sysconfig
from socket import gethostname, gethostbyname, socket as sock, AF_INET, SOCK_DGRAM
import json
import uuid
import boto3
from botocore.exceptions import ClientError
from json import JSONDecodeError
from platform import python_version, platform
from urllib.parse import urlsplit
from datetime import datetime, timedelta, timezone
from smart_open import open
from pathlib import Path

from csiMVP.Common.tf_config_load import update_from_terraform
from csiMVP.Toolbox.json_encoder import extEncoder
from csiMVP.Toolbox.aws_init import S3C, AWS_S3_NAME
from csiMVP.Toolbox.supabase import post_status_to_supabase

try:
    from jsonmerge import merge
except ImportError:
    merge = None

try:
    from packaging import version
except ImportError:
    version = None

if not os.getenv("MODULE_STATUS_STAGE", ""):
    os.environ["MODULE_STATUS_STAGE"] = "0.0"

url_re_str = r"(?P<protocol>(?:https?|gs|hdfs|webhdfs|file|ssh|scp|sftp|s3):///?)?" \
             r"(?P<usr_pwd>(?:\S+(?::\S*)?@))?" \
             r"(?P<host>(?:(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-zA-Z\u00a1-\uffff0-9]+-?)*[a-zA-Z\u00a1-\uffff0-9]+))(?:\.(?:[a-zA-Z\u00a1-\uffff0-9]+-?)*[a-zA-Z\u00a1-\uffff0-9]+)*(?:\.(?:[a-zA-Z\u00a1-\uffff]{2,})))" \
             r"(?P<port>(?::\d{2,5}))?" \
             r"(?P<path>(?:(?:/[^\s]*)(?:[-a-zA-Z\u00a1-\uffff./\d_%]{1,255}))+)?" \
             r"(?P<query>(?:(?:(?:\?[^\s]*)(?:[-a-zA-Z\u00a1-\uffff@\[\]\{\}\(\)./\d:_%=]{3,}))" \
             r"(?:(?:\&[^\s]*)(?:[-a-zA-Z\u00a1-\uffff@\[\]\{\}\(\)./\d:_%=]{3,}))*))?"

beginning_of_time = datetime.fromisoformat("2000-01-01T00:00:01.011001+00:00")
end_of_time = datetime.fromisoformat("2199-01-01T00:00:01.011001+00:00")   # Pandas won't accept times past year 2262
use_color = True
progress_bar_last_update = 0


def post_status_message(stage='', message='', category='info', status='grey', progress_bar=0, extra=None):
    global progress_bar_last_update
    last_stage = os.getenv("MODULE_STATUS_STAGE", "0.0")

    # Increment the last value of the stage if not specified
    def _inc_minor_stage(istage):
        sls = istage.split('.')
        sls[-1] = str(int(sls[-1]) + 1)
        return '.'.join(sls)

    out_stage = stage if stage else _inc_minor_stage(last_stage)

    if version and version.parse(out_stage) <= version.parse(last_stage) and last_stage != "0.0":
        print(f"[WARNING] Attempt to post status message for stage {out_stage} after stage {last_stage}.")
        out_stage = _inc_minor_stage(last_stage)

    os.environ["MODULE_STATUS_STAGE"] = out_stage
    timestamp = datetime.now(tz=timezone.utc).isoformat()

    statmsg = {"category": category, "group": os.getenv("CSI_MODULE", "<module_not_set>"), "stage": out_stage}
    statmsg |= {"message": message} if message else {"message": "Status update"}
    statmsg |= {"status": status} if status else {"status": "pending"}
    statmsg |= {"extra": {"ipv4": get_primary_ip()}}
    statmsg |= {"deployment_id": os.getenv("CSI_DEPLOYMENT_ID")} if os.getenv("CSI_DEPLOYMENT_ID") else {}
    statmsg |= {"timestamp": timestamp}

    print(f"[STATUS] {statmsg}")

    # # NOTE: Apparently posting messages to the Cloudbuild log group casues Cloudbuild to
    # # continue running until it times out.  This is BAD.  So only post status to Supabase
    # post_status_to_cloudwatch(status)

    post_status_to_supabase(statmsg)

    os.environ["LAST_LOG_POST_TIME"] = timestamp
    return


def prep_shutdown(signum, frame):
    print(f'[INFO] Caught SIGTERM {signum}: Preparing to shut-down {frame}')
    status = "running" if "dashboard" in os.getenv("CSI_MODULE", "").lower() else "orange"
    post_status_message(stage="3.9", category="info", message=f"Scale-in event received", status="orange")
    os.environ.update({"CSI_CONTAINER_SHUTDOWN": "True"})
    # Finish any outstanding requests, then...


def check_shutdown(_exit=True):
    if os.environ.get("CSI_CONTAINER_SHUTDOWN", "False") == "True":
        if _exit:
            print(f'[INFO] Shutting down.')
            status = "exit-success" if "dashboard" in os.getenv("CSI_MODULE", "").lower() else "red"
            post_status_message(stage="4.0", category="warning",
                                message=f"Shutting down",
                                status="red")
            exit(0)
        return os.environ.get("CSI_CONTAINER_SHUTDOWN", "False")


def compile_regex_dict(r, default_compression_suffix='gz'):
    regex_dict = {}
    n = 0
    if not isinstance(r, dict):
        print("[WARNING] Regexes not formatted as a dictionary")
    else:
        r.update({"suffix_compressed": r"^.*\." + f"(gz$)?(gzip$)?(zip$)?(7z$)?(z$)?(zz$)?(br$)?({default_compression_suffix}$)?"})
        r.update({"null": 'a^'})    # Match nothing
        for name, rgx in r.items():
            if name == 'doc':
                continue
            n += 1
            # Thanks https://stackoverflow.com/questions/6752485/how-to-replace-a-double-backslash-with-a-single-backslash-in-python
            try:
                exec(f'global {name}_rgx_out; {name}_rgx_out = re.compile(rgx.encode().decode("unicode_escape").encode()); regex_dict.update({{"{name}": {name}_rgx_out}})',
                     globals(), {'rgx': rgx, 'regex_dict': regex_dict})
            except:
                # If a regex fails to compile, substitute for it a regex that will match nothing
                # so the ordering of the rest of the regexes is not messed up.
                print(f'[WARNING] Failed to compile regex {name} with {rgx}')
                exec(f'global {name}_rgx_out; {name}_rgx_out = re.compile(b"a^"); regex_dict.update({{"{name}": {name}_rgx_out}})',
                     globals(), {'rgx': rgx, 'regex_dict': regex_dict})
    return regex_dict


def get_platform():
    global use_color
    pf = 'Local'
    if os.environ.get("AWS_LAMBDA_RUNTIME_API"):
        pf = 'AWS.Lambda'
        use_color = False
    elif os.environ.get("AWS_EXECUTION_ENV"):
        pf = os.environ.get("AWS_EXECUTION_ENV").replace('_', '.')
        use_color = False
    elif os.environ.get("ECS_CONTAINER_METADATA_URI_V4") or os.environ.get("ECS_CONTAINER_METADATA_URI"):
        pf = 'AWS.ECS'
        use_color = False
    if Path("/.dockerenv").exists():
        pf += ".docker"
    pf += f".[{platform().split('-with')[0]}]"
    return pf


def make_test_dir(ldd):
    if not isinstance(ldd, (str, Path)):
        raise ValueError(f"Argument must be string or Path not {type(ldd)}")
    if isinstance(ldd, str):
        ldd = Path(ldd)
    if not ldd.exists():
        ldd.mkdir(mode=0o775, parents=True)
    ldd.joinpath('delete_me.test_only').write_text('delete_me.test_only')      # ALWAYS LOCAL - PATH OPEN
    ldd.joinpath('delete_me.test_only').unlink()                               # ALWAYS LOCAL - PATH OPEN
    return ldd


class csiLogging():
    mod = ''

    def __init__(self, MODULE):
        self.mod = MODULE


# class csiLogging(logging):
#     loglev = ''
#     logger = None
#
#     def __init__(self, MODULE):
#
#         loglev = CFG.me("logLevel", "INFO").upper()
#         if loglev == "VERBOSE":
#             loglev = "DEBUG"
#
#         super(csiLogging, logging).__init__(self)
#
#         numeric_level = getattr(self, CFG.me("logLevel", "INFO").upper(), None)
#         if not isinstance(numeric_level, int):
#             raise ValueError('Invalid log level: %s' % loglev)
#
#         self.basicConfig(level=numeric_level, format='%(asctime)s [%(levelname)s] %(message)s',
#                             datefmt='%m/%d %H:%M:%S', stream=sys.stdout)
#
#         self.logger = self.getLogger(MODULE)
#         # self.logger.setLevel(self.INFO)


def tclean(t):
    tc = t.ctime()
    stt = tc.split(' ')
    return ' '.join(stt[1:-1])


def scantree(inpath, depth=2):
    """Recursively yield DirEntry objects for given directory."""
    depth += inpath.count('/')
    for entry in os.scandir(inpath):
        if entry.is_dir(follow_symlinks=False) and entry.path.count('/') <= depth:
            try:
                yield from scantree(entry.path)  # see below for Python 2.x
            except PermissionError:
                yield entry
        else:
            yield entry


def merge_all_configs_in_folder(folder, bucket, user_agent=""):
    bootstrap_config_file = os.environ.get("CSI_BOOTSTRAP_CONFIG", '').replace('s3://', '', 1).split('/', 1)[-1]

    try:
        config_objects = S3C.list_objects_v2(Bucket=bucket, Prefix=folder).get("Contents", [])
    except ClientError as err:
        print(f"[WARNING] Merge-configs: Unable to list objects in bucket '{bucket}': {err}")
        return {}

    config_objects.sort(key=lambda x: x.get('LastModified', 0))

    object_contents = {}
    for key in [k.get('Key', '') for k in config_objects if k.get('Key', False)]:
        content = S3C.get_object(Bucket=bucket, Key=key).get('Body')
        if content is not None and content.readable():
            content = content.read()
            content = content.decode() if not isinstance(content, str) else content
            object_contents.update({key: content})

    try:
        merged_config = json.loads(object_contents.pop(bootstrap_config_file, ""))
    except JSONDecodeError:
        merged_config = {}

    for key, content in object_contents.items():
        try:
            next_config = json.loads(content)
        except JSONDecodeError:
            pass
        else:
            merged_config = merge(merged_config, next_config)

    return merged_config


def try_cf_read(path, file='', skip_test=False):
    cf = {}
    if isinstance(path, str):
        if not file or (file and (path.endswith(file) or path.endswith('.json'))):
            pf = path
        elif path.endswith('/'):
            pf = path + file
        else:
            pf = path + '/' + file
        try:
            # print(f'[DEBUG] try_cf_read: Attempting to get config file from: {pf}')
            with open(pf, 'r') as fi:      # USING NATIVE SMART_OPEN.OPEN
                cf = json.load(fi)
        except (OSError, FileNotFoundError, IsADirectoryError) as err:
            try:
                code = err.backend_error.response.get("Error", {}).get("Code", "")
                message = err.backend_error.response.get("Error", {}).get("Code", "")
                if code == 'InvalidAccessKeyId':
                    print(f'[FATAL ERROR] try_cf_read: {code}: {message}')
                    return None, f'FATAL ERROR (init.try_cf_read) {code}: {message}'
            except Exception:
                pass
            # print(f'[DEBUG] try_cf_read: Error trying to get config file: {err}')
            return None, '_'
        except json.JSONDecodeError:
            if not fi.closed: fi.close()
            print(f"[DEBUG] try_cf_read: Configuration file does not contain valid JSON")
            return None, 'j'
    elif isinstance(path, Path):
        fi = ''
        try:
            # print(f'Trying to get config file from: {str(path.joinpath(file).absolute())}')
            if path.joinpath(file).name and path.joinpath(file).exists():
                fi = path.joinpath(file).read_text()
            elif path.name and path.exists():
                fi = path.read_text()
            else:
                # print(f'[DEBUG] try_cf_read: No config file name or path specified.')
                return None, '_'
        except (OSError, FileNotFoundError, IsADirectoryError) as err:
            print(f'[DEBUG] try_cf_read: Error trying to get config file: {err}')
            return None, '_'
        try:
            cf = json.loads(fi)
        except json.JSONDecodeError:
            print(f"[ERROR] try_cf_read: Configuration file '{file}' does not contain valid JSON")
            return None, 'j'
    else:
        return None, '?'

    if not isinstance(cf, dict):
        print(f"[ERROR] try_cf_read: Configuration file empty")
        return None, '_'

    test = [cf.get("RKCQF", False), cf.get("GLOBAL", False), cf.get("ENV_Manager", False)]
    if all(test) or skip_test:
        return cf, 'Found'
    else:
        print(f"[ERROR] try_cf_read: Configuration file signature does not match")
        return None, 'i'


class Hues:
    use_color = True
    rst = "\u001b[0m" if use_color else ""
    fg = None
    bg = None

    def __init__(self):
        self.use_color = 'AWS' not in get_platform()
        self.fg = self.Colors(self, True)
        self.bg = self.Colors(self, False)

    class Colors:
        def __init__(self, outer_hue_instance, foreground_true_background_false=True):
            self.outer = outer_hue_instance
            self.code = "38" if foreground_true_background_false else "48"

        @property
        def blu(self):
            return f"\u001b[1m\u001b[{self.code};5;12m" if use_color else ""
        @property
        def grn(self):
            return f"\u001b[1m\u001b[{self.code};5;28m" if use_color else ""
        @property
        def ylw(self):
            return f"\u001b[1m\u001b[{self.code};5;226m" if use_color else ""
        @property
        def orn(self):
            return f"\u001b[1m\u001b[{self.code};5;208m" if use_color else ""
        @property
        def red(self):
            return f"\u001b[1m\u001b[{self.code};5;160m" if use_color else ""
        @property
        def pur(self):
            return f"\u001b[1m\u001b[{self.code};5;92m" if use_color else ""
        @property
        def cyn(self):
            return f"\u001b[1m\u001b[{self.code};5;51m" if use_color else ""
        @property
        def gry(self):
            return f"\u001b[1m\u001b[{self.code};5;251m" if use_color else ""
        @property
        def bwt(self):
            return f"\u001b[1m\u001b[{self.code};5;15m" if use_color else ""


Hue = Hues()


def get_primary_ip():
    try:
        # The AF_INET address family is used for IPv4.
        # SOCK_DGRAM is the socket type for UDP, which doesn't require an actual connection.
        # This combination avoids the need to actually create a network connection.
        with sock(AF_INET, SOCK_DGRAM) as s:
            # Connect to a remote server. The IP address does not need to be reachable.
            s.connect(("8.8.8.8", 80))
            # Get the IP address of the container
            ip = s.getsockname()[0]
            return ip
    except Exception as e:
        print(f"[ERROR] get_primary_ip: First method to get IP address didn't work {e}")
        hostname = gethostname()
        return gethostbyname(hostname)


class Config:
    name = '<not set>'
    bucket = ""
    _svc_domain = ''
    default_store = AWS_S3_NAME
    customer_files = ""
    user_agent = "CSI.UNCONFIGURED"
    ua_prefix = "CSI"
    config_filename = "config.json"  # All modules should go to ENV_Manager for config
    container_name = ""
    testLocal = True
    localdir = os.getcwd()
    local_index = ""
    logLevel = "verbose"
    modhome = os.getenv("CSI_MODULE", "<module_not_set>")
    _lastid = ''
    _ecs = False
    pubipv4 = ''
    platform = 'default'
    sw_version = "0.1.0-dev"
    D = {}
    init_complete = False
    regex_dict = {}
    upstrmAPI = ''
    keyBits = 32
    valBits = 32
    log2slots = 11
    _lookup = None
    sstarget = ''
    first_update_done = False
    _mod_prefixes = []
    _log_post_seconds = 120
    _log_post_last_time = beginning_of_time

    def __init__(self, module_name=None, container_name=None):
        if not module_name:
            if os.environ.get("CSI_MODULE"):
                module_name = os.environ.get("CSI_MODULE")

        if not container_name:
            if os.environ.get("CSI_CONTAINER_NAME"):
                self.container_name = os.environ.get("CSI_CONTAINER_NAME")
        else:
            self.container_name = container_name

        # PyCharm debugger sets the http_proxy variable which causes http requests to fail in a
        # docker compose environment with explicit network definitions.  So if it is set, unset it
        if os.environ.get("CSI_CHECK_HTTP_PROXY"):
            if os.environ.get("http_proxy", ''):
                os.environ["http_proxy"] = ''
                print(f"{Hue.fg.red}You may need to attach this container to the correct docker network...{Hue.rst}")
                time.sleep(15)

        self.platform = get_platform()
        top_level = __package__.split('.')[0]

        if sysconfig.get_config_var(name="MACOSX_DEPLOYMENT_TARGET"):
            resuid = os.getuid()
            resgid = os.getgid()
        else:
            resuid = os.getresuid()[1]
            resgid = os.getresgid()[1]

        lead = Hue.fg.cyn + '>' + ' ' * len(self.token) + Hue.rst
        print(f"{Hue.fg.cyn}{self.token} Module '{top_level}.{module_name.split('.')[-1]}'"
              f"{lead} Caber Systems, Inc. \u00A92024 {self.token}{Hue.rst}\n"
              f"{lead} Python {python_version()} on {self.platform}\n"
              f"{lead} Process ID {os.getppid()}->{os.getpid()}\n"
              f"{lead} Running as UID:GID {resuid}:{resgid}\n"
              f"{lead} Current working directory '{os.getcwd()}'\n"
              f"{lead} Hostname is '{gethostname()}' {'Container name' if self.container_name else ''} '{self.container_name if self.container_name else ''}'")

        # Set up search paths for the config file
        self.bucket = os.environ.get("CSI_BUCKET_OR_SHARE")

        # Incorporate a software version number
        self.sw_version = os.environ.get("CSI_SOFTWARE_VERSION_NUMBER", self.sw_version)

        # Get the name of the running cofiguration file
        self.config_filename = os.environ.get("CSI_RUNNING_CONFIG", self.config_filename)

        status = "initializing" if "dashboard" in os.getenv("CSI_MODULE", "").lower() else "white"
        post_status_message(stage="0.0", message=f"Begin initialization", status="grey")

        self.re_initialize(module_name)

    def re_initialize(self, module_name=None):
        """
        Re-read the config file and reinitialize the config.
        :return:
        """
        i = 0
        self.D = None
        delay = 0
        loc = ''

        if self.modhome and isinstance(self.modhome, str) and self.modhome != '<not set>':
            print(f">>>> Re-Reading module {self.modhome} configuration")
            module_name = self.modhome
        elif not module_name:
            # This should never happen but best to check.
            raise ValueError(f"init.re-initialize: module_name not set on first initialization.")

        myd = Path(__file__).parent.resolve()   # The path to the directory containing this init.py file (./Common)
        up1d = myd.parent.resolve()             # The directory containing all the csi modules
        cwd = Path().resolve()                  # The current working directory
        s3prfx = f"s3://{self.bucket}/"
        tryfiles = [s3prfx, "/tmp/", cwd, myd, up1d]

        # Give special treatment to ENV_Manager since it serves the config to other services.
        if module_name.endswith('ENV_Manager'):
            tryfiles = []
            # If the service has already been initialized, there will be a running config.  If so, use it.
            if os.environ.get("CSI_RUNNING_CONFIG", ''):
                crc = os.environ.get("CSI_RUNNING_CONFIG", '')
                tryfiles.append(crc)
            if os.environ.get("CSI_BOOTSTRAP_CONFIG", ''):
                ccf = os.environ.get("CSI_BOOTSTRAP_CONFIG", '')
                tryfiles.append(ccf)
            tryfiles.extend([cwd, up1d, myd, "/tmp/"])

        elif os.environ.get("CSI_CONFIG_FILE", ''):
            ccf = os.environ.get("CSI_CONFIG_FILE", '')
            if ccf.count('://'):
                tryfiles = [ccf] * 100     # Try to read config file from ENV_Manager many times before giving up
                delay = 10
            else:
                tryfiles = [ccf, s3prfx, "/tmp/", cwd, myd, up1d]

        while 0 <= i < len(tryfiles) and self.D is None:
            self.D, rc = try_cf_read(tryfiles[i], self.config_filename)
            if rc == 'Found':
                if str(tryfiles[i]).endswith('/'):
                    loc = str(tryfiles[i]) + self.config_filename
                elif self.config_filename not in str(tryfiles[i]) and not str(tryfiles[i]).endswith(".json"):
                    loc = str(tryfiles[i]) + '/' + self.config_filename
                else:
                    loc = str(tryfiles[i])
                lead = Hue.fg.cyn + '>' + ' ' * len(self.token) + Hue.rst
                print(f"{lead} Config file read from {loc}")
                self.first_update_done = True
                self.config_filename = loc
            elif rc.startswith('FATAL'):
                # The credentials are invalid.
                status = "exit-error" if "dashboard" in os.getenv("CSI_MODULE", "").lower() else "red"
                post_status_message(stage="0.9", category="error", message=rc, status="red")
                print(f"{self.modhome}: {rc}")
                exit(4)
            elif delay:
                # PyCharm debugger sets the http_proxy variable which causes http requests to fail in a
                # docker compose environment with explicit network definitions.  So if it is set, unset it
                if os.environ.get("http_proxy", ''):
                    os.environ["http_proxy"] = ''
                    print(f"{Hue.fg.red}You may need to attach this container to the correct docker network...{Hue.rst}")
                    time.sleep(15)
                else:
                    print(f"{Hue.fg.orn}Waiting on config file read {str(tryfiles[i])} ret={rc}  n={i}{Hue.rst}")
                    time.sleep(delay)
            i += 1

        if self.D is None:
            status = "exit-error" if "dashboard" in os.getenv("CSI_MODULE", "").lower() else "red"
            post_status_message(stage="0.9", category="error", message="No valid config file found", status="red")
            raise FileNotFoundError(f"No valid config file found")

        # Even though a bucket may have been specified for bootstrap in an environment variable, we
        # need one bucket all services will share in common and that has to come from the config file.
        if not self.bucket:
            ss_bkt = self.D.get('Dependencies', {}).get("shared-storage", {}).get("useTarget", "not_present")
            ss_bkt = self.D.get('Dependencies', {}).get("shared-storage", {}).get("targets", {})\
                           .get(ss_bkt, {}).get("csiBucket", None)
            if ss_bkt:
                self.bucket = ss_bkt
            else:
                self.bucket = self.D.get('GLOBAL', {}).get("csiBucket", "csi-mvp-master")
        else:
            self.D['GLOBAL'].update({"csiBucket": self.bucket})

        # Now that a shared storage bucket has been set, get the customer files path and make a CORI prefix for it
        if not os.environ.get("CSI_CUSTOMER_FILES_PATH"):
            x = self.D.get('GLOBAL', {}).get('customerPrefix', 'customer-files').strip('/ ')
            self.D['GLOBAL'].update({'customerPrefix': x})
        else:
            self.D['GLOBAL'].update({'customerPrefix': os.environ["CSI_CUSTOMER_FILES_PATH"]})
        self.customer_files = f"{self.sspfx}{self.token}{self.bucket}/{self.D['GLOBAL']['customerPrefix']}/"

        # Get the customer AWS account information from the environment variables and update the config
        if os.environ.get('CSI_TENANT_ROLE_ARN', '') and os.environ.get('CSI_ROLE_EXTERNAL_ID', ''):
            pass
            # set_temp_credentials(os.environ['CSI_TENANT_ROLE_ARN'],
            #                      os.environ['CSI_ROLE_EXTERNAL_ID'],
            #                      f"{module_name}.{gethostname()}")
        else:
            if not os.environ.get('AWS_ACCOUNT_ID') and self.D.get('AWS', {}).get('accountID'):
                os.environ['AWS_ACCOUNT_ID'] = self.D['AWS']['accountID']
            elif os.environ.get('AWS_ACCOUNT_ID') and not self.D.get('AWS', {}).get('accountID'):
                self.D['AWS'].update({'accountID': os.environ['AWS_ACCOUNT_ID']})
            if not os.environ.get('AWS_ACCESS_KEY_ID') and self.D.get('AWS', {}).get('accessKey'):
                os.environ['AWS_ACCESS_KEY_ID'] = self.D['AWS']['accessKey']
            elif os.environ.get('AWS_ACCESS_KEY_ID') and not self.D.get('AWS', {}).get('accessKey'):
                self.D['AWS'].update({'accessKey': os.environ['AWS_ACCESS_KEY_ID']})
            if not os.environ.get('AWS_SECRET_ACCESS_KEY') and self.D.get('AWS', {}).get('secretKey'):
                os.environ['AWS_SECRET_ACCESS_KEY'] = self.D['AWS']['secretKey']
            elif os.environ.get('AWS_SECRET_ACCESS_KEY') and not self.D.get('AWS', {}).get('secretKey'):
                self.D['AWS'].update({'secretKey': os.environ['AWS_SECRET_ACCESS_KEY']})
            if not os.environ.get('AWS_DEFAULT_REGION') and self.D.get('AWS', {}).get('region'):
                os.environ['AWS_DEFAULT_REGION'] = self.D['AWS']['region']
            elif os.environ.get('AWS_DEFAULT_REGION') and not self.D.get('AWS', {}).get('region'):
                self.D['AWS'].update({'region': os.environ['AWS_DEFAULT_REGION']})

        # If Terraform set up AWS CloudTrail event logging, read the configuration from the environment variable
        if os.environ.get("CSI_AWS_CLOUDTRAIL"):
            self.D['GLOBAL']["eventBucket"] = ""
            try:
                ct_cfg = json.loads(os.environ.get("CSI_AWS_CLOUDTRAIL"))
            except JSONDecodeError as err:
                print(f"[WARNING] Error decoding environment variable 'CSI_AWS_CLOUDTRAIL'. "
                      f"Disabling CloudTrail ingest.")
            else:
                if not ct_cfg.get("s3-trail-arn") or not ct_cfg.get("s3-trail-bucket"):
                    print(f"[WARNING] No trail name set in environment variable 'CSI_AWS_CLOUDTRAIL'. "
                          f"Disabling CloudTrail ingest")
                else:
                    if ct_cfg.get("s3-trail-arn"):
                        self.D['GLOBAL']["cloudTrailArn"] = ct_cfg.get("s3-trail-arn")
                    if ct_cfg.get("s3-trail-bucket"):
                        self.D['GLOBAL']["eventBucket"] = ct_cfg.get("s3-trail-bucket")

        self.D['GLOBAL']["customerAWSpartition"] = os.environ.get("AWS_PARTITION", "aws")

        r = self.D['RKCQF']['keyBits']
        if r is not None: self.keyBits = int(r)
        r = self.D['RKCQF']['valBits']
        if r is not None: self.valBits = int(r)
        r = self.D['RKCQF']['log2slots']
        if r is not None: self.log2slots = int(r)

        for k in self.D.keys():
            if isinstance(self.D.get(k, ''), dict):
                self.D.get(k, {}).pop('doc', '')

        if self.D.get("Regex"):
            self.regex_dict = compile_regex_dict(self.D['Regex'],
                                                 self.D['GLOBAL'].get("remoteSuffix", ".gz").strip('.'))

        self.set_id(module_name)
        status = "initializing" if "dashboard" in os.getenv("CSI_MODULE", "").lower() else "yellow"
        post_status_message(stage="1.0", message="Initialization complete", status="yellow")

    def set_id(self, module_name=None):
        module_name = module_name.split('.')[-1]
        if module_name is None:
            raise ValueError("Setting module requires the name of the module")
        if module_name not in self.D['GLOBAL']["caberModuleContainerNames"].keys():
            raise ValueError(f"Module '{module_name}' is not one of {self.D['GLOBAL']['caberModuleContainerNames'].keys()}")
        if self.D.get(module_name, None) is None:
            raise KeyError(f"Module '{module_name}' is valid but does not exist in config file!")

        print(f"Caber module {module_name} running as {self.mod_to_con(module_name)}")

        self.modhome = module_name
        self.user_agent = f"{self.ua_prefix}.{module_name}/{self.sw_version} ({gethostname()}; {self.platform}) AWS/{self.D.get('AWS', {}).get('accessKey', os.environ.get('CSI_TENANT_ID', '0000'))}"

        self.name = self.mod_to_con(module_name)
        self.logLevel = os.getenv('CSI_LOG_LEVEL', self.me('logLevel')) or "INFO"
        os.environ['CSI_LOG_LEVEL'] = self.logLevel
        self.testLocal = ('<default>' in self.platform)

        ldd = os.environ.get("CSI_LOCAL_DATA_DIR") or tempfile.mkdtemp()

        if not Path(ldd).is_absolute():
            ldd = Path('/tmp').joinpath(Path(ldd))
        ldd = make_test_dir(ldd)

        self.localdir = ldd.as_posix()
        self.local_index = ldd.joinpath(self.D['GLOBAL'].get('indexFile', 'index')).with_suffix(
                                        self.D['GLOBAL']['filenameSuffixes'].get('index', 'cqf')).as_posix()

        prefixes = list(self.D['GLOBAL']["caberModuleContainerNames"].values())
        prefixes.extend(self.D['GLOBAL']['caberDependencyContainerNames'].values())
        prefixes = [p.get('host', '') if isinstance(p, dict) else p for p in prefixes]
        prefixes.extend(self.D['GLOBAL'].get("svcPrefixes", []))
        prefixes = [re.match(r'^\w+', p).group(0) for p in prefixes if isinstance(p, str) and re.match(r'^\w+', p)]
        self._mod_prefixes = prefixes
        self.D['GLOBAL'].update({"svcPrefixes": self._mod_prefixes})

        self.init_complete = True

    def update_configs(self, s3only=True):

        if self.modhome != 'ENV_Manager':
            print(f"[WARNING] Service {self.modhome} is not allowed to call update_configs")
            return

        elif s3only and os.environ.get("CSI_BUCKET_OR_SHARE", ''):
            # TODO: This code only works for configs stored in s3!
            folder = os.environ.get("CSI_CONFIG_PREFIX", '')
            bucket = os.environ.get("CSI_BUCKET_OR_SHARE", '')
            mc = merge_all_configs_in_folder(folder, self.bucket, user_agent="")
            # Add in the dependent services configurations from Terraform
            mc = update_from_terraform(mc)

            if isinstance(self.D, dict) and isinstance(mc, dict) and mc:
                self.D = merge(self.D, mc)
            elif isinstance(mc, dict) and mc:
                self.D = mc

            # Filter out all the doc items in the config
            for k, v in self.D.items():
                v.pop('doc', None)

            if os.getenv('CSI_RUNNING_CONFIG'):
                try:
                    with open(os.getenv('CSI_RUNNING_CONFIG'), 'w') as fout:
                        json.dump(self.D, fout, cls=extEncoder)
                    self.config_filename = os.getenv('CSI_RUNNING_CONFIG')
                except Exception as err:
                    print(f"[ERROR] Failed to write running config file.  Got: {err}")
        else:
            bootstrap_config_file = os.environ.get("CSI_BOOTSTRAP_CONFIG", '')
            customer_config_file = os.environ.get("CSI_CUSTOMER_CONFIG", '')
            terraform_dynamic_deploy = os.getenv("CSI_DYNAMIC_DEPLOY", "")

            loc = ''
            b_cfg = {}
            c_cfg = {}
            t_cfg = {}
            if bootstrap_config_file:
                bcf = urlsplit(bootstrap_config_file)
                if bcf.scheme in ['', 'file']:
                    bcf = Path(bcf.path)
                    loc = bcf.resolve()
                elif bcf.scheme in ['azure', 's3', 'gs', 'http', 'https']:
                    bcf = bcf.geturl()
                    loc = bcf
                b_cfg, rcb = try_cf_read(bcf)
                if rcb == 'Found':
                    print(f">> Bootsrap config file read from {loc}")
                    if isinstance(self.D, dict) and isinstance(b_cfg, dict) and b_cfg:
                        self.D = merge(self.D, b_cfg)
                    elif not self.D and isinstance(b_cfg, dict) and b_cfg:
                        self.D = b_cfg
                else:
                    print(f">> No Bootsrap config file found")
                    b_cfg = {}

            # Guarantee we go through entire initialization one time with bootstrap only.
            if not self.first_update_done:
                self.first_update_done = True
                return False

            if customer_config_file:
                ccf = urlsplit(customer_config_file)
                if ccf.scheme in ['', 'file']:
                    ccf = Path(ccf.path)
                elif ccf.scheme in ['azure', 's3', 'gs', 'http', 'https']:
                    ccf = ccf.geturl()
                c_cfg, rcc = try_cf_read(ccf, skip_test=True)
                if rcc == 'Found':
                    print(f">> Customer config file read from {ccf}")
                else:
                    print(f">> No Customer config file found")
                    c_cfg = {}

            if terraform_dynamic_deploy:
                t_cfg = json.loads(terraform_dynamic_deploy)

            # if isinstance(self.D, dict) and isinstance(b_cfg, dict) and b_cfg:
            #     self.D = merge(self.D, b_cfg)
            # elif not self.D and isinstance(b_cfg, dict) and b_cfg:
            #     self.D = b_cfg

            if isinstance(self.D, dict) and isinstance(c_cfg, dict) and c_cfg:
                self.D = merge(self.D, c_cfg)
            if isinstance(self.D, dict) and isinstance(t_cfg, dict) and t_cfg:
                self.D = merge(self.D, t_cfg)

            if os.getenv('CSI_RUNNING_CONFIG'):
                try:
                    with open(os.getenv('CSI_RUNNING_CONFIG'), 'w') as fout:
                        json.dump(self.D, fout, cls=extEncoder)
                except Exception as err:
                    print(f"[ERROR] Failed to write running config file.  Got: {err}")
        return os.getenv('CSI_RUNNING_CONFIG', self.config_filename)

    @property
    def G(self):
        return self.D['GLOBAL']

    @property
    def M(self):
        return self.D[self.modhome]

    @property
    def svc_domain(self):
        if not self._svc_domain:
            self._svc_domain = os.environ.get('CSI_SERVICE_DOMAIN', self.D['GLOBAL'].get("svcDomain", ""))
        if self._svc_domain:
            self.D['GLOBAL'].update({"svcDomain": self._svc_domain})
        return self._svc_domain

    @svc_domain.setter
    def svc_domain(self, value):
        if not self.svc_domain and isinstance(value, str):
            self.D['GLOBAL'].update({"svcDomain": value})

    @property
    def log_post_interval(self):
        return timedelta(seconds=self._log_post_seconds)

    @log_post_interval.setter
    def log_post_interval(self, value):
        if isinstance(value, timedelta):
            self._log_post_seconds = value.seconds
        elif isinstance(value, int):
            self._log_post_seconds = value
        else:
            raise ValueError(f"Invalid type for log_post_interval: {type(value)}")

    @property
    def post_log_now(self):
        """Returns True if it is time to post a log message to the dashboard"""
        if os.getenv("LAST_LOG_POST_TIME"): # If the environment variable is set, use it
            try:
                trytime = datetime.fromisoformat(os.getenv("LAST_LOG_POST_TIME"))
            except ValueError:
                pass
            else:
                if trytime > self._log_post_last_time:
                    self._log_post_last_time = trytime

        return datetime.now(tz=timezone.utc) - self._log_post_last_time > self.log_post_interval

    def update_log_post_time(self):
        """Update the last log post time to now"""
        self._log_post_last_time = datetime.now(tz=timezone.utc)

    @property
    def mod_prefixes(self):
        if not self._mod_prefixes or not isinstance(self._mod_prefixes, list):
            prefixes = list(self.D['GLOBAL']["caberModuleContainerNames"].values())
            prefixes.extend(self.D['GLOBAL']['caberDependencyContainerNames'].values())
            prefixes = [p.get('host','').split('-')[0] if isinstance(p, dict) else p.split('-')[0] for p in prefixes]
            prefixes = [p for p in list(set(prefixes)) if p and not p.count('.')]
            self._mod_prefixes = prefixes
        self._mod_prefixes.sort(key=len, reverse=True)
        return self._mod_prefixes

    def append_prefix(self, value):
        if isinstance(self._mod_prefixes, list):
            if isinstance(value, str) and value:
                self._mod_prefixes.append(value)
            if isinstance(value, list):
                self._mod_prefixes.extend([v for v in value if isinstance(v, str) and v])
            self.D['GLOBAL'].update({"svcPrefixes": self._mod_prefixes})

    @property
    def token(self):
        default = "\u22ca\u232c\u22c9"
        return self.D.get('GLOBAL', {}).get('token', default)

    @property
    def null_uid(self):
        default = "NOT-FOUND"
        id_raw = self.D['GLOBAL'].get("authZoptions", {}).get("uidIfNotFound", default)
        return "USER-" + id_raw.strip("USER-")

    @property
    def sspfx(self):
        """Caber global shared storage prefix"""
        x = self.D["Dependencies"]["shared-storage"].get("prefix", "gss")
        if not x.startswith('g'):
            x = f"g{x}"
            self.D["Dependencies"]["shared-storage"].update({"prefix": x})
        return x

    def rem_cori_prefix(self, bucket=None, module="CQF"):
        if not bucket:
            bucket = self.bucket
        return f"{self.sspfx}{self.token}{bucket}/{module}"

    def new_id(self, val=None):
        if self._lastid == '' and not val:
            mac = uuid.getnode()
            nid = uuid.uuid3(uuid.uuid1(), self.name + str(mac))
        elif val:
            nid = uuid.uuid3(uuid.uuid1(), val)
        else:
            nid = uuid.uuid3(uuid.uuid1(), self._lastid)
        pfx = self.D[self.modhome].get('filePrefix', 'XXX')
        return f'{pfx}-{nid.hex[-28:-20].upper()}-{nid.hex[-20:-16].upper()}-{nid.hex[-16:].upper()}'

    def me(self, key, default=None):
        if self.modhome not in self.D['GLOBAL']["caberModuleContainerNames"].keys():
            return default
        keys = key.split('.')
        lk = len(keys)
        val = self.D.get(keys[0], None)
        if val is None:
            val = self.D[self.modhome].get(keys[0], None)
        if lk > 1:
            i = 1
            while i < lk:
                val = val.get(keys[i], None)
                i += 1
                if val is None:
                    val = default
                    break
        elif val is None:
            val = default
        return val

    def mod_to_con(self, mod):
        for m, c in self.D['GLOBAL']["caberModuleContainerNames"].items():
            if m == mod:
                if isinstance(c, dict):
                    # print(f"<<DEBUG>> {c}")
                    return c.get('host', '<<ERROR THIS SHOULD BE A CABER SERVICE HOSTNAME>>')
                else:
                    return c
        return ""

    def con_to_mod(self, con):
        for m, c in self.D['GLOBAL']["caberModuleContainerNames"].items():
            if isinstance(c, dict):
                c = c.get('host')
            if c == con:
                return m
        return ""

# Initialize the CFG global variable based upon the module name.
CFG = Config()

# Each python module/package needs to have a __main__.py file with the following lines coming before ANY other
# code or imports:
#
#     import os
#     mod = os.getenv("CSI_MODULE", None)
#     if __package__ and not mod:
#         # package should be e.g. 'csiMVP.Common'
#         os.environ["CSI_MODULE"] = __package__.split('.')[-1]
#     elif __package__ and mod and mod != __package__.split('.')[-1]:
#         raise RuntimeWarning(f"'CSI_MODULE' and __package__ do not agree {mod} vs. {__package__.split('.')[-1]}")
#     else:
#         # We get here if, as one possibility, the module was not run with 'python -m Module_Name'
#         raise RuntimeError(f"__package__ is not set")