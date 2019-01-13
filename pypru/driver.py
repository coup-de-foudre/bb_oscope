import os

import cffi

import pypru
import pypru.prussdrv as DEFINES


CDEF_FILE_PATH = os.path.join(os.path.split(pypru.__file__)[1], "prussdrv.h")


class LibraryLoader:
    DEFINES = DEFINES

    def __init__(self):
        self.ffi = cffi.FFI()
        with open(CDEF_FILE_PATH) as f:
            self.ffi.cdef(f.read())

        self.lib = self.ffi.dlopen("prussdrv")

    def handle_error(self, return_code, callname):

    def __getattr__(self, callname):
        if hasattr(self.lib):
            raise AttributeError()
        
        unwrapped_call = getattr(self.lib, callname)
        def wrapper(*args, handle=True):
            returncode = unwrapped_call(*args)
            if (returncode != 0) and (returncode is not None) and handle:
                raise RuntimeError("Call {}({}) returned {}".format(callname, args, returncode))
            return returncode

        return wrapper


# Smoketest
if __name__ == "__main__":
    LibraryLoader().prussdrv_init()