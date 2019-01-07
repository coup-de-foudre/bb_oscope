import datetime
import time

import numpy as np

import oscope.schema


class AbstractOscilloscope(object):
    def __init__(self, name: str=None):
        self.name = name

    def get_name(self):
        if self.name is None:
            return self.__class__.__name__
        else:
            return self.name

    def get_trace_meta(samples: int, frequency: float) -> dict:
        return dict(samples=samples, frequency=frequency)

    def is_ready(self) -> bool:
        raise NotImplementedError()

    def read(self) -> np.ndarray:
        raise NotImplementedError()

    def get_sample_rate(self) -> float:
        raise NotImplementedError()

    def get_sample_count(self) -> int:
        raise NotImplementedError()

    # The above methods must be implemented by the subclass

    def block_on_ready(self, timeout: datetime.timedelta):
        if self.is_ready():
            return

        done_dt = datetime.datetime.now() + timeout
        while datetime.datetime.now() < done_dt:
            time.sleep(0.001)
            if self.is_ready():
                return
        
        raise TimeoutError("Did not become ready in {} seconds".format(timeout.total_seconds()))
