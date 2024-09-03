# ##################################################################################################
#  Copyright (c) 2022.    Caber Systems, Inc.                                                      #
#  All rights reserved.                                                                            #
#                                                                                                  #
#  CABER SYSTEMS CONFIDENTIAL SOURCE CODE                                                          #
#  No license is granted to use, copy, or share this software outside of Caber Systems, Inc.       #
#                                                                                                  #
#  Filename:  filenames.py                                                                         #
#  Authors:  Rob Quiros <rob@caber.com>  rlq                                                       #
# ##################################################################################################

'''
For the sake of consistency across the project, the FileNames class takes a local file path,
AWS s3 path, AWS S3 URI, or bucket/key pair and produces the local and s3 object names, index names,
and hashlist names.  It attempts to do any-to-any translation making it easier for the other modules to give it a
name and get all the other names.
'''

# TODO: Rewrite this POS.  It was grown organically as features were added making it brittle and slow.
#   Pretty much every module depends on it.  Need to rethink it for the general multi-object store host case.

import os
import re

from datetime import datetime, timezone
from botocore.exceptions import ClientError, ParamValidationError
from urllib.parse import unquote_plus, quote_plus

rkcqf_available = True
try:
    import rkcqf as rc
except ModuleNotFoundError:
    rkcqf_available = False
except ImportError:
    pass

mime_check_available = True
try:
    import typecode as mimetypes
except ModuleNotFoundError:
    mime_check_available = False
except (ImportError, AttributeError):
    pass

from csiMVP.Common.init import CFG, beginning_of_time
from csiMVP.Common.remote_open import pull_store_config, ropen, Path, get_object_store_client


filename_suffixes = CFG.G['filenameSuffixes']
module_prefix_to_module_name = {CFG.D[m]['filePrefix']: CFG.D[m]['pathPrefix'] for m in CFG.D.keys()
                                if isinstance(CFG.D[m], dict) and CFG.D[m].get('filePrefix', '')}
module_prefix_to_module_name.update({"CQF": "indexFiles"})


