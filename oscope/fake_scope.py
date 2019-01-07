import numpy as np

import oscope.abstract_scope as abstract_scope

class FakeOscilloscope(abstract_scope.AbstractOscilloscope):
    def get_channel_sample_count(self, channel: int) -> int:
        return 1000
    
    def get_channel_sample_rate(self, channel: int) -> float:
        return 100000.0
    
    def is_channel_ready(self, channel: int) -> bool:
        return True
    
    def read_channel(self, channel: int) -> np.ndarray:
        return np.arange(self.get_channel_sample_count(channel), dtype=np.float64)
