import numpy as np

import oscope.scope.abstract as abstract_scope

class FakeOscilloscope(abstract_scope.AbstractOscilloscope):
    def get_sample_count(self) -> int:
        return 1000
    
    def get_sample_rate(self) -> float:
        return 100000.0
    
    def is_ready(self) -> bool:
        return True
    
    def read(self) -> np.ndarray:
        return np.arange(self.get_sample_count(), dtype=np.float64)
