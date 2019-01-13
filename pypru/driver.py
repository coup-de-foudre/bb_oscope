import os
import tempfile

import cffi

import pypru
import pypru.prussdrv as DEFINES


CDEF_FILE_PATH = os.path.join(os.path.split(pypru.__file__)[0], "prussdrv.h")


class LibraryLoader:
    DEFINES = DEFINES

    def __init__(self):
        self.ffi = cffi.FFI()
        with open(CDEF_FILE_PATH) as f:
            self.ffi.cdef(f.read())

        self.lib = self.ffi.dlopen("prussdrv")
        self.lib.prussdrv_init()

    def __getattr__(self, callname):
        if not hasattr(self.lib, callname):
            raise AttributeError(callname)
        
        unwrapped_call = getattr(self.lib, callname)

        def wrapper(*args, handle=True):
            returncode = unwrapped_call(*args)
            message = "Call {}{} returned {}".format(callname, args, returncode)

            if (returncode != 0) and (returncode is not None) and handle:
                raise ValueError(message)
            print("DEBUG:  " + message)
            return returncode

        return wrapper

    def start(self, pru: int):
        self.lib.prussdrv_pru_enable(pru)

    def stop(self, pru: int):
        self.lib.prussdrv_pru_disable(pru)

    def load_bin(self, pru: int, path: str):
        assert os.path.isfile(path), path
        self.lib.prussdrv_exec_program(pru, path)

    def close(self):
        self.lib.prussdrv_exit()

    def __del__(self):
        self.close()


# Smoketest
if __name__ == "__main__":
    ll = LibraryLoader()
    ll.start(1)
    ll.stop(1)
    ll.close()
