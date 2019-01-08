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

def test_ip_enumerants():
    slash24 = oscope.discovery.ips_in_24("1.2.3.1")

    for x in range(256):
        assert ("1.2.3.%s" % x) in slash24
