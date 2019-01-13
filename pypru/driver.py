import os

import cffi

import pypru
import pypru.prussdrv as DEFINES


CDEF_FILE_PATH = os.path.join(pypru.__file__, "prussdrv.h")


class LibraryLoader:
    DEFINES = DEFINES

    def __init__(self):
        self.ffi = cffi.FFI()
        with open(CDEF_FILE_PATH) as f:
            self.ffi.cdef(f.read())

        self.lib = self.ffi.dlopen("prussdrv")
