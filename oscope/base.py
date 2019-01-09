def assert_isinstance(thing, expected_type):
    assert isinstance(thing, expected_type), "Expected {} got {}".format(expected_type, type(thing))

def assert_length(thing, length):
    assert len(thing) == length, "Expected '{}' to have length of {}, has {}".format(thing, length, len(thing))