class LocRemData:
    __name = ''
    host = None
    bucket = None
    object = None
    objver = None
    version = '0.0'
    modified = beginning_of_time
    created = beginning_of_time
    etag = ''
    content_type = ''
    content_encoding = False
    sha256 = ''
    _path_obj = None
    _client = None
    _exists = False
    _length = -1
    _scfg = None
    _is_store = False
    _invalid = False
    _ret = None
    deleted = False
    _version = None
    head = {}

    def __init__(self, init_name):
        self._set_name(init_name)

    def _set_name(self, name):
        if not name or not isinstance(name, (str, bytes, os.PathLike)) or self._invalid:
            self._invalid = True
        else:
            self.__name = name
            self.object = name
            self._path_obj = Path(self.__name)

            if name.startswith(CFG.localdir):
                self.host = ''
                mod = ''
                if self._path_obj.is_dir():
                    self._invalid = True
            elif CFG.token in self.__name:
                self.host, self.bucket, mod, self.object, self.objver = parse_cori(name)
                self._client = get_object_store_client(self.__name)
                self._is_store = self.host and self.bucket and self.object and self._client
                if mod:
                    self.object = mod + '/' + self.object
            else:
                self._invalid = True
            self._refresh()

    def _get_name(self):
        if not self._invalid:
            return self.__name
        else:
            return ''

    name = property(_get_name, _set_name)

    @property
    def valid(self):
        return not self._invalid

    def _refresh(self):
        if not self._invalid:
            if self._is_store:
                kwargs = {"ChecksumMode": "ENABLED"}  # Ignored by MinIO

                if self.objver:
                    kwargs.update({"VersionId": self.objver})

                elif self.object.count(CFG.G["objVersSeparator"]):
                    self.object, self.objver = self.object.rsplit(CFG.G["objVersSeparator"], 1)
                    kwargs.update({"VersionId": self.objver})

                try:
                    self._ret = self._client.head_object(Bucket=self.bucket, Key=self.object, **kwargs)
                except (KeyError, ClientError):
                    self._exists = False
                except ParamValidationError:
                    self._exists = False
                else:
                    # Key names used in the .get() statements below come from AWS.  However, not all S3-compatible
                    # object stores (e.g., MinIO) support allof these keys.
                    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.head_object
                    self.sha256 = self._ret.get('ChecksumSHA256', '')
                    self.deleted = self._ret.get('DeleteMarker', False)
                    self._exists = not self.deleted
                    self.modified = self._ret.get('LastModified', beginning_of_time)
                    self.created = self._ret.get('LastModified', beginning_of_time)
                    self.content_type = self._ret.get('ContentType', '')
                    self.content_encoding = self._ret.get('Content-Encoding', '')
                    self._length = self._ret.get('ContentLength', 0)
                    self.etag = self._ret.get('ETag', '')
                    self._version = self._ret.get('VersionId', '')
                    self.head = self._ret
            else:
                self._exists = self._path_obj.exists()
                if self._exists:
                    self.modified = datetime.fromtimestamp(self._path_obj.stat().st_mtime, tz=timezone.utc)
                    self.created = datetime.fromtimestamp(self._path_obj.stat().st_ctime, tz=timezone.utc)
                    self._length = self._path_obj.lstat().st_size
                    self.object = self.__name.split('/')[-1]
                    if mime_check_available:
                        typeobj = mimetypes.get_type(self._path_obj)
                        self.content_type = typeobj.mimetype_file
                        self.content_encoding = typeobj.is_archive
                    if self.content_encoding is None:
                        self.content_encoding = False

    def touch(self, **kwargs):
        if not self._is_store and not self._invalid:
            self._path_obj.touch(**kwargs)
            self._refresh()
        return

    def exists(self):
        if not self._invalid:
            self._refresh()
            return self._exists
        else:
            return False

    @property
    def length(self):
        return self._length if not self._invalid else None

    def write_bytes(self, bytes_in):
        if not self._invalid:
            # Enforce no writing to customer object store with self.host == CFG.sspfx
            if not self._is_store or self._is_store and self.host == CFG.sspfx:
                x = self._path_obj.write_bytes(bytes_in)
                self._refresh()
                return x

    def read_bytes(self):
        if not self._invalid:
            x = self._path_obj.read_bytes()
            self._refresh()
            return x

    def write_text(self, text_in):
        if not self._invalid:
            # Enforce no writing to customer object store with self.host == CFG.sspfx
            if not self._is_store or self._is_store and self.host == CFG.sspfx:
                x = self._path_obj.write_text(text_in)
                self._refresh()
                return x

    def read_text(self):
        if not self._invalid:
            x = self._path_obj.read_text()
            self._refresh()
            return x

    def delete(self):
        if not self._invalid:
            # Enforce no deleting from customer object store with self.host == CFG.sspfx
            if self._is_store and self._exists and not self.deleted and self.host == CFG.sspfx:
                if self._version:
                    x = self._client.delete_object(Bucket=self.bucket, Key=self.object, VersionId=self._version)
                else:
                    x = self._client.delete_object(Bucket=self.bucket, Key=self.object)
                self.deleted = x.get('DeleteMarker', False)
                return x
            elif not self._is_store and self._exists and not self.deleted:
                try:
                    self._path_obj.unlink()
                    self.deleted = True
                    self._exists = False
                except (OSError, FileNotFoundError, ValueError, TypeError) as err:
                    self.deleted = False
                    self._exists = False
                self.modified = beginning_of_time
                self.created = beginning_of_time
                self.sha256 = ''
                self._length = 0
                return

    def list_objects_v2(self, **kwargs):
        if not self._invalid:
            if self._is_store and self._exists and self.bucket:
                kwargs.update({'Bucket': self.bucket})
                x = self._client.list_objects_v2(**kwargs)
                return x
            elif not self._is_store and self._exists and self._path_obj.is_dir():
                return list(self._path_obj.iterdir())

    def list_objects(self, **kwargs):
        if not self._invalid:
            return self.list_objects_v2(**kwargs)


