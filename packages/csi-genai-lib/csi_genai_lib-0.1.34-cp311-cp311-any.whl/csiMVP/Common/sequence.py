# ##################################################################################################
#  Copyright (c) 2022.    Caber Systems, Inc.                                                      #
#  All rights reserved.                                                                            #
#                                                                                                  #
#  CABER SYSTEMS CONFIDENTIAL SOURCE CODE                                                          #
#  No license is granted to use, copy, or share this software outside of Caber Systems, Inc.       #
#                                                                                                  #
#  Filename:  sequence.py                                                                          #
#  Authors:  Rob Quiros <rob@caber.com>  rlq                                                       #
# ##################################################################################################
import fnmatch
import os
import math
import codecs
import re

import io
import binascii
import base64
import ftfy

import socket

import gzip
import zipfile
import json  # import loads as jloads, dumps as jdumps, JSONDecodeError

import pandas as pd
import xmltodict
import collections
import hashlib
# import imagehash

try:
    import tika
    from tika import detector, config, parser
except (ModuleNotFoundError, ImportError):
    tika = None
    detector = None
    config = None
    parser = None

import warnings
from langchain.utilities import LangChainDeprecationWarning
# Suppress specific deprecation warnings from LangChain
warnings.filterwarnings(
    action='ignore',
    category=LangChainDeprecationWarning,
    message=".*deprecated.*"
)

from langchain.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader

from email.message import Message as content_type_parser

mime_check_available = True
try:
    import typecode as mimetypes
except ModuleNotFoundError:
    mime_check_available = False
except ImportError:
    pass

from csiMVP.Common.remote_open import ropen, Path
from datetime import datetime, timezone
from yaml import load as yload, SafeLoader  #, FullLoader, YAMLError

try:
    import rkcqf as rc
except (ImportError, ModuleNotFoundError):
    print(f"[DEBUG] (sequence) Could not import rkcqf")
    try:
        import csi_genai_lib.rkcqf as rc
    except (ImportError, ModuleNotFoundError):
        print(f"[DEBUG] (sequence) Could not import csi_genai_lib.rkcqf")
        rc = None

from requests.exceptions import ReadTimeout
from urllib3.exceptions import ReadTimeoutError

from csiMVP.Toolbox.retry import retry
from csiMVP.Toolbox.goodies import b_if_not_a
from csiMVP.Toolbox.filenames import FileNames
from csiMVP.Toolbox.json_encoder import extEncoder
from csiMVP.Dependencies.tika_init import init_tika

whsp = [" ", "\n", "\t", "    ", "   ", "  ", "  ", "  "]
gzip_magic_number = b'\x1f\x8b'

if tika is not None:
    tika.TikaClientOnly = True

logLevel = os.getenv('CSI_LOG_LEVEL', 'info')
DEBUG = (logLevel in ["verbose", "debug"])
VERBOSE = (logLevel == "verbose")
LF = '\n'
bLF = b'\n'

bytes_per_hash = []

char_filter = re.compile(r"[^a-zA-Z,/:;\"\'\n]")
unicode_substitions = {"\\u2010": "-", "\\u2011": "-", "\\u2012": "-", "\\u2013": "-", "\\u2014": "-", "\\u2015": "-",
                       "\\u2018": "'", "\\u2019": "'", "\\u201c": "\"", "\\u201d": "\"", "\\u2026": "...",
                       "\\u00a0": " ", "\\ufb00": "ff", "\\ufb01": "fi", "\\ufb02": "fl", "\\ufb03": "ffi",
                       "\\ufb06": "st", "\\ufb04": "ffl"}

langchain_inprompt_tags = ["Question:", "Helpful Answer:", "Chat History:", "Human:", "Relevant text, if any:",
                           "Assistant:", "Follow Up Input:", "Standalone question:", "QUESTION:", "FINAL ANSWER:",
                           "Model:", "Critique Request:", "Critique:", "Revision Request:", "Revision:", "Content:"]

Langchain_context_preambles = ["Use the following pieces of context to answer the user's question. \nIf you don't know the answer, just say that you don't know, don't try to make up an answer."]


def normalize(text):
    if not isinstance(text, str):
        return text

    text = re.sub(r'|'.join(map(re.escape, unicode_substitions.keys())),
                  lambda m: unicode_substitions[m.group()], text)
    # The below two problems were seen in a research paper that was in a .pdf format but had equations and much
    # text that was not extracted correctly by PyPDFLoader
    # Fix any unicode characters that are not properly encoded
    if "\\u" in text:
        text = ftfy.fix_text(text)

    # Ligatures are a pain. Create a regex that finds one '/' followed by a letter in [a-zA-Z], followed by an
    # underscrore, followed by another letter in [a-zA-Z] with the letter between the '/' and '_'.
    pattern = r'/([a-zA-Z])_([a-zA-Z])'
    # The replacement keeps only the first captured group
    text = re.sub(pattern, r'\1\2', text)
    return text


def _check_compressed(test_bytes, test_type):
    """
    https://www.gnu.org/software/tar/manual/html_node/gzip.html

    :param self:
    :param test_type:
    :return:
    """
    # TODO: Support more compressed file formats.  Fleep is useless since it cannot detect compression type!

    # compressed_types = {"*gzip*": "gzip", "*bzip*": "bzip2", "*lzip*": "lzip", "*lzma*": "lzma",
    #                     "*lzop*": "lzop", "*lzo*": "lzo", "*lz4*": "lz4", "*lzw*": "lzw", "*lzh*": "lzh",
    #                     "*lzx*": "lzx", "*tgz*": "tar", "*gz*": "gzip", "*zstd*": "zstd", "*binhex*": "binhex",
    #                     "*7zip*": "7zip", "*7za*": "7za", "*7z*": "7z", "*xz*": "xz", "*zip*": "zip",
    #                     "*gtar*": "tar", "*x-tar*": "tar", "*vnd.rar*": "rar", "*x-rar*": "rar",
    #                     "*brotli*": "brotli", "*compressed*": "mimetypes", "*compress*": "compress",
    #                     "*octet-stream*": "mimetypes", "*binary*": "mimetypes", "*br*": "mimetypes"}

    # magic bytes from https://en.wikipedia.org/wiki/List_of_file_signatures
    magic_bytes = {b'\x1F\x8B': "gzip", b'\x42\x5A\x68': "bzip2", b'\xFD\x37\x7A\x58\x5A\x00': "xz",
                   b'\x37\x7A\xBC\xAF\x27\x1C': "7z", b'\x75\x73\x74\x61\x72\x00\x30\x30': "tar",
                   b'\x75\x73\x74\x61\x72\x20\x20\x00': "tar"}

    compressed_types = {"*gzip*": "gzip", "*gz*": "gzip", "*zip*": "zip", "*compress*": "gzip",
                        "*octet-stream*": "gzip", "*binary*": "gzip"}

    if isinstance(test_type, list):
        test_type = ' '.join(test_type)

    test_mb = ''
    test_ct = ''

    if test_bytes and isinstance(test_bytes, (bytes, bytearray)):
        test_mb = [magic_bytes[m] for m in magic_bytes.keys() if test_bytes.startswith(m)]
        if any(test_mb):
            test_mb = test_mb[0]

    ret_mime = test_type
    if test_type and isinstance(test_type, str):
        test_ct = [compressed_types[pat] for pat in compressed_types.keys() if fnmatch.fnmatch(test_type, pat)]
        if any(test_ct):
            test_ct = test_ct[0]

    # If it's a compressed file and the mime type says it's a compressed file,
    # then clear the mime type to force Tika redetection of the type.
    if test_mb and test_mb == test_ct:
        return test_mb, ''
    elif test_mb and not test_ct:
        return test_mb, test_type

    elif test_mb and test_ct and test_mb != test_ct:
        print(f"[DEBUG] (_check_compressed) Magic bytes and mime type suggest "
              f"inconsistent compression types ({test_mb} != {test_ct})")
        return test_mb, ''

    elif not test_mb and test_ct and test_ct != 'mimetypes':
        if 'octet-stream' not in test_type:
            print(f"[DEBUG] (_check_compressed) No match on magic bytes ({test_bytes}) "
                  f"but mime type ({test_type}) suggests compressed format")
        return test_ct, ''

    else:
        return '', test_type


