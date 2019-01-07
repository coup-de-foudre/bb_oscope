import time

import numpy as np

import oscope.array_encoding as array_encoding


def test_to_from_bytes():
    a1 = np.arange(107)
    b1 = array_encoding.ndarray_to_bytes(a1)

    a2 = array_encoding.bytes_to_ndarray(b1)
    np.testing.assert_array_equal(a1, a2)


def test_idempotence():
    a1 = np.arange(107)
    b1 = array_encoding.ndarray_to_bytes(a1)
    time.sleep(0.1)
    b2 = array_encoding.ndarray_to_bytes(a1)

    assert b1 == b2, "Idempotence check failed :("