class csiObject:
    local = ''
    remote = ''

    def __init__(self, key='', module=''):

        if not key:
            self.remote = LocRemData('')
            self.local = LocRemData('')

        elif module and not _check_mod(module):
            # When a module is specified, but it is not a valid Caber module, it is a command.  If it is
            # not "invalidate_local" it means the name 'key' is a customer remote object reference.  We
            # can use it directly.
            self.remote = LocRemData(key)
            if module == "invalidate_local":
                self.local = LocRemData('')
            else:
                local_name = CFG.localdir + "/CQF/" + quote_plus(key)
                self.local = LocRemData(local_name)

        else:
            if '%' not in key:
                if key != quote_plus(key):
                    raise ValueError("Argument 'key' must be url quoted using quote_plus")

            # By checking the suffix of the name we can see if the name represents an index, keylist, body object,
            # hashlist, or extracted text. All these go under the module prefix 'CQF' unless a module was specified
            quoted, m, c = _split_suffixes(key)
            if (m and not module) or m == filename_suffixes['index']:
                module = 'CQF'
            elif not module:
                module = CFG.me('pathPrefix')

            if not c:
                c = CFG.G['remoteSuffix']

            rem_prefix = CFG.sspfx + CFG.token + CFG.bucket + "/" + module
            loc_prefix = CFG.localdir + "/" + module

            lp = Path(loc_prefix)
            if not lp.exists():
                lp.mkdir(parents=True, exist_ok=True)

            self.remote = LocRemData(f"{rem_prefix}/{quoted}{m}{c}")
            self.local = LocRemData(f"{loc_prefix}/{quoted}{m}")

    def pull(self, show=True):
        if self.local.exists():
            self.local.touch(exist_ok=True)    # Update the file time
            return self.local.length
        elif not self.local.valid:
            if show:
                print(f"[WARNING] FileNames.pull(): Local filename is not valid '{self.local.name}'")
            return -1
        elif not self.remote.exists():
            if show:
                print(f"[WARNING] FileNames.pull(): Remote file does not exist '{self.remote.name}'")
            return -1
        elif self.remote.length <= 0:
            self.local.touch(exist_ok=True)
            return 0

        try:
            # Pull is always coming from caber shared storage so need to use our transport params
            rrb = self.remote.read_bytes()
            self.local.write_bytes(rrb)
            del rrb
        except (OSError, FileNotFoundError, ClientError, KeyError) as err:
            if show:
                print(f"[WARNING] FileNames.pull(): Exception on write.\n"
                      f"          Remote='{self.remote.name}' to \n"
                      f"          Local='{self.local.name}'\n"
                      f"          {err}")
            return -1
        else:
            if self.local.length == self.remote.length and show:
                print(f".  Pulled {self.local.name}")
        return self.local.length

    def push(self, show=True):
        if not self.local.valid:
            if show:
                print(f"[WARNING] FileNames.push(): Local filename is not valid '{self.local.name}'")
            return -1
        elif not self.remote.valid:
            if show:
                print(f"[WARNING] FileNames.push(): Remote filename is not valid '{self.remote.name}'")
            return -1
        elif not self.local.exists():
            if show:
                print(f"[WARNING] FileNames.push(): Local file does not exist '{self.local.name}'")
            return -1
        elif self.remote.name.split(CFG.token)[0] != CFG.sspfx:
            print(f"[WARNING] FileNames.push(): Cannot push data to customer object stores '{self.remote.name}'")
            return -1
        elif self.local.length <= 0:
            self.remote.touch(exist_ok=True)
            return 0

        size = self.local.length
        try:
            lrb = self.local.read_bytes()
            self.remote.write_bytes(lrb)
            del lrb
        except (OSError, FileNotFoundError, ClientError, KeyError) as err:
            size = -1
            print(f"[ERROR] FileNames.push(): Exception on write.\n"
                  f"        Local='{self.local.name}' to \n"
                  f"        Remote='{self.remote.name}'\n"
                  f"        {err}")
        else:
            if self.remote.exists() and show:
                print(f".  Pushed {self.remote.name}")
            if not self.remote.bucket:
                self.remote.touch(exist_ok=True)
        return size


def _check_mod(x):
    """Enforce mod to be the filePrefix of our module names, otherwise clear it."""
    if x and isinstance(x, str) and x in module_prefix_to_module_name.keys():
        return x
    else:
        return ''


def _rm_slash(name):
    # Remove trailing slash or quote_plus('/') = '%2F'
    if name.endswith('/'):
        name = name[:-1]
    if name.lower().endswith('%2f'):
        name = name[:-3]
    return name


