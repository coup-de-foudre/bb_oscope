import json

import numpy as np

import oscope.base
import oscope.schema
import oscope.array_encoding


def package_trace_data(metadata: dict, trace: np.ndarray) -> tuple:
    oscope.schema.validate_message_metadata(metadata)
    encoded_header = json.dumps(metadata).encode("utf-8")
    encoded_array = oscope.array_encoding.ndarray_to_bytes(trace) 
    return (encoded_header, encoded_array)


def unpackage_trace_data(frame: tuple) -> (dict, np.ndarray):
    oscope.base.assert_length(frame, 2)
    encoded_header, encoded_array = frame

    decoded_header = json.loads(encoded_header.decode())
    oscope.schema.validate_message_metadata(decoded_header)

    decoded_array = oscope.array_encoding.bytes_to_ndarray(encoded_array)
    return decoded_header, decoded_array