def parse_content_types(content_type: (str, list), charset='') -> dict:
    """
    Content-Type headers can be in multiple formats:
        - text/plain
        - text/plain; utf-8
        - text/plain; charset=utf-8
        - text/plain; charset="utf-8"
    """

    ctp = content_type_parser()
    ctp['content-type'] = content_type
    test = ctp.get_params()
    test = dict(test)
    content_type = list(set(test.keys()).difference({'charset', 'boundary'}))
    charset = b_if_not_a(test.get("charset"), charset)
    boundary = test.get("boundary")

    ret = {'mime': content_type, 'charset': charset, 'multi': False}

    if content_type and isinstance(content_type, (str, bytes, bytearray)):
        content_type = [content_type]

    if not isinstance(content_type, list):
        return ret

    multi = True if len(content_type) > 1 else False
    out = []

    for ct in content_type:
        if 'charset=' in ct:
            mime, char = [c.strip('"; ') for c in ct.split('charset=', 1)]
        elif ';' in ct:
            mime, char = [c.strip('"; ') for c in ct.split(';', 1)]
        else:
            mime = ct
            char = charset

        out.append({'mime': mime, 'charset': char})

    if out:
        ret = {'mime': out[0]['mime'], 'charset': out[0]['charset'], 'multi': multi}
        if multi:
            ret.update({"others": out[1:]})

    return ret


def bytes_to_string(val, ctype=''):
    """
    Convert a bytes object to a string by trying multiple encodings.  If the bytes cant be converted
    it will return an empty string.  If the input is already a string function will simply return it.
    """

    newval = ''
    newlen = 0
    newct = ctype if ctype else 'UTF-8'

    if isinstance(val, str):
        return val, newct

    charsets = ['UTF-8', 'UTF-16', 'ISO-8859-1', 'UTF-32']

    if isinstance(val, (bytes, bytearray)):

        if ctype:  # Try the input charset first if it exists
            ct = [ctype]
            ct.extend([c for c in charsets if c != ctype])
            charsets = ct

        fail = []
        for ct in charsets:
            try:
                cdc = codecs.lookup(ct)
            except LookupError:
                fail.append(f"Invalid codec: {ct}")
                continue
            try:
                newval, newlen = cdc.decode(val)  # errors='ignore'
                newct = cdc.name
                break
            except (LookupError, TypeError, UnicodeDecodeError, UnicodeTranslateError) as err:
                fail.append(f"Decode failed: {ct} {err}")
        if not newval:
            fail = '\n'.join(fail)
            print(f"[DEBUG] (bytes_to_string) {fail}")

    return newval, newct


def bytes_to_string_y(val, ctype=''):
    newval, newct = bytes_to_string(val, ctype)
    return newval


def split_text_lines(text, min_size=80, old_behavior=False):
    '''
    Split lines of text in the input text and remove any lines that are less than min_size characters long.
    Compact the text and remove almost all special characters if old_behavior is True.  If old_behavior is
    False (default) then the text will be compacted but not have special characters removed.
    :param text:
    :param min_size:
    :param old_behavior:
    :return:
    '''
    if not text:
        return ''

    success_string = f'.  Converted {len(text)} characters of text to '

    # Compact the text and remove almost all special characters
    bar = re.sub(char_filter, '', text) if old_behavior else normalize(text)
    encoded = [f.encode('utf-8') for f in bar.splitlines() if len(f) >= min_size]
    if old_behavior:
        encoded.append(re.sub(r"\s", '', bar).encode('utf-8'))
    else:
        encoded.append(bar.encode('utf-8'))

    success_string += f'{len(encoded)} lines with {len(b"".join(encoded))} total characters'
    print(success_string)
    return encoded


def is_useful_mime_type(cfg, content_type):
    """
    It's common to see the incomming content_type of a compressed object be the mime-type of the
    decompressed version of the object.  If so, we want to save that content type to use after
    decompressing since the mime-type checkers in Tika, typecode, mimetypes, etc., default to
    'text/plain' or 'application/octet-stream', or other not-useful mime-types that can be configured
    in CFG.G["alwaysCheckTypes"].

    Similarly, if the incomming content_type indicates the compressision type (e.g., application/gzip)
    it is not a useful indicator of the decompressed content type.
    """
    if not content_type:
        return False
    test_list = cfg.G["alwaysCheckTypes"]
    test_list.extend(cfg.G["compressed_types"])
    useful = not any([fnmatch.fnmatch(content_type, pat) for pat in test_list])
    return useful


def pick_best_mime_type(cfg, mime_1, mime_2):
    useful_mime_1 = is_useful_mime_type(cfg, mime_1)
    useful_mime_2 = is_useful_mime_type(cfg, mime_2)

    if useful_mime_1 and not useful_mime_2:
        return mime_1
    elif useful_mime_2 and not useful_mime_1:
        return mime_2
    else:
        return mime_1