def hbmo_to_cori(host='', bkt='', mod='', obj='', ver=''):
    """
    Join host, bucket, module, object into a Caber Object Resource Identifier (CORI)
    The function tries really hard to find the right host name to put at the front of the CORI
    given host from an API_Map, or http hostname, or it combined with the bucket name.

    :param host: Host where the bucket is located.
    :param bkt: Bucket name
    :param mod: Module name (Not used for customer buckets/objects
    :param obj: object name
    :param ver:  Object version
    :return: cori
    """
    def _finish(h, b, m, o, v):
        if CFG.token in o:
            o = quote_plus(o)
        else:
            o = unquote_plus(o)
        x = Path(b, m, o).joinpath()
        x = str(x)
        x = x[1:] if x.startswith("/") else x
        if v:
            return f"{h}{CFG.token}{x}{CFG.G['objVersSeparator']}{v}"
        else:
            return f"{h}{CFG.token}{x}"

    mod = _check_mod(mod)
    if obj.endswith('/'):
        obj = obj[:-1]

    if isinstance(host, str):
        host = host.strip('/')

    if not host or host == CFG.sspfx or bkt == CFG.bucket:
        host = CFG.sspfx
        bkt = CFG.bucket
        return _finish(host, bkt, mod, obj, ver)
    elif host in CFG.D["Object_Sources"].get("revMap", {}).keys():
        bkt = bkt.strip('/')
        return _finish(host, bkt, mod, obj, ver)
    else:
        scfg, where = pull_store_config(host, bucket=bkt.strip('/'))
        if where:
            host = scfg.get('id_prefix', host).replace(CFG.token, '')
        return _finish(host, bkt, mod, obj, ver)


def parse_cori(cori, no_split_mod=False, host_is_cori=True):
    """
    Split a Caber Object Resource Identifier into host, bucket, module, object
    :param cori:
    :param no_split_mod: Keep the mod and key together as the key as in mod/key
    :param host_is_cori: True if host return value should be the cori id_prefix. False for actual host name.
    :return: host, bucket, module, object, version
    """
    host = ''
    bkt = ''
    mod = ''
    key = ''
    ver = ''

    if not cori:
        return cori, cori, cori, cori, cori

    if CFG.token in cori:
        host, path = cori.split(CFG.token, 1)
        if not host_is_cori:
            sc, _ = pull_store_config(cori)
        if host == CFG.sspfx and path.count('/') >= 2:
            if not no_split_mod:
                bkt, mod, key = path.split('/', 2)
            else:
                bkt, key = path.split('/', 1)
                mod, _ = key.split('/', 1)
            if not host_is_cori:
                host = sc.get('host') if sc.get('host') else host
        else:
            if not host_is_cori:
                host = sc.get('host') if sc.get('host') else host
            mod = ''
            if path.count('/') >= 1:
                bkt, key = path.split('/', 1)
            else:
                bkt = path
            # If the key endswith a '/' then it's just a prefix.  Prefixes have no useful properties.
            key = '' if key.endswith('/') else key

    elif cori.startswith(CFG.localdir):
        host = ''
        mod, key = cori.split('/', 1)
        bkt = ''
    else:
        raise ValueError(f"Bad resource identifier: No bucket cori found in {cori}")

    if key.count(CFG.G["objVersSeparator"]):
        key, ver = key.rsplit(CFG.G["objVersSeparator"], 1)

    return host, bkt, mod, _rm_slash(key), ver


def _parse_directory_item(name):
    subdir = ''
    if '/' not in name:
        raise ValueError(f"Bad directory item: No directory or '/' found in {name}")
    mod, obj = name.rsplit('/', 1)
    mod = mod.strip('/')
    if '/' in mod:
        mod, subdir = mod.split('/', 1)
    return mod, subdir, _rm_slash(obj)


sha256_pat = re.compile("([0-9a-fA-F]{63,64})")


def _is_sha256(name):
    x = sha256_pat.match(name)
    if not x:
        return ''
    return x.group(0)


def _split_suffixes(name):
    i = ''
    g = ''
    if name.endswith(CFG.G['remoteSuffix']):
        g = CFG.G['remoteSuffix']
        name = name.replace(CFG.G['remoteSuffix'], '', 1)

    for sfx in filename_suffixes.values():
        new = name.replace(sfx, '', 1)
        if new != name:
            i = sfx
            name = new
            break

    return _rm_slash(name), i, g


