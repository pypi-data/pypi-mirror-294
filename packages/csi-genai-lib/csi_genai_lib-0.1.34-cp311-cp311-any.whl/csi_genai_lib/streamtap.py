# ##################################################################################################
#  Copyright (c) 2024.    Caber Systems, Inc.                                                      #
#  All rights reserved.                                                                            #
#                                                                                                  #
#  CABER SYSTEMS CONFIDENTIAL SOURCE CODE                                                          #
#  No license is granted to use, copy, or share this software outside of Caber Systems, Inc.       #
#                                                                                                  #
#  Filename:  streamtap.py                                                                         #
#  Authors:  Rob Quiros <rob@caber.com>  rlq                                                       #
# ##################################################################################################

import os
import uuid
import inspect
import hashlib

from csiMVP.Common.remote_open import ropen, validate_all_store_configs
from csiMVP.Common.init import CFG


validated = False
bsfxx = CFG.G["filenameSuffixes"]["body"].strip('.')
bsfxx = f".{bsfxx}" if bsfxx else ""
rsfxx = CFG.G["remoteSuffix"].strip('.')
rsfxx = f".{rsfxx}" if rsfxx else ""


class StreamTap:
    """
    Class initialization inputs:
    instream     (required - file-like object): The originating stream that this class will read

    temp_path    (required - string): local machine directory where the tapped byte stream will be written

    chunk      (optional - int): Number of bytes to yeild. Defaults to maxBodysize in config fiel.  If instream
                is an iterator with a fixed chunk size, chunk must equal that chunk size exactly!

    file_id  (optional - uuid): UUID used to create the file name for the tapped stream.  If not supplied
                 a machine specific uuid will be created.


    Class properties (in addition to base class properties):
    local_file   (string) Path and filename where the copy of the bytes is stored.
    remote_file  (string) Bucket, prefix, and object name of the tapped stream
    """

    def __init__(self, instream, chunk_size=1024, content_length=0, uid=None):
        global validated
        global bsfxx
        global rsfxx

        if not validated:
            validated = validate_all_store_configs(CFG.sspfx)

        self._instrm = instream
        self._bufmax = CFG.me("maxBodyLen", default=(1024 * 1024))
        self.local_name = None
        self.remote_name = None
        self.length = content_length
        self.sha256 = b''
        self._chnksz = chunk_size
        self._start = 0
        if uid is None:
            self.uid = uuid.uuid4()
        else:
            self.uid = uid
        self.result = None
        self._hash = hashlib.sha256()
        self._gen = None
        self._done = False
        self.closed = False
        self._isgen = inspect.isgenerator(instream)
        self._isstr = isinstance(instream, (bytes, bytearray))
        try:
            self._isfile = instream.readable()
        except:
            self._isfile = False

        print(f"[{self.uid[0:4]}{self.uid[-8:]}] Stream source is {type(instream).__qualname__}")

        if not self._isfile and not self._isgen and not self._isstr:
            if isinstance(instream, str):
                try:
                    self._instrm = instream.encode('utf-8')
                    self._isstr = True
                except UnicodeEncodeError:
                    raise TypeError(f"[{self.uid[0:4]}{self.uid[-8:]}] Stream source is a string that could not be encoded to bytes")
            else:
                raise TypeError(f"[{self.uid[0:4]}{self.uid[-8:]}] Stream source is not a file-like, bytes-like, or generator object {type(instream).__qualname__}")
        if not self.closed:
            self._done = False
            self.local_name = f"{CFG.localdir}/{self.uid}{bsfxx}"
            # Remote name in Caber's global shared storage (gss) NO CHARS THAT REQUIRE quote_plus HERE!!!!!!!!!
            self.remote_name = f"{CFG.rem_cori_prefix(module=CFG.M['filePrefix'])}/{self.uid}{bsfxx}{rsfxx}"
            self._ftmp = open(self.local_name, 'wb+')         # ALWAYS LOCAL - BUILT-IN OPEN
        else:
            self._done = True
        if self._isstr:
            print(f'[{self.uid[0:4]}{self.uid[-8:]}] STAP Attached to data of type BYTES chunk size = {self._chnksz}')
        if self._isfile:
            print(f'[{self.uid[0:4]}{self.uid[-8:]}] STAP Attached to data of type FILE chunk size = {self._chnksz}')
        if self._isgen:
            print(f'[{self.uid[0:4]}{self.uid[-8:]}] STAP Attached to data of type GENERATOR chunk size = {self._chnksz}')

    def read(self, chunklen=0):
        chunk = b''
        if self.closed: raise ValueError(f"[{self.uid[0:4]}{self.uid[-8:]}] Attempt to read when stream is closed")
        if not isinstance(chunklen, int):
            raise ValueError(f"[{self.uid[0:4]}{self.uid[-8:]}] Argument 'chunklen' to read(chunklen) must be of type int.")
        if self._chnksz == 0 and chunklen <= 0:   # If a chunk size was not set at init, it can be set by chunklen
            self._chnksz = self._bufmax           #   otherwise chunklen is ignored
        elif self._chnksz == 0:
            self._chnksz = chunklen

        # Enable a bytes-like object to be read like a file
        if self._isstr:
            if not self._done:
                if self._chnksz >= len(self._instrm[self._start:]):
                    chunk = self._instrm[self._start:]
                    # Process all  or the last remaining part of instrm
                    self.length += len(chunk)
                    self._ftmp.write(chunk)
                    self._hash.update(chunk)
                    self._done = True
                    print(f"[{self.uid[0:4]}{self.uid[-8:]}] STAP Sent final chunk {self.length} bytes tapped")
                else:
                    # Process the next chunk of instream
                    chunk = self._instrm[self._start:self.length]
                    self._ftmp.write(chunk)
                    self._hash.update(chunk)
                    self._start = self.length
                    self.length += len(chunk)
                    # print(f"[{self.uid[0:4]}{self.uid[-8:]}] STAP Sent {len(chunk)} byte chunk. ({self.length} bytes so far)")

        # Enable a generator to be read like a file
        elif self._isgen:
            if not self._done:
                try:
                    chunk = next(self._instrm, b'')
                    if chunk == b'':
                        raise StopIteration
                    self._ftmp.write(chunk)
                    self._hash.update(chunk)
                    self.length += len(chunk)
                    # print(f"[{self.uid[0:4]}{self.uid[-8:]}] STAP Sent {len(chunk)} byte chunk. ({self.length} bytes so far)")
                except StopIteration:
                    print(f"[{self.uid[0:4]}{self.uid[-8:]}] STAP Sent final chunk {self.length} bytes tapped")
                    self._done = True

        # Enable a file to be read like a file :)
        elif self._isfile:
            if not self._done:
                try:
                    chunk = self._instrm.read(self._chnksz)
                    if chunk == b'':
                        raise EOFError
                    self._ftmp.write(chunk)
                    self._hash.update(chunk)
                    self.length += len(chunk)
                    # print(f"[{self.uid[0:4]}{self.uid[-8:]}] STAP Sent {len(chunk)} byte chunk. ({self.length} bytes so far)")
                except EOFError:
                    print(f"[{self.uid[0:4]}{self.uid[-8:]}] STAP Sent final chunk {self.length} bytes tapped")
                    self._done = True

        else:
            print(f'[{self.uid}][ERROR] How did I get here?  instream type is {type(self._instrm)} done={self._done}')

        if self._done:
            if self._isfile:
                try:
                    if not self._instrm.closed:
                        self._instrm.close()
                except:
                    pass
        # print(f"[{self.uid}][DEBUG] Returning chunk of length={len(chunk)}")
        return chunk

    def close(self, delete_temp=True):
        fsize = 0
        fosize = 0
        if self._ftmp.seekable():
            # print(f"[{self.uid}][DEBUG] Local temp file seekable")
            fsize = self._ftmp.tell()
            fosize = os.stat(self.local_name).st_size
            self._ftmp.seek(0)
        else:
            self._ftmp.close()
            # print(f"[{self.uid}][DEBUG] Local temp file NOT seekable")
            if os.path.exists(self.local_name):
                fsize = os.stat(self.local_name).st_size
                self._ftmp = open(self.local_name, 'rb')         # ALWAYS LOCAL - BUILT-IN OPEN
            else:
                print(f"[{self.uid}][ERROR] What? Local temp file no longer exists! {self.local_name}")
                self.result = b''

        # Get the SHA256 before writing the file so we can use the SHA256 as the filename.  Common to see the same
        # data being read and written many times for the same transaction.
        # TODO: Optimization.  Ideally we would check to see if a file with the same hash exists before writing
        #    to avoid wasted cycles.  Probably best to do the check only for file lengths over a certain size
        #    since checking has a cost too.  Could also use a local lru_cache...
        # TODO: Decompress files. It might also make sense to see if a file is compressed so we don't
        #    don't compress it again when writing it via smart-open.  If we decompress here then
        #    get the sha256 we'll avoid work later on since there won't be duplicate compressed/uncompressed
        #    content to deal with.
        self.sha256 = self._hash.hexdigest()
        self.remote_name = self.remote_name.replace(self.uid, self.sha256)

        if fsize != self.length:
            print(f"[{self.uid}][WARNING] Local temp file length inconsistent {fsize}<>{fosize}<>{self.length}")

        if CFG.G.get("minObjSize", 0) < fsize <= CFG.me("maxInlineBodyLen", 0):
            self.result = self._ftmp.read()
        elif fsize >= CFG.G.get("minObjSize", 0):
            with ropen(self.remote_name, 'wb') as fout:
                print(f"[{self.uid[0:4]}{self.uid[-8:]}] STAP writing {self.length} bytes to remote {self.remote_name}")
                fout.write(self._ftmp.read())
            self.result = f"{self.remote_name}"
        else:
            self.result = b''

        self._ftmp.close()
        if delete_temp:
            os.remove(self.local_name)

        self.closed = True
        self._done = True
        return self.result

    def readable(self): return True
    def writable(self): return False
    def seekable(self): return False

    # The __iter__ and __next__ functions turn the class into a generator even though it uses
    # the read function under the covers
    def __iter__(self):
        # returning __iter__ object
        return self

    def __next__(self):
        while not self._done:
            return self.read(self._chnksz)
        if self._done:
            raise StopIteration

    def __len__(self):
        return self.length

    def __del__(self):
        if not self.closed:
            self.close()

    __call__ = __next__
