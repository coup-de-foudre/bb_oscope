import numpy as np

import oscope.fake_scope as fake_scope

def test_getters():
    scope = fake_scope.FakeOscilloscope()

    scope.get_channel_sample_count(1)
    scope.get_channel_sample_rate(1)

    scope.is_channel_ready(1)

    array = scope.read_channel(1)
    assert array.dtype == np.float64, array.dtype