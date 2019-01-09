import datetime
import threading
import time

import numpy as np

import oscope.schema


class AbstractOscilloscope(object):
    def __init__(self, name: str=None):
        self.name = name
        self._sender = None

    # Must be implemented by the subclass
    def is_ready(self) -> bool:
        raise NotImplementedError()

    def read(self) -> np.ndarray:
        raise NotImplementedError()

    def get_sample_rate(self) -> float:
        raise NotImplementedError()

    def get_sample_count(self) -> int:
        raise NotImplementedError()

    def get_name(self):
        if self.name is None:
            return self.__class__.__name__
        else:
            return self.name

    def get_trace_meta(self) -> dict:
        return dict(samples=self.get_sample_count(), frequency=self.get_sample_rate())

    def block_on_ready(self, timeout: datetime.timedelta):
        done_dt = datetime.datetime.now() + timeout
        while True:
            if self.is_ready():
                return
            time.sleep(0.001)
            if datetime.datetime.now() > done_dt:
                break

        raise TimeoutError("Did not become ready in {} seconds".format(timeout.total_seconds()))

    def _sender_thread_run(self):
        with oscope.network.util.PubSocket() as skt:
            while not self._stop_event.is_set():
                try:
                    self.block_on_ready(datetime.timedelta(seconds=0.1))
                except TimeoutError:
                    continue
                do_sending()

    def start_sender(self):
        assert self._sender is None, "Already running!"
        
        self._stop_event = threading.Event()
        self._sender = threading.Thread(target=self._sender_thread_run)
        self._sender.start()