def cori_to_resource_arns(cori, acct=None, region=None, ret='all'):
    host, bkt, mod, key, ver = parse_cori(cori)
    scfg, where = pull_store_config(cori)
    client = get_object_store_client(cori)
    object_resource = {"type": "", "ARN": ""}
    bucket_resource = {"type": "", "ARN": ""}

    if host and scfg:  # One colon before first slash means it's a URL
        if acct is None:
            acct = ''
        if region is None:
            region = scfg.get('region', client.meta.region_name)
        obj_type = scfg.get('type', '')
        id_pfx = scfg.get('id_prefix', '').replace(CFG.token, '')
        arnp = 'ARN'
        if obj_type == 's3':
            arnp = 'AWS'
        bucket_resource = {"type": f"{arnp}::{obj_type.upper()}::Bucket",
                           "ARN": f"arn:{obj_type}:{id_pfx}:{region}:{acct}:{bkt}", "accountId": acct}
        cori_resource = {"type": "CORI", "CORI": cori}
        if key:
            object_resource = {"type": f"{arnp}::{obj_type.upper()}::Object",
                               "ARN": f"arn:{obj_type}:{id_pfx}:{region}:{acct}:{bkt}/{key}"}
            resource_arns = {"resources": [bucket_resource, object_resource, cori_resource]}
        else:
            resource_arns = {"resources": [bucket_resource, cori_resource]}
        if ret.startswith('o'):
            return object_resource['ARN']
        elif ret.startswith('b'):
            return bucket_resource['ARN']
        else:
            return resource_arns
    elif ret.startswith('o') or ret.startswith('b'):
        return ''
    else:
        return cori


def resource_arns_to_cori(resources):
    """
    Convert a dict of resource arns from a Cloudtrail log entry, or similar, to a list of CORIs

    :param resources: {'resources':
                            [
                              {'type': 'AWS::cnewcomini::Bucket',
                               'ARN': 'arn:minio:cnewcomini:us-west-1::newco-demo',
                               'accountId': ''},
                              {'type': 'AWS::cnewcomini::Object',
                               'ARN': 'arn:minio:cnewcomini:us-west-1::newco-demo/urn:oid:28'}
                            ]
                          }

    or
                      {'resources':
                           [
                               {'type': 'AWS::S3::Object',
                                'ARNPrefix': 'arn:aws:s3:::newco-docs-3428fa035e52b34261fffbfc9kk177c1c481bf7/'},
                               {'accountId': '062333172176',
                                'type': 'AWS::S3::Bucket',
                                'ARN': 'arn:aws:s3:::newco-docs-3428fa035e52b34261fffbfc9kk177c1c481bf7'}
                          ]
                      }

    :return: cnewcomini⋊⋉newco-demo/urn:oid:28
    """
    def _arnsplit(arn):
        ars = arn.split(':', 5)
        if len(ars) >= 6:
            if arn.startswith("arn:aws:s3"):
                scfg, where = pull_store_config("s3.amazonaws.com", ars[5].split('/')[0])
                if scfg.get('id_prefix'):
                    return f"{scfg['id_prefix']}{ars[5]}"
            else:
                return f"{ars[2]}{CFG.token}{ars[5]}"
        return ""

    if isinstance(resources, dict):
        if resources.get('resources', None):
            resources = resources.get('resources', None)
        else:
            resources = [resources]
    if not isinstance(resources, list):
        print(f"[WARNING] Unexpected input type '{type(resources).__qualname__}'")
        return []

    coris = [b.get('CORI', '') for b in resources if b.get('type', '') == 'CORI']
    objects = [b.get('ARN', '') for b in resources if b.get('type', '').endswith('Object')]
    # ARN Prefixes are not objects.  They only specify a bucket.
    # buckets = [b.get('ARNPrefix', '').split('/', 1)[0] for b in resources if b.get('type', '').endswith('Object')]

    bkt_check = [o.rsplit('/', 1)[0] for o in objects]
    buckets = [b.get('ARN', '') for b in resources if b.get('type', '').endswith('Bucket')]
    buckets = set(buckets).difference(bkt_check)

    for arnlist in [objects, buckets]:
        for arn in arnlist:
            new_cori = _arnsplit(arn)
            # Filtering with hbmo_to_cori(*parse_cori(new_cori)) here for consistency.
            new_cori = hbmo_to_cori(*parse_cori(new_cori)) if new_cori else new_cori
            coris.append(new_cori)

    coris = set(coris)
    coris.discard("")
    return list(coris)


