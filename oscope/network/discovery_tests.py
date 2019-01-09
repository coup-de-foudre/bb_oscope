import datetime

import pytest
import zmq

import oscope.base
import oscope.network.discovery as discovery
import oscope.network.util

def _assert_is_list_of_strings(thing):
    oscope.base.assert_isinstance(thing, list)
    for element in thing:
        oscope.base.assert_isinstance(element, str)

def test_get_interfaces():
    interfaces = discovery.get_interfaces()
    _assert_is_list_of_strings(interfaces)
    assert len(interfaces) > 0, interfaces

def test_get_ip():
    interfaces = discovery.get_interfaces()

    for iface in interfaces:
        ips = discovery.get_ip_address(iface)
        _assert_is_list_of_strings(ips)

def test_ip_enumerants():
    slash24 = discovery.ips_in_24("1.2.3.1")
    for x in range(256):
        oscope.base.assert_contained("1.2.3.%s" % x, slash24)

def test_is_sub_scket_live():
    with oscope.network.util.LinkedPubSubPair() as (pub, sub):
        pub.send(b"anything")
        live = discovery.is_sub_socket_live(sub, max_time=datetime.timedelta(seconds=1))
    
    oscope.base.assert_true(live)

    with oscope.network.util.SubSocket() as skt:
        live = discovery.is_sub_socket_live(skt, max_time=datetime.timedelta(seconds=1))
    oscope.base.assert_false(live)

    with oscope.network.util.SubSocket() as skt:
        live = discovery.is_sub_socket_live(skt, max_time=datetime.timedelta(seconds=1))
    oscope.base.assert_false(live)

def test_is_ip_address_live():
    live = discovery.is_ip_address_live("127.0.0.1", datetime.timedelta(seconds=0.1), port=55555)
    oscope.base.assert_isinstance(live, bool)
    oscope.base.assert_false(live)

    with oscope.network.util.LinkedPubSubPair() as (pub, _):
        port = pub.bind_to_random_port('tcp://127.0.0.1')
        discovery.is_ip_address_live("127.0.0.1", datetime.timedelta(seconds=1), port=port)

def test_scan_subnet_smoke():
    discovery.scan_subnet("127.23.23.23", quiet=False)

def test_scan_subnet():
    results = discovery.scan_subnet("127.23.23.23")
    oscope.base.assert_isinstance(results, list)
    assert results == [], results