class TryDecode:
    xml_dict = {}
    json_dict = {}
    yaml_dict = {}
    content_updated = False
    content_decompressed = None
    content_string = ''
    content_bytes = b''
    content_type = ''
    charset = ''
    content_encoding = ''
    exists = False
    is_str = False
    text = ''
    _original_mime_type = ''
    pre_sha256 = ''
    _not_compressed = False
    _doc_type = ''
    flat_dict = collections.OrderedDict()
    errors = []
    _step = 0
    _b64 = False
    _min_obj_size = 128
    _too_small = False
    _CFG = None
    _ExTika = None

    def __init__(self, CFG, content, from_file=False, b64=False, content_type=None, content_encoding=None, charset=None):
        self._b64 = b64
        self._CFG = CFG

        if content_type and isinstance(content_type, str):
            self.content_type = content_type
        if content_encoding and isinstance(content_encoding, str):
            self.content_encoding = content_encoding
        if charset and isinstance(charset, str):
            self.charset = charset

        self._original_mime_type = self.content_type if is_useful_mime_type(self._CFG, self.content_type) else ''

        self.exists = Path(content).exists()
        if not self.exists:
            if DEBUG:
                print(f"[DEBUG] TryDecode: Object {content} does not exist")
        else:
            if self._ExTika is None:
                self._ExTika = Extract(self._CFG)

            if b64 and isinstance(content, str) and not from_file:
                self._un_base64(content)
                self._decode()
            elif isinstance(content, str) and from_file and b64:
                with ropen(content, 'r') as _fin:
                    self.content_string = _fin.read()
                self._un_base64(self.content_string)
                self._decode()
            elif isinstance(content, str) and from_file and not b64:
                with ropen(content, 'rb') as _fin:
                    self.content_bytes = _fin.read()
                self._decode()
            elif isinstance(content, (bytes, bytearray)):
                self.content_bytes = content
                self._decode()
            else:         # isinstance(content, str):
                if DEBUG:
                    print(f"[DEBUG] TryDecode: Hit default case. Variable type is "
                          f"{type(content).__qualname__}.  Mime type is {content_type}")
                self.content_string = content
                self._encode()
                self.is_str = True

            self._min_obj_size = CFG.G["minObjSize"]
            self._too_small = len(self.content_bytes) < self._min_obj_size

            # If after unzipping the mime type is not useful, replace it with the original mime type
            if not is_useful_mime_type(self._CFG, self.content_type) and self._original_mime_type:
                print(f"[DEBUG] TryDecode: Deduced mime type ({self.content_type}) is not useful. "
                      f"Replacing with original {self._original_mime_type}")
                self.content_type = self._original_mime_type

            if not self._too_small:
                not_doc = set(CFG.G['struct_types']).union(CFG.G['script_types']
                                                   ).union(CFG.G['string_types']
                                                   ).union(CFG.G['media_types']
                                                   ).union(CFG.G["ignore_types"])

                is_doc = not any([fnmatch.fnmatch(self.content_type, t) for t in not_doc])
                is_struct = any([fnmatch.fnmatch(self.content_type, t) for t in CFG.G['struct_types']])
                is_ignore = any([fnmatch.fnmatch(self.content_type, t) for t in CFG.G['ignore_types']])
                is_media = any([fnmatch.fnmatch(self.content_type, t) for t in CFG.G['media_types']])

                if not self.is_str and is_doc and not is_ignore:
                    self.try_tika()

                elif not is_media and not is_ignore:
                    if self.content_bytes and not self.content_string:
                        self._step += 1
                        self.content_string, self.content_encoding = bytes_to_string(self.content_bytes, self.content_encoding)
                    if is_struct or self.content_type == 'text/plain':
                        self.parse_structured()
                # Always include compacted text if possible
                self.text = split_text_lines(b_if_not_a(self.text, self.content_string), min_size=self._min_obj_size)
            else:
                self.errors.append(f'warning: content too small {len(self.content_bytes)} < {self._min_obj_size}')

    def _p_error(self, pmsg):
        if VERBOSE:
            print(f'[DEBUG] TryDecode {pmsg}')
        self.errors.append(pmsg)

    def try_tika(self):
        global ExTika

        if VERBOSE:
            print(f"[DEBUG] TryDecode.try_tika; Tika extract from mime type {self.content_type}")

        self._step += 1
        x = None
        y = None

        if self._ExTika and self._ExTika.enabled:
            if self.is_str and len(self.content_string):
                x = self._ExTika.tika_text_from_buffer(self.content_string, from_file=False, mime_type=self.content_type)

                with open("tempfile", "w") as fout:
                    fout.write(self.content_string)

            elif not self.is_str and len(self.content_bytes):
                x = self._ExTika.tika_text_from_buffer(self.content_bytes, from_file=False, mime_type=self.content_type)
                with open("tempfile", "wb") as fout:
                    fout.write(self.content_bytes)

            if x:
                if x.message and not x.text:
                    self._p_error(x.message)
                self.text = x.text
                self.content_type = b_if_not_a(self.content_type, x.mime_type)

        # Adding parsers used by the ragchat langchain demo application to try to get better matching.
        try:
            if 'pdf' in self.content_type:
                y = PyPDFLoader("tempfile").load()
            elif 'doc' in self.content_type:
                y = Docx2txtLoader("tempfile").load()
            elif 'text' in self.content_type:
                y = TextLoader("tempfile").load()
        except Exception as err:
            self.errors.append(f"[WARNING]: {self._step} try_tika while loading with langchain {err}")
        else:
            for doc in y:
                self.text += doc.page_content
                self.text += LF

        self.text = normalize(self.text)

        # Remove the file if we created it
        if os.path.isfile("tempfile"):
            os.remove("tempfile")

    def parse_structured(self):
        if VERBOSE:
            print(f"[DEBUG] TryDecode.parse_structured Mime type is '{self.content_type}; {self.charset}'")
        if "xml" in self.content_type:
            self.un_xml()
        elif "json" in self.content_type:
            self.un_json()
        elif "yaml" in self.content_type:
            self.un_yaml()
        # elif self.content_type in ["text/plain", "application/octet-stream", ""]:
        else:
            if not self.un_json():
                if not self.un_xml():
                    self.un_yaml()

    def _decode(self):
        """
        Decompress incoming bytes if we find it's a compressed object by checking the initial 'magic bits'.
        Resolve new mime_type of decompressed object.
        """
        global ExTika

        self.content_encoding, _ = _check_compressed(self.content_bytes[0:20], self.content_type)

        if self.content_encoding == 'gzip' and self._un_gzip()\
                or self.content_encoding == 'zip' and self._un_zip():

            if mime_check_available:
                with open("temp_mimetype_check.test", "wb") as ftest:
                    ftest.write(self.content_bytes)
                typeobj = mimetypes.get_type("temp_mimetype_check.test")
                self.content_type = typeobj.mimetype_file
                if DEBUG:
                    print(f'.  Uncompressed content mime-type is "{self.content_type}"')

            self.content_updated = True
            self._step += 1
            self._not_compressed = True

        elif self.content_encoding not in ['gzip', 'zip', '']:
            print(f'[DEBUG] TryDecode._decode: Got unexpected content_encoding type "{self.content_encoding}"')
            self._not_compressed = True

        if isinstance(self.content_type, list):
            print(f'[DEBUG] TryDecode._decode: Got content_type in list "{self.content_type}"')
            self.content_type = ' '.join(self.content_type)

        if VERBOSE and self.content_encoding:
            print(f"[DEBUG] TryDecode._decode [{self._step}] mime type is '{self.content_type}' "
                  f"and check compression returned {self.content_encoding}")

    def _encode(self):
        if not self._too_small:
            if self.content_string:
                self._step += 1
                try:
                    self.content_bytes = self.content_string.encode('utf-8')
                except Exception as err:
                    self._p_error(f"warning: {self._step} _encode {err}")
                    return False
                else:
                    return True
        else:
            self._p_error(f'warning: content too small {len(self.content_string)} < {self._min_obj_size}' )
            return False

    def _un_base64(self, content):
        self._step += 1
        try:
            self.content_bytes = base64.b64decode(content)
            if DEBUG:
                print(f"[DEBUG] TryDecode._un_base64 produced {len(self.content_bytes)} bytes")
        except (binascii.Error, ValueError, TypeError) as err:
            print(f'.  [WARNING] Base64 = {self._b64} but decode FAILED: {str(err):.60s}')
            self.errors.append(f"warning: {self._step} Base64Decode {err}")

    def _get_sha256(self):
        self._step += 1
        try:
            hash_sha256 = hashlib.sha256(self.content_bytes)
            self.pre_sha256 = hash_sha256.hexdigest()
        except Exception as err:
            self.pre_sha256 = None
            self._p_error(f"warning: {self._step} hashlib {err}")

    def _un_gzip(self):
        self._get_sha256()

        self._step += 1
        try:
            nbytes = len(self.content_bytes)
            self.content_bytes = gzip.decompress(self.content_bytes)
            if DEBUG:
                print(f'.  Content GZIP decompressed: {nbytes} bytes -> {len(self.content_bytes)} bytes')
            self.content_decompressed = self.pre_sha256
            self._not_compressed = True
            return True
        except Exception as err:
            self._p_error(f"warning: {self._step} un_gzip {err}")
            return False

    def _un_zip(self):
        print(f'[WARNING] TryDecode._un_zip files is NOT YET FUNCTIONAL')
        self._get_sha256()

        self._step += 1
        try:
            nbytes = len(self.content_bytes)
            zinfo = zipfile.ZipFile(io.BytesIO(self.content_bytes))
            for f in zinfo.filelist:
                self._not_compressed += zinfo.read(f)
            if DEBUG:
                print(f'.  ZIP decompress SUCCEEDED: {nbytes} bytes -> {len(self.content_bytes)} bytes')
            self.content_decompressed = self.pre_sha256
            return True
        except Exception as err:
            self._p_error(f"warning: {self._step} un_zip {err}")
            return False

    def un_xml(self):
        self._step += 1
        start = self.content_string.find("<?xml")
        if start >= 0:
            try:
                x_dict = xmltodict.parse(self.content_string[start:], process_namespaces=True)
                self.xml_dict = dict(x_dict)
            except Exception as err:
                self._p_error(f"warning: {self._step} un_xml {err}")
                return False
            else:
                self.flatten()
                if DEBUG:
                    print(f'.  XML parse SUCCEEDED {len(self.flat_dict)} Keys')
                return True
        else:
            self._p_error(f"warning: {self._step} un_xml no '<?xml' found")
            return False

    def un_json(self):
        self._step += 1
        start = self.content_string.find('{')
        if start >= 0:
            try:
                j_dict = json.loads(self.content_string[start:])
                self.json_dict = dict(j_dict)
            except Exception as err:
                self._p_error(f"warning: {self._step} un_json {err}")
                return False
            else:
                self.flatten()
                if DEBUG:
                    print(f'.  JSON parse SUCCEEDED {len(self.flat_dict)} Keys')
                return True
        else:
            self._p_error(f"warning: {self._step} un_json no '{{' found")
            return False

    def un_yaml(self):
        self._step += 1
        try:
            y_dict = yload(self.content_string, Loader=SafeLoader)
            self.yaml_dict = dict(y_dict)
        except Exception as err:
            self._p_error(f"warning: {self._step} un_yaml {err}")
            return False
        else:
            self.flatten()
            if DEBUG:
                print(f'.  YAML parse SUCCEEDED {len(self.flat_dict)} Keys')
            return True

    def dump_keys(self, typ='b'):
        """
        Generate formatted key-value pairs and additional information from `self.flat_dict`.

        This method iterates over the key-value pairs in `self.flat_dict` and yields
        various formatted representations of the key-value pairs based on the specified
        `typ` parameter.

        Parameters:
        - typ (str): The type of formatting to apply. Default is 'b'.
         - If `typ` is 'b', the key-value pairs are yielded as bytes objects,
           handling encoding errors by yielding an empty bytes object.
         - If `typ` is not 'b' (e.g., 's' for string), the key-value pairs are
           yielded as strings, handling decoding errors by calling the
           `bytes_to_string_y` function.

        Yields:
        - If the value is a string:
         - The formatted key-value pair `k + ': ' + v`.
         - The value `v` itself.
         - If `v` contains multiple lines (i.e., `v.splitlines()[0] != v`),
           each line of `v` is yielded separately.
        - If the value is a bytes or bytearray object:
         - The formatted key-value pair `k + b': ' + v`.
         - The value `v` itself.
         - If `v` contains multiple lines (i.e., `v.splitlines()[0] != v`),
           each line of `v` is yielded separately.

        The `self.content_encoding` attribute is used as the preferred encoding for
        encoding and decoding the key-value pairs. If it is not set, the default
        encoding of 'utf-8' is used.
        """
        for k, v in self.flat_dict.items():
            if isinstance(v, str):
                s = k + ': ' + v
                if typ == 'b':
                    try:
                        yield s.encode(self.content_encoding or 'utf-8', errors='ignore')
                    except UnicodeEncodeError as err:
                        yield b''
                    else:
                        try:
                            yield v.encode(self.content_encoding or 'utf-8', errors='ignore')
                        except UnicodeEncodeError as err:
                            yield b''
                        else:
                            if v.splitlines() and v.splitlines()[0] != v:
                                for line in v.splitlines():
                                    try:
                                        yield line.encode(self.content_encoding or 'utf-8', errors='ignore')
                                    except UnicodeEncodeError as err:
                                        yield b''
                else:
                    yield s
                    yield v
                    if v.splitlines() and v.splitlines()[0] != v:
                        for line in v.splitlines():
                            yield line
            if isinstance(v, (bytes, bytearray)):
                s = k + b': ' + v
                if typ == 'b':
                    yield s
                    yield v
                    if v.splitlines() and v.splitlines()[0] != v:
                        for line in v.splitlines():
                            yield line
                else:
                    try:
                        yield s.decode(self.content_encoding or 'utf-8')
                    except UnicodeDecodeError as err:
                        yield bytes_to_string_y(s, self.content_encoding or 'utf-8')
                    try:
                        yield v.decode(self.content_encoding or 'utf-8')
                    except UnicodeDecodeError as err:
                        yield bytes_to_string_y(v, self.content_encoding or 'utf-8')
                    if v.splitlines() and v.splitlines()[0] != v:
                        for line in v.splitlines():
                            try:
                                yield line.decode(self.content_encoding or 'utf-8')
                            except UnicodeDecodeError as err:
                                yield bytes_to_string_y(line, self.content_encoding or 'utf-8')

    def flatten(self, d=None, sep="."):
        if d is None:
            d = {}
            if len(self.xml_dict): d = self.xml_dict
            elif len(self.json_dict): d = self.json_dict
            elif len(self.yaml_dict): d = self.yaml_dict
        self.flat_dict = collections.OrderedDict()

        def recurse(t, parent_key=""):
            if isinstance(t, list):
                for i in range(len(t)):
                    recurse(t[i], parent_key + sep + str(i) if parent_key else str(i))
            elif isinstance(t, dict):
                for k, v in t.items():
                    if isinstance(v, str) and any(tag in v for tag in langchain_inprompt_tags):
                        # Split the value into a dictionary based on the langchain_inprompt_tags
                        split_dict = {}
                        current_key = None
                        for line in v.split("\n"):
                            # print(line)
                            for tag in langchain_inprompt_tags:
                                if line.startswith(tag):
                                    current_key = tag
                                    split_dict[current_key.strip(':')] = line[len(tag):].strip()
                                    break
                            else:
                                if current_key and split_dict[current_key.strip(':')]:
                                    split_dict[current_key.strip(':')] += "\n" + line.strip()
                                elif current_key and not split_dict[current_key.strip(':')]:
                                    split_dict[current_key.strip(':')] = line.strip()
                                else:
                                    # If the line doesn't start with any tag, append "Command:" to it
                                    current_key = "Command:"
                                    split_dict[current_key.strip(':')] = line.strip()
                        recurse(split_dict, parent_key + sep + k if parent_key else k)
                    else:
                        recurse(v, parent_key + sep + k if parent_key else k)
            else:
                self.flat_dict[parent_key] = normalize(t)

        recurse(d)
        return self.flat_dict