class FileNames:
    """
    Many places in each services' code there is the need to take all or part of an object name, say the bucket
    and key of an S3 object, and derive where to put, and how to name, local CQF index files, hashlist files,
    etc., as sequence.py does.  And we need inverse lookups as well, to go from an index file to the name of
    the S3 object it came from.  That's all handled here along with methods to pull remote objects to local disk,
    push local to remote, check existence, last modified dates, etc.

    FileNames leverages our remote-open.py module to access remote objects that use Caber Object Resource
    Identifiers (CORIs) such as 'cnewcomini⋊⋉newco-demo/PAPI/urn:oid:40'.  We use the patched version of Path
    from remote-open.py to open/read/write remote and local object which in turn uses smart-open which does
    most of the heavy lifting for remote access over the Internet to many flavors of cloud object stores
    transparently.

    Given a CORI such as 'cnewcomini⋊⋉newco-demo/urn:oid:40' representing a customer object in object storage
    system 'cnewcomini', in bucket 'newco-demo', with key 'urn:oid:40', we create the following names (based
    upon default settings for CFG.localdir, file name suffixes, etc.:

       Local object name: /data/CQF/cnewcomini%E2%8B%8A%E2%8B%89newco-demo%2FPAPI%2Furn%3Aoid%3A40
       Local index name:  /data/CQF/cnewcomini%E2%8B%8A%E2%8B%89newco-demo%2FPAPI%2Furn%3Aoid%3A40.ccqf
       Remote index name: gss⋊⋉csi-master/CQF/cnewcomini%E2%8B%8A%E2%8B%89newco-demo%2FPAPI%2Furn%3Aoid%3A40.ccqf.gz
       etc.

    We also need to take any of those names above as a starting point and create all the others.  Also, when
    we don't know the name of the object, such as when Process_API indexes an API payload, we need to create
    an 'unattached' set of names for the other associated files.  The format for an unattached CORI is:
         ⋊⋉05f05e8c7761b353b5202da01ac3bb10a975f6c6827ef6a  or CFG.token + SHA256 of the payload.

    Which gets converted to
       Local index name: /data/CQF/05f05e8c7761b353b5202da01ac3bb10a975f6c6827ef6a.ccqf
       Remote index name: gss⋊⋉csi-master/CQF/05f05e8c7761b353b5202da01ac3bb10a975f6c6827ef6a.ccqf.gz
       etc.

    Under the hood we do all the conversions by taking the input name down to the four basic components below
    then build back all the other names from there.
       self.store_host - The object store host identifier from the dynamic customer configuration
                         CFG.D['Object_Sources'], or from Caber's global shared store in CFG.D["Dependencies"]["shared-storage"]

       self.obj_bkt    - The bucket in the store_host holding the object
       self.obj_key    - The prefix/key for the object
       self._csimod    - Internal location identifier for objects in Caber's global shared store
                         most commonly set to the default 'CQF' for object indices and such.

    """

    _complete = False
    _s3n = False
    _csimod = ''
    _CFG = None
    hashlist = None
    obj_bkt = ''
    obj_key = ''        # b = Bucket, k = Key, s = Corresponding remote URL, q = Url-quoted arg with host/bkt/key
    obj_ver = ''
    meta = {}
    sha256 = ''
    rec_id = ''
    quoted = ''
    store_host = ''
    _local_invalid = False
    index = None
    index_k = None
    index_t = None

    def __init__(self, name='', module='', rec_id='', names_only=False):
        secondary = ''

        # CASE: There should never be more than one CFG.token in the name, and never more than one quote_plus(CFG.token)
        if name.count(CFG.token) > 1 or name.count(quote_plus(CFG.token)) > 1:
            raise ValueError(f"Bad resource identifier: More than one CFG.token found in {name}")

        # CASE: Process_API names data objects from APIs, where the source is unknown, with a token in front of a
        #       SHA256. Normally not quoted like:
        #                     ⋊⋉05f05e8c7761b353b5202da01ac3bb10a975f6c6827ef6a
        #
        elif name.startswith(CFG.token):
            self.store_host = CFG.sspfx
            self.module = "CQF" if not module else module
            self.obj_bkt = ''
            self.obj_key = name[len(CFG.token):]   # Remove the leading CFG.token

        # CASE: If name is in our local data directory, parse it and check if it ends with a customer index object.
        #       Example w/o customer object:
        #            /data/module/05f05e8c7761b353b5202da01ac3bb10a975f6c6827ef6a.ccqf.gz
        #       Example with customer object:
        #            /data/module/cnewcomini%E2%8B%8A%E2%8B%89newco-demo%2Fsavage-babage.txt.ccqf.gz
        #                                ^^^^^^^^  ^^^^^^^^^^^^^^^^
        #                   customer storage host  quote_plus(CFG.token)
        #
        elif name.startswith(CFG.localdir):
            name = name.replace(CFG.localdir, '')
            # Get the module name from the directory name.
            mod, subdir, self.obj_key = _parse_directory_item(name)
            self.module = mod
            if not self.module and self.module != 'CQF':
                print(f"[DEBUG] Could be an issue here:  Got {self.module} in local url")
            if quote_plus(CFG.token) in self.obj_key:
                secondary = unquote_plus(self.obj_key)

        # CASE: If it's marked from global remote storage, parse the name and check if it ends with
        #       a customer index object as above.
        #
        elif name.startswith(f"{CFG.sspfx}{CFG.token}"):
            self.store_host, self.obj_bkt, mod, self.obj_key, self.obj_ver = parse_cori(name)
            self.module = mod
            if quote_plus(CFG.token) in self.obj_key:
                secondary = unquote_plus(self.obj_key)
        elif name.startswith(quote_plus(f"{CFG.sspfx}{CFG.token}")):
            raise ValueError(f"Bad resource identifier: Should not see '{CFG.sspfx}{CFG.token}' url quoted {name}")

        # CASE: Here it is a reference to customer object in a customer storage host like:
        #         cnewcomini⋊⋉newco-demo/savage-babage.txt
        #
        elif CFG.token in name:
            secondary = name
        elif quote_plus(CFG.token) in name:
            secondary = unquote_plus(name)
        else:
            self._local_invalid = True
            if CFG.logLevel.lower() == 'verbose':
                print(f"[WARNING] FileNames.__init__: Invalid object name '{name}'")

        # Our setter function below for self.module won't allow it to change once it's been set.  So if module
        # has not otherwise been set above, set it from the initialization arg 'module'. If that was empty,
        # then use the filePrefix of the current module.
        self.module = module
        self.module = CFG.me('filePrefix')

        if secondary:
            # If the object referenced above turned out to be another resource identifier, meaning we wrapped
            # a customer object resource identifier in a caber object resource identifier, we use the customer one.
            # Since we are starting anew here with the secondary resource identifier, force the change to
            # self.module by setting its underlying variable self._csimod below.
            self.store_host, self.obj_bkt, self._csimod, self.obj_key, self.obj_ver = parse_cori(secondary)

        self.sha256 = _is_sha256(self.obj_key)
        if self.rec_id == '':
            self.rec_id = F"{CFG.new_id()}"

        # Get rid of any filename suffixes for index, body, keys
        self.obj_key, i, g = _split_suffixes(self.obj_key)

        if self.store_host == CFG.sspfx:
            ob = self.obj_key
        else:
            ob = hbmo_to_cori(self.store_host, self.obj_bkt, self.module, self.obj_key, self.obj_ver)
        if not self._local_invalid:
            self.quoted = quote_plus(ob)
        else:
            self.quoted = ""

        if not names_only:
            self._finalize()

    def _finalize(self):
        if not self._complete:
            self.index = csiObject(f"{self.quoted}{filename_suffixes['index']}", self._csimod)
            self.index_k = csiObject(f"{self.quoted}{filename_suffixes['index_k']}", self._csimod)
            self.index_t = csiObject(f"{self.quoted}{filename_suffixes['index_t']}", self._csimod)
            self.body = csiObject(f"{self.quoted}{filename_suffixes['body']}", self._csimod)
            self.keys = csiObject(f"{self.quoted}{filename_suffixes['keys']}", self._csimod)
            self.text = csiObject(f"{self.quoted}{filename_suffixes['text']}", self._csimod)
            if CFG.G.get("keepHashFiles", False):
                self.hashlist = csiObject(f"{self.quoted}{filename_suffixes['hashes']}", self._csimod)
            self.object = csiObject(f"{self.rem_customer_object}", "customer object")
            self._complete = True

    @property
    def rem_customer_object(self):
        if not self._local_invalid and self.store_host and self.store_host != CFG.sspfx:
            return hbmo_to_cori(self.store_host, self.obj_bkt, '', self.obj_key, self.obj_ver)
        else:
            return ''

    @property
    def local_object(self):
        if not self._local_invalid and self._complete and self.rem_customer_object:
            return self.object.local.name
        else:
            return ''

    @property
    def module(self):
        if self._local_invalid:
            return
        return self._csimod

    @module.setter
    def module(self, x):
        if not self._csimod and not self._local_invalid:
            self._csimod = _check_mod(x)
            
    @property
    def bksq(self):
        if self._local_invalid:
            return {}
        if self.obj_ver:
            return {"B": hbmo_to_cori(self.store_host, self.obj_bkt),
                    "K": f"{self.obj_key}{CFG.G['objVersSeparator']}{self.obj_ver}",
                    "S": self.rem_customer_object,
                    "Q": self.quoted}
        else:
            return {"B": hbmo_to_cori(self.store_host, self.obj_bkt),
                    "K": self.obj_key,
                    "S": self.rem_customer_object,
                    "Q": self.quoted}

    def invalidate_local_object(self):
        self._local_invalid = True
        if self.rem_customer_object:
            self.object = csiObject(f"{self.rem_customer_object}", "invalidate_local")

    def getmeta(self):
        if self._local_invalid:
            return
        if rkcqf_available:
            if not self.meta and self.index.pull() > 0:
                if rc.QFinit(self.index.local.name, initialize=False, read_only=False):  # ALWAYS LOCAL
                    self.meta = rc.get()
                    rc.QFclose()
                if not self.sha256:
                    self.sha256 = self.meta.get('sha256ext', b'').hex()
                elif self.meta.get('sha256ext', b'').hex() != self.sha256:
                    print(f"Inconsistent sha256:\n\t{self.rem_customer_object}\n\t{self.meta.get('sha256ext', b'').hex()}\n\t{self.sha256}")
            return self.meta.get('sha256ext', b'').hex()
        else:
            print("[WARNING] Cannot return metadata: RKCQF package not available in this Module")
            return ''

    def to_dict(self):
        if self._local_invalid:
            return {}
        if not self._complete:
            return self.bksq
        if CFG.G.get("keepHashFiles", False):
            return {'remote': {'objBkt': self.obj_bkt, 'objKey': self.obj_key,
                               'objURI': self.rem_customer_object, 'hashlist': self.hashlist.remote.name,
                               'index': self.index.remote.name, 'index_k': self.index_k.remote.name, 
                               'index_t': self.index_t.remote.name},
                    'local': {'object': self.local_object, 'hashlist': self.hashlist.local.name,
                              'index': self.index.local.name, 'index_k': self.index_k.local.name, 
                              'index_t': self.index_t.local.name}}
        else:
            return {'remote': {'objBkt': self.obj_bkt, 'objKey': self.obj_key,
                               'objURI': self.rem_customer_object, 'index': self.index.remote.name, 
                               'index_k': self.index_k.remote.name, 'index_t': self.index_t.remote.name},
                    'local': {'object': self.local_object, 'index': self.index.local.name, 
                              'index_k': self.index_k.local.name, 'index_t': self.index_t.local.name}}

    def rm_locals(self):
        if self._complete and not self._local_invalid:
            if CFG.G.get("keepHashFiles", False):
                locals = [self.index.local.name, self.index_k.local.name, self.index_t.local.name, 
                          self.hashlist.local.name, self.body.local.name,
                          self.keys.local.name, self.text.local.name, self.local_object]
            else:
                locals = [self.index.local.name, self.index_k.local.name, self.index_t.local.name,
                          self.body.local.name, self.keys.local.name, self.text.local.name, self.local_object]
            for path in locals:
                if os.path.exists(path) and os.path.isfile(path):
                    os.remove(path)


