import numpy as np

import oscope.trace
import oscope.schema_tests


def test_package_trace_data():
    expected_length = oscope.schema_tests.VALID_METADATA["trace"]["samples"]
    array_data = np.arange(expected_length, dtype=np.float64)

    packaged = oscope.trace.package_trace_data(oscope.schema_tests.VALID_METADATA, array_data)

    for element in packaged:
        assert isinstance(element, bytes)

def test_unpackage_trace_data():
    expected_length = oscope.schema_tests.VALID_METADATA["trace"]["samples"]
    array_data = np.arange(expected_length, dtype=np.float64)

    packaged = oscope.trace.package_trace_data(oscope.schema_tests.VALID_METADATA, array_data)

    oscope.trace.unpackage_trace_data(packaged)