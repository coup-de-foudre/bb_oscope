import pytest
import jsonschema
import pytest

import oscope.schema as schema


VALID_METADATA = {
        "sender": {
            "id": "foo",
            "name": "bar",
            "session": "baz",
            "time": 0
        },
        "trace": {
            "samples": 100,
            "frequency": 3000000,
            "channel": 1
        },
        "sequence": 0
    }

def test_validator_fails():
    with pytest.raises(jsonschema.ValidationError):
        schema.validate_message_metadata({})
    
def test_validator_success(): 
    schema.validate_message_metadata(VALID_METADATA)

def test_get_sender_meta():
    meta = schema.get_sender_meta("foo", "bar")
    jsonschema.validate(meta, schema.SENDER_SCHEMA)