# TODO: Replace TIka with https://medium.com/kx-systems/rag-llamaparse-advanced-pdf-parsing-for-retrieval-c393ab29891b
class Extract:
    tika_endpoint = ''
    no_tika_server = 0
    tika = None
    enabled = True
    mime_type = ''
    meta = {}
    text = ''
    status = 500
    charset = ''
    message = ''
    length = 0

    def __init__(self, CFG):
        self._CFG = CFG
        self.tika = init_tika(CFG)

        if not self.tika or not isinstance(self.tika, dict) or not self.tika.get("initialized", False):
            self.enabled = False
            print(f'Apache Tika server unavailable or disabled by config.')
        else:
            self.tika_endpoint = self.tika.get("url") or self.tika.get("urls")[0] or self.tika.get("client")

    @retry((socket.timeout, ConnectionError, ReadTimeoutError, ReadTimeout), total_tries=3)
    def tika_text_from_buffer(self, buff, from_file=False, mime_type='', charset=''):

        if not self.enabled:
            self.message = 'warning: Tika not enabled'
            return self

        self.text = ''
        self.message = ''
        self.mime_type = ''
        self.meta = {}

        pct = parse_content_types(mime_type, charset)
        self.mime_type = b_if_not_a(pct.get("mime"), charset)
        self.charset = b_if_not_a(pct.get("charset"), charset)

        if len(buff) < 128 and not from_file:
            if DEBUG:
                print(f'.  Extract.tika_text_from_buffer: Data buffer length is too small ({len(buff)} < 128)')
            self.message = f'warning: content too small {len(buff)} < 128)'
            return self

        try:
            if not from_file:
                response = parser.from_buffer(buff, serverEndpoint=self.tika_endpoint,
                                              requestOptions={'timeout': 15, 'verify': False,
                                                              'headers': {"content-type": mime_type}})
            else:
                response = parser.from_file(buff, serverEndpoint=self.tika_endpoint,
                                            requestOptions={'timeout': 15, 'verify': False,
                                                            'headers': {"content-type": mime_type}})
        except Exception as err:
            if DEBUG:
                print(f'.  Extract.tika: Extract failed -> {err}')
            self.message = f'error: extract failed {err}'
            return self

        self.meta = response.get("metadata", {})
        self.text = response.get('content', '')
        self.status = response.get('status', 200)

        if self.meta:
            charset = b_if_not_a(self.meta.get("Content-Encoding"), charset)
            if isinstance(self.meta.get("Content-Type"), list):
                pct = parse_content_types(b_if_not_a(self.meta.get("Content-Type-Override"),
                                                     self.meta.get("Content-Type")[0]), charset)
            else:
                pct = parse_content_types(b_if_not_a(self.meta.get("Content-Type"), mime_type), charset)
            self.mime_type = pct["mime"]
            self.charset = pct["charset"]
            tika_parser = self.meta.get('X-TIKA:Parsed-By', [])
            if 'org.apache.tika.parser.microsoft.ooxml.OOXMLParser' in tika_parser:
                self._ooxmlparser()
            elif 'org.apache.tika.parser.pdf.PDFParser' in tika_parser:
                self._pdfparser()

        else:
            self.mime_type = mime_type
            self.charset = charset

        self.length = len(self.text) if self.text is not None else 0
        print(f'.  TIKA extracted {self.length} of type {self.mime_type}')
        return self

    def _ooxmlparser(self):
        tika_app = self.meta.get('extended-properties:Application', '')
        # Characters excludes leading and trailing newlines.
        characters = self.meta.get('meta:character-count-with-spaces', -1)
        resource_names = self.meta.get('resourceName', [])
        resource_names = [resource_names] if isinstance(resource_names, str) else resource_names
        for rn in resource_names:
            self.text.replace(rn, '')
        self.text = self.text.strip() if isinstance(self.text, (str, bytes, bytearray)) else ''

    def _pdfparser(self):
        chars_per_page = self.meta.get('pdf:charsPerPage', [])
        num_pages = self.meta.get('xmpTPg:NPages', [])
        self.text = self.text.strip() if isinstance(self.text, (str, bytes, bytearray)) else ''

    # TODO: Incorporate image fingerprinting. Check alternative image comparison https://github.com/yahoo/blink-diff

    # def create_image_hash(self, file):
    #     img = Image.open(file)
    #     h1 = imagehash.average_hash(img)
    #     h2 = imagehash.phash(img)
    #     h3 = imagehash.dhash(img)
    #     h4 = imagehash.whash(img)
    #     h5 = imagehash.whash(img,  mode='db4')
    #     h6 = imagehash.colorhash(img)
    #     # h7 = imagehash.crop_resistant_hash(img)
    #     print(f"h1:{len(str(h1))} h2:{len(str(h2))} h3:{len(str(h3))} h4:{len(str(h4))} h5:{len(str(h5))} h1:{len(str(h6))}")
    #     out = f"{str(h1)}, {str(h2)}, {str(h3)}, {str(h4)}, {str(h5)}, {str(h6)}"
    #     out = str(h1) + str(h2) + str(h3) + str(h4) + str(h5) + str(h6)
    #     return out
    #
    # def img_hash_compare(self, a, b):
    #     hdiff = []
    #     # hlen is the lengths of the hashes created in create_image_hash
    #     hlen = [16, 16, 16, 16, 49, 11]
    #     n = 0
    #
    #     for l in hlen:
    #         d = imagehash.hex_to_hash(a[n:n+l-1]) - imagehash.hex_to_hash(b[n:n+l-1])
    #         n += l
    #         hdiff.append(d)
    #         print(l, n)
    #
    #     print(hdiff)
    #     return


