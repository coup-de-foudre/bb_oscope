import time

import numpy as np

import oscope.base
import oscope.encoding as array_encoding
import oscope.schema_tests


def test_to_from_bytes():
    a1 = np.arange(107)
    b1 = array_encoding.ndarray_to_bytes(a1)

    a2 = array_encoding.bytes_to_ndarray(b1)
    np.testing.assert_array_equal(a1, a2)


def test_to_from_bytes_idempotence():
    a1 = np.arange(107)
    b1 = array_encoding.ndarray_to_bytes(a1)
    time.sleep(0.1)
    b2 = array_encoding.ndarray_to_bytes(a1)

    assert b1 == b2, "Idempotence check failed :("

def test_package_trace_data():
    packaged = oscope.encoding.package_trace_data(oscope.schema_tests.VALID_METADATA, oscope.schema_tests.VALID_DATA)

    for element in packaged:
        oscope.base.assert_isinstance(element, bytes)

def test_unpackage_trace_data():
    packaged = oscope.encoding.package_trace_data(oscope.schema_tests.VALID_METADATA, oscope.schema_tests.VALID_DATA)
    oscope.encoding.unpackage_trace_data(packaged)
