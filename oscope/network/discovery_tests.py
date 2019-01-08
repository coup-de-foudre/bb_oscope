import datetime

import pytest
import zmq

import oscope.discovery
import oscope.network.util

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

def test_is_sub_scket_live():
    with oscope.network.util.LinkedPubSubPair() as (pub, sub):
        pub.send(b"anything")
        live = oscope.discovery.is_sub_socket_live(sub, max_time=datetime.timedelta(seconds=1))
    
    assert live, "Not live :("

    with oscope.network.util.SubscribeSocket() as skt:
        live = oscope.discovery.is_sub_socket_live(skt, max_time=datetime.timedelta(seconds=1))
    assert not live, "Live?!?!"

    with oscope.network.util.SubscribeSocket() as skt:
        live = oscope.discovery.is_sub_socket_live(skt, max_time=datetime.timedelta(seconds=1))
    assert not live, "Live?!?!"

def test_is_ip_address_live():
    live = oscope.discovery.is_ip_address_live("127.0.0.1", datetime.timedelta(seconds=0.1), port=55555)
    assert isinstance(live, bool)
    assert not live, "?!?!?"

    with oscope.network.util.LinkedPubSubPair() as (pub, _):
        port = pub.bind_to_random_port('tcp://*')
        oscope.discovery.is_ip_address_live("127.0.0.1", datetime.timedelta(seconds=2), port=port)