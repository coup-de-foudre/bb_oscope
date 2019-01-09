import tempfile
import time
import threading
import os

import zmq

import oscope.base

IPC_PATH_MAX_LEN = 107


class IPCTemp:
    """
    This class provides unique and sanitary IPC addresses
    on the local filesystem.  It is designed to be used
    as a context manager in the following pattern:

    >>> with IPCTemp(["foo", "bar"]) as (foo_path, bar_path):
    >>>    socket1.bind(foo_path)
    >>>    socket2.bind(bar_path)

    On exit of the block, the context manager will ensure deletion
    of the root folder as well as any sockets found within it.
    Each path from a particular invocation has a unique
    directory prefix, so this context manager can be used in a
    nested fashion without fear of name collision.
    """
    def __init__(self, ipc_names: list):
        self._ipc_names = ipc_names
        assert len(ipc_names) == len(set(ipc_names)), \
            "All ipc names must be unique:" + repr(ipc_names)

    def __enter__(self):
        self._td = tempfile.TemporaryDirectory(prefix="ipc_temp")
        self._td.__enter__()
        names = ["ipc://" + os.path.join(self._td.name, ipc_name) for ipc_name in self._ipc_names]

        for name in names:
            if len(name) >= IPC_PATH_MAX_LEN:
                self._td.cleanup()
                raise AssertionError(
                    'IPC Address name "{}" is too long: ({} chars, max is {})'.format(name, len(name), IPC_PATH_MAX_LEN))
        return names

    def __exit__(self, *args):
        self._td.__exit__(*args)


class LinkedPubSubPair():
    def __init__(self):
        self._ctx = None
        self._pub = None
        self._sub = None

    def __enter__(self):
        self._ipc_temp = IPCTemp(["pubsub-pair"])
        address = self._ipc_temp.__enter__()[0]

        self._ctx = zmq.Context.instance()
        self._pub = self._ctx.socket(zmq.PUB)
        self._pub.bind(address)
        
        self._sub = self._ctx.socket(zmq.SUB)
        self._sub.connect(address)
        self._sub.subscribe("")

        time.sleep(0.4)
        # Send some things till you get a response through
        while self._sub.poll(timeout=50) < 0:
            self._pub.send(b"ping")
        
        # Empty out the responses
        while self._sub.poll(timeout=50) > 0:
            self._sub.recv()

        return self._pub, self._sub

    def __exit__(self, *args):
        if self._pub is not None:
            self._pub.close(linger=0)
            self._pub = None
        
        if self._sub is not None:
            self._sub.close(linger=0)
            self._sub = None

        if self._ctx is not None:
            self._ctx.term()
            self._ctx = None

        self._ipc_temp.__exit__(*args)

class SubscribeSocket:
    def __enter__(self):
        self._ctx = zmq.Context().__enter__()
        self._sub = self._ctx.socket(zmq.SUB).__enter__()
        return self._sub

    def __exit__(self, *args):
        self._sub.__exit__(self, *args)
        self._ctx.__exit__(self, *args)


class PubSocket:
    def __init__(self):
        self._ctx = None
        self._pub = None

    def __enter__(self):
        self._ctx = zmq.Context().__enter__()
        self._pub = self._ctx.socket(zmq.PUB).__enter__()
        return self._pub

    def __exit__(self, *args):
        self._pub.__exit__(self, *args)
        self._ctx.__exit__(self, *args)

class NoisyPubSocket(PubSocket):
    PAYLOAD = b"foo"
    def _do_sending(self):
        while True:
            self._pub.send(self.PAYLOAD)
            self._close_event.wait(timeout=0.1)
            if self._close_event.is_set():
                break

    def __enter__(self):
        super().__init__()
        super().__enter__()

        self._close_event = threading.Event() 
        self._thread = threading.Thread(target=self._do_sending)
        self._thread.start()
        return self._pub

    def __exit__(self, *args):
        self._close_event.set()
        self._thread.join(1)
        oscope.base.assert_false(self._thread.is_alive(), "Pub Socket did not shutdown")
        super().__exit__(*args)
