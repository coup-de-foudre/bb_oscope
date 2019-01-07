import json

import numpy as np

import oscope.schema
import oscope.support


def package_trace_data(metadata: dict, trace: np.ndarray) -> tuple:
    oscope.schema.validate_message_metadata(metadata)
    encoded_header = json.dumps(metadata).encode("utf-8")
    encoded_array = oscope.support.ndarray_to_bytes(trace) 
    return (encoded_header, encoded_array)


def unpackage_trace_data(frame: tuple) -> (dict, np.ndarray):
    assert len(frame) == 2, frame
    encoded_header, encoded_array = frame

    decoded_header = json.loads(encoded_header.decode())
    oscope.schema.validate_message_metadata(decoded_header)

    decoded_array = oscope.support.bytes_to_ndarray(encoded_array)
    return decoded_header, decoded_array
