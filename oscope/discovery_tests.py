import pytest

import oscope.discovery

def _assert_is_list_of_strings(thing):
    assert isinstance(thing, list), type(thing)
    for element in thing:
        assert isinstance(element, str), type(element)


def test_get_interfaces():
    interfaces = oscope.discovery.get_interfaces()
    _assert_is_list_of_strings(interfaces)
    assert len(interfaces) > 0, interfaces

def test_get_ip():
    interfaces = oscope.discovery.get_interfaces()

    for iface in interfaces:
        ips = oscope.discovery.get_ip_address(iface)
        _assert_is_list_of_strings(ips)

def test_IPQuad_valid():
    ipq = oscope.discovery.IPQuad((1, 2, 3, 4))

    assert str(ipq) == "1.2.3.4", str(ipq)
    assert ipq.octets == [1, 2, 3, 4]

    oscope.discovery.IPQuad.from_string("127.0.0.1")

def test_IPQuad_asserts():
    with pytest.raises(AssertionError):
        oscope.discovery.IPQuad.assert_octets_valid((1, 2, 3, 256))

    with pytest.raises(AssertionError):
        oscope.discovery.IPQuad.assert_octets_valid((0, 2, 3, 256))

    with pytest.raises(AssertionError):
        oscope.discovery.IPQuad.assert_octets_valid((1, 2, 3))

def test_ip_enumerants():
    quad = oscope.discovery.IPQuad((1, 2, 3, 4))
    slash24 = quad.ips_in_24()

    for x in range(256):
        assert ("1.2.3.%s" % x) in slash24
