# TODO(meawoppl) - Add tests for all of these.


def assert_isinstance(thing, expected_type):
    __tracebackhide__ = True
    msg = "Expected {} got {}".format(expected_type, type(thing))
    assert isinstance(thing, expected_type), msg


def assert_length(thing, length):
    __tracebackhide__ = True
    msg = "Expected '{}' to have length of {}, has {}".format(
        thing, length, len(thing))
    assert len(thing) == length, msg


def assert_contained(thing, container):
    __tracebackhide__ = True
    assert thing in container, "Expected {} to contain {}".format(
        thing, container)


def assert_true(thing, message="Expected to be true"):
    __tracebackhide__ = True
    assert_isinstance(thing, bool)
    assert thing, message


def assert_false(thing, message="Expected value to be false"):
    __tracebackhide__ = True
    assert_isinstance(thing, bool)
    assert not thing, message
