import numpy as np

import oscope.scope.fake as fake_scope

def test_getters():
    scope = fake_scope.FakeOscilloscope()

    scope.get_sample_count()
    scope.get_sample_rate()

    scope.is_ready()

    array = scope.read()
    assert array.dtype == np.float64, array.dtype