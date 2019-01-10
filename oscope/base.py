import datetime

import zmq


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


def assert_pollin(skt: zmq.Socket, timeout=datetime.timedelta(seconds=1)):
    assert_isinstance(skt, zmq.Socket)
    message = "Socket {} did not POLLIN in {} seconds".format(skt, timeout.total_seconds())
    assert skt.poll(timeout=timeout.total_seconds() * 1000) > 0, message


def assert_is_none(thing):
    assert thing is None, "Expected None, got: {}".format(type(thing))