ExTika: Extract = None


# TODO: Research using https://github.com/fomy/destor with AE as an alternative to
#   Rabin-Karp rolling hash.


def extract_and_index(CFG, content: (bytes, bytearray, str, FileNames), index_file_name: str=None,
                      b64: bool = False, content_type: (str, dict)=None, expected_hash=None, return_hashlist=False):
    global ExTika
    global bytes_per_hash

    if ExTika is None:
        ExTika = Extract(CFG)

    if isinstance(content_type, dict):
        obj_mime = content_type.get("mime", "")
        charset = content_type.get('charset', 'utf-8')
    else:
        obj_mime = content_type
        charset = ''

    if isinstance(expected_hash, str) and expected_hash in CFG.G["nullMsgSha256s"].values():
        expected_hash = None

    # Prepare a default return dictionary. Running a SHA-256 with no data gives the value below.
    ret_dict = {'data.index.name': f'<no data:{content.bksq.get("S", "")}>', 'data.bytes': -1,
                'data.content.raw': None, 'data.content.key_vals': None, 'data.content.text': None,
                'data.sha256': CFG.G["nullMsgSha256s"]["sha_no_data"],
                'data.index.time.last_modified': pd.NaT, 'data.mime_type': obj_mime,
                'data.index.de_dupe': 0, 'data.nmers.primary': 0, 'data.nmers.total': 0, 'message': ''}

    fnobj: FileNames = None
    obj_enc = ''

    print(f"BEGIN Extract and Index: ")

    # Content can be a file (string) or a buffer (bytes), or a FileNames object.
    if isinstance(content, FileNames):
        if not content.object.remote.exists() and content.body.remote.exists():
            if not content.body.local.exists():
                content.body.pull()
            in_file = content.body.local.name
            obj_len = content.body.local.length
            obj_mime = pick_best_mime_type(CFG, obj_mime, content.body.local.content_type)
            obj_enc = content.body.local.content_encoding
        elif content.object.remote.exists():
            if not content.object.local.exists():
                content.object.pull()
            in_file = content.object.local.name
            obj_len = content.object.local.length
            obj_mime = pick_best_mime_type(CFG, obj_mime, content.object.local.content_type)
            obj_enc = content.object.local.content_encoding
        else:
            # Setting name to null invalidates the index
            content.index.remote.name = ''
            if content.object.remote.deleted or content.body.remote.deleted:
                ret_dict.update({'message': 'marked_deleted_warning'})
                print(f".  Indexing skipped. Object marked as deleted.")
            else:
                ret_dict.update({'message': 'does_not_exist_warning'})
                print(f".  Indexing skipped. Object does not exist.")
            return content, ret_dict

        ret_dict.update({'data.mime_type': obj_mime})
        from_file = True
        buff = in_file
        fnobj = content

    elif isinstance(content, (bytes, bytearray)):
        obj_len = len(content)

        from_file = False
        buff = content
        in_file = io.BytesIO(content)
        in_file.name = 'content_buffer.bin'

    else:
        in_file = content
        buff = in_file
        obj_len = os.path.getsize(in_file)
        from_file = True

    if not isinstance(obj_len, (int, float)) or obj_len < CFG.G["minObjSize"]:
        # print(f"[INFO] Indexing failed for '{in_file}'")
        ret_dict.update({'message': 'object_length_too_small_warning'})
        print(f".  Indexing skipped. Object length is {obj_len} <= {CFG.G['minObjSize']}.")
        return fnobj, ret_dict

    pct = parse_content_types(obj_mime, obj_enc)
    obj_mime = pct.get("mime", obj_mime)
    obj_enc = pct.get('charset', obj_enc)

    if DEBUG:
        print(f".  {obj_len} bytes of type '{obj_mime}'")

    content_decoded = TryDecode(CFG, buff, from_file=from_file, b64=b64, content_type=obj_mime,
                                content_encoding=obj_enc, charset=charset)

    if fnobj is None:
        if index_file_name is None or index_file_name == '':
            raise RuntimeError(f'No index file name provided')
        else:
            fnobj = FileNames(index_file_name)

    if content_decoded.content_decompressed:  # Send up the sha256 of the object before it was decompressed
        print(f".  Content decompressed.")
        ret_dict.update({'object.flag.decompressed': content_decoded.content_decompressed})

    if content_decoded.content_type:
        obj_mime = content_decoded.content_type

    # Errors and lack of content_decoded.flat_dict only mean the content was not structured
    if content_decoded.errors:
        failed = [e for e in content_decoded.errors if 'error' in e]
        if failed:
            ret_dict.update({'tika_extract_error': failed[0]})
        if not content_decoded.flat_dict and CFG.me("logLevel") in ['verbose']:
            print(f".  Content type '{obj_mime}' is not JSON, YAML, or XML: \n {content_decoded.errors}")

    if content_decoded.charset:
        ret_dict.update({'object.mime_type': f"{content_decoded.content_type}; {content_decoded.charset}"})
    else:
        ret_dict.update({'object.mime_type': content_decoded.content_type})

    if content_decoded.content_bytes:
        fnobj.body.local.write_bytes(content_decoded.content_bytes)
        obj_len = fnobj.body.local.length
        ret_dict.update({'data.content.raw': fnobj.body.local.name})

    # We'll learn the average bytes per hash but want to pre-load and bias to the expected value in the CFG file
    # in case early learned values are outliers.
    if not bytes_per_hash or isinstance(bytes_per_hash, list) and len(bytes_per_hash) == 0:
        bytes_per_hash = [CFG.G['aveDedupe']] * 16
    ave_bph = sum(bytes_per_hash) / len(bytes_per_hash)

    if content_decoded.flat_dict:
        struct = json.dumps(content_decoded.flat_dict, cls=extEncoder)
        len_struct = len({k: v for k, v in content_decoded.flat_dict.items() if v is not None})
        # ret_dict.update({'data.content.key_vals': struct})
        fnobj.keys.local.write_text(struct)
    else:
        len_struct = 0

    if content_decoded.text:
        if isinstance(content_decoded.text, list):
            len_text = len(b''.join(content_decoded.text))
            slots = ((obj_len + len_text) / ave_bph) + len_struct + len(content_decoded.text)
        else:
            len_text = len(content_decoded.text)
            slots = ((obj_len + len_text) / ave_bph) + len_struct
    else:
        len_text = 0
        slots = ((obj_len + len_text) / ave_bph) + len_struct

    # number of hashes we expect for this object
    l2slots = max(math.ceil(math.log(slots * 2.5, 2)), 10)

    if DEBUG:
        print(f".  Expect {int(slots * 2.5)} slots or 2^{l2slots} at a {int(ave_bph)}:1 bytes per sequence ratio")
        print(f'.  Initializing local index file {fnobj.index.local.name}')

    rc.set(enter_sha256="niether" if not CFG.D['RKCQF']["enterSha256nmers"] else "",
           debug="verbose" if VERBOSE else "")

    r = rc.QFinit(fnobj.index.local.name, initialize=True, read_only=False, key_bits=CFG.D['RKCQF']['keyBits'],
                  value_bits=CFG.D['RKCQF']['valBits'], log2slots=l2slots)
    if not r:
        raise RuntimeError(f'[ERROR] Failed to initialize local index file. QFinit returned {r}')

    if VERBOSE:
        retdict = rc.get()
        print(f".  QFinit returned {r} slots: rk_init={retdict['rk_init']} qf_init={retdict['qf_init']}"
              f" and debug={retdict['debug']}")

    stats = {}
    mode = ("fp-insert-val", 0)
    if CFG.D['RKCQF']['keyFunc'] == 0 or CFG.D['RKCQF']['keyFunc'] == "fp-insert-val":
        mode = ("fp-insert-val", 0)
    elif CFG.D['RKCQF']['keyFunc'] == 1 or CFG.D['RKCQF']['keyFunc'] == "fp-insert-seq":
        mode = ("fp-insert-seq", 1)
    elif CFG.D['RKCQF']['keyFunc'] == 2 or CFG.D['RKCQF']['keyFunc'] == "fp-insert-lnk":
        mode = ("fp-insert-lnk", 2)

    ddratio = 0
    hashlist = []

    try:
        if return_hashlist or CFG.G.get("keepHashFiles", False):
            stats = rc.fileCmd(fnobj.body.local.name, fnobj.hashlist.local.name, value=0, command=mode[0])
        else:
            stats = rc.fileCmd(fnobj.body.local.name, value=0, command=mode[0])
    except (ValueError, FileNotFoundError, TypeError) as err:
        # We pulled the object to local ok, but rkcqf can't open it
        rc.QFclose()
        print(f'[ERROR] Had a problem here {str(err):.60s}')
        ret_dict.update({'message': 'index_error'})
        return content, ret_dict

    tot_bytes = stats["bytes_read"]
    pri_hash_count = stats["hashes_inserted"]

    retdict = rc.get()
    ext = len(retdict.get('shalist', []))
    pre_expected = pri_hash_count + ext if CFG.D["RKCQF"]["enterSha256nmers"] else 0
    pre_occslots = retdict.get('occ_slots', -1)
    pre_nmerspri = retdict.get('nmers_pri', -1)
    pre_nmersext = retdict.get('nmers_ext', -1)

    # Debug output to help get nmer counts correct
    check = ""
    if pre_expected and pre_expected != pre_occslots:
        check = f" (Expected {pre_expected})"
    print(f".  Inserted {tot_bytes} bytes -> {pri_hash_count} sequences -> {pre_occslots}{check} slots"
          f" -> {pre_nmerspri}:{pre_nmersext} nmers pri:sec")

    rc.checkpoint()    # Calculate and insert the SHA256 for the object hashes just inserted.
    txt_hash_count = 0   # At this point we should have

    if DEBUG:
        # Debug output to help get nmer counts correct
        retdict = rc.get()
        ext = len(retdict.get('shalist', [])) + len(retdict.get('shalistext', []))
        post_expected = pri_hash_count + ext if CFG.D["RKCQF"]["enterSha256nmers"] else 0
        post_occslots = retdict.get('occ_slots', -1)
        post_nmerspri = retdict.get('nmers_pri', -1)
        post_nmersext = retdict.get('nmers_ext', -1)
        check = ""
        if post_expected != post_occslots:
            check = f"(Expected {post_expected}!)"
        # print(f".  [DEBUG] After rc.checkpoint() {post_occslots}{check} slots"
        #       f" -> {post_nmerspri}:{post_nmersext} nmers pri:sec")

    #
    #  Do the insertion of extracted text into the CQF
    #
    if len_text and not len_struct:
        hashkey = {}
        if isinstance(content_decoded.text, (bytes, bytearray)):
            fnobj.text.local.write_text(content_decoded.text.decode('utf-8'))
            r = rc.databuf_insert(content_decoded.text, value=0, sequence=mode[1], sha_update=0)
            tot_bytes += len_text
            hashlist.extend(r)
            txt_hash_count = len(set(r))
            print(f".  Inserted {txt_hash_count} sequences from {len_text} extracted text bytes")

            if CFG.G.get("keepTextFiles", False):
                fnobj.text.push()
                ret_dict.update({'data.content.text': fnobj.text.remote.name})
                # print(f".  Saved extracted text to {fnobj.text.remote.name}")

        elif content_decoded.text and isinstance(content_decoded.text, list):
            fnobj.text.local.write_text(b'\n'.join(content_decoded.text).decode('utf-8'))
            txt_hash_count = 0
            tbytes = 0
            for k in content_decoded.text:
                r = rc.databuf_insert(k, value=0, sequence=mode[1], sha_update=0)
                hashlist.extend(r)
                hashkey.update({r if not isinstance(r, list) else r[0]: k})
                tbytes += len(k)
                txt_hash_count += len(set(r))

            print(f".  Inserted {txt_hash_count} sequences from {tbytes} extracted text bytes"
                  f" in list of {len(content_decoded.text)} items")

            tot_bytes += tbytes
            if CFG.G.get("keepTextFiles", False):
                fnobj.text.push()
                ret_dict.update({'data.content.text': fnobj.text.remote.name})
                # print(f".  Saved extracted text to {fnobj.text.remote.name}")

            fnobj.text.local.delete()

        else:
            fnobj.text.local.write_text(content_decoded.text)
            raise TypeError("content_decoded.text should always be of type BYTES or list of byte strings")

    #
    #  Do the insertion of extracted keys into the CQF
    #
    # FIXME: For structured (JSON, YAML, etc) content, there's no point indexing the JSON as a whole
    #  since the ordering of keys doesn't matter.
    # TODO: k is of the form b'ocs.meta.status: ok' - should have a filter set to scan particular keys
    #  or to look for object names
    # TODO: Explore the idea of locally scoped byte-sequences.  For example, if we have a sequence that has strong
    #  relevance to a particular service, but would be noise in the context of the entire corpus of data in the customer
    #  environment, local scope would allow us to track the sequence in the context of the service, but not outside of it.
    #  This has come up when looking at user input prompts that a service will add context to (e.g. from RAG) but
    #  that are short.  We want to track the user prompt data from the input API to the API the service calls on behalf of
    #  the user to connect the two.
    key_hash_count = 0
    if len_struct:
        kbytes = 0
        keybuf = []
        hashkey = {}
        n = 0
        # Build a list of (key:value, value) tuples, then unpack the tuples into separate items and include only
        # those where the value is greater than the minObjSize. Then insert each item into the CQF.
        # kdump = content_decoded.dump_keys()   # Returns bytes
        # keyvals = [(k, k.split(b':', 1)[-1].strip(b' ,')) for k in kdump]
        # keyvals = [item for tup in keyvals for item in tup if isinstance(tup[1], (bytes, bytearray)) and len(tup[1]) > CFG.G.get("minObjSize", 128)]
        for k in content_decoded.dump_keys():
            if len(k) < CFG.G.get("minObjSize", 128):
                continue
            if VERBOSE:
                print(f'.  .  Inserting {len(k)} bytes in cqf from key {k.split(b":")[0]}')
            r = rc.databuf_insert(k, value=0, sequence=mode[1], sha_update=0)
            kbytes += len(k)
            keybuf.append(k)
            hashlist.extend(r)
            hashkey.update({r if not isinstance(r, list) else r[0]: k})
            key_hash_count += len(set(r))
            n += 1

        tot_bytes += kbytes

        if key_hash_count:
            print(f".  Inserted {key_hash_count} nmers from {kbytes} bytes in {n} extracted keys ")

            if CFG.G.get("keepKeysFiles", False) and keybuf:
                fnobj.keys.push()
                ret_dict.update({'data.content.key_vals': fnobj.keys.remote.name})
                print(f".  Saved extracted keys to {fnobj.keys.remote.name}")

            fnobj.keys.local.delete()

    if len(hashlist) > 0:
        if return_hashlist or CFG.G.get("keepHashFiles", False):
            # Can't use fnobj.hashlist.local.write_bytes() since the operation is 'append'
            with open(fnobj.hashlist.local.name, 'a') as fout:
                fout.write(str(hashlist))
            if CFG.G.get("keepHashFiles", False):
                fnobj.hashlist.push()
                ret_dict.update({'data.content.hashlist': fnobj.hashlist.remote.name})
                print(f".  Saved hashlist to {fnobj.hashlist.remote.name}")
            if return_hashlist:
                hl = fnobj.hashlist.local.read_text()
                if "][" in hl:
                    hl = hl.replace("][", ", ")
                hashlist = json.loads(hl)
            fnobj.hashlist.local.delete()

    if len(fnobj.body.remote.name) < 256:
        rc.set(obj_name=fnobj.body.remote.name)
    else:
        print(f"[WARNING] Object name 'fnobj.body.remote.name' is too long for RKCQF ({len(fnobj.body.remote.name)} bytes)\n{fnobj.body.remote.name}")
    retdict = rc.get()

    pri_nmers = retdict.get('nmers_pri', 6666)   # - len(p.get('shalist', 0)) - len(p.get('shalistext', 0)) - sec_set_len
    sec_nmers = retdict.get('nmers_ext', 9999)

    if CFG.D['RKCQF']["enterSha256nmers"]:
        post_expected = pri_hash_count + len(hashlist) + len(retdict.get('shalist', []))\
                                                       + len(retdict.get('shalistext', []))
        len_sha_ext = len(retdict.get('shalistext', []))
    else:
        post_expected = pri_hash_count + len(hashlist)
        len_sha_ext = 0

    if DEBUG:
        # Debug output to help get nmer counts correct
        post_occslots = retdict.get('occ_slots', -1)
        post_nmerspri = retdict.get('nmers_pri', -1)
        post_nmersext = retdict.get('nmers_ext', -1)
        check = ""
        if post_expected != post_occslots:
            check = f"(Expected {post_expected}!)"
        # print(f".  [DEBUG] After insert text/keys {post_occslots}{check} slots"
        #       f" -> {post_nmerspri}:{post_nmersext} nmers pri:sec")

    if pri_nmers > 0:
        ddratio = tot_bytes / (sec_nmers * (CFG.D['RKCQF']['keyBits'] + CFG.D['RKCQF']['valBits']) / 8)
        bytes_per_hash.append(int(tot_bytes / post_expected))
        print(f'.  Extract and index complete: {int(tot_bytes / post_expected)} bytes per hash')
    else:
        print(f'.  Extract and index complete: No sequence hashes generated')

    # This sha256 will allow us to match other identical objects with different names
    sha256 = retdict.get('sha256', b'').hex()

    if not content_decoded.content_updated:
        if isinstance(expected_hash, str) and expected_hash and expected_hash != sha256:
            print(f"[WARNING] Index file SHA256 and expected SHA256 are not the same ( & content not decompressed)\n"
                  f"          Expected: {expected_hash}   <--- Probably from X-Amz-Content-Sha256\n"
                  f"             Index: {sha256}")

    if '000000000' in sha256:
        print(f"[WARNING] Index file '{fnobj.index.local.name}' SHA256 should not be {sha256}")

    del content_decoded

    rc.QFclose()

    if return_hashlist:
        return hashlist

    write_time = datetime.now(timezone.utc)

    ret_dict.update({'data.index.name': fnobj.index.remote.name,
                     'data.bytes': obj_len,
                     'data.sha256': sha256,
                     'data.mime_type': obj_mime,
                     'data.nmers.primary': pri_nmers,
                     'data.nmers.total': sec_nmers + len_sha_ext + txt_hash_count + key_hash_count,
                     'data.content.length.text': len_text,
                     'data.content.length.key_val': len_struct,
                     'data.index.time.last_modified': write_time,
                     'data.index.de_dupe': ddratio,
                     'message': 'new_index'})

    if return_hashlist:
        retdict |= {'data.nmers.list': hashlist}

    return fnobj, ret_dict
