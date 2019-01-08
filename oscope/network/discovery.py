import datetime

import netifaces as ni
import zmq

import oscope.network.util

# Neumonic     0scil0
SCOPE_DEFAULT = 55110


def get_interfaces() -> list:
    return ni.interfaces()

def get_ip_address(ifname: str) -> list:
    """
    Get a possibly empty list of IP4 addresses for an interface
    """
    try:
        inets = ni.ifaddresses(ifname)[ni.AF_INET]
    except KeyError:
        return []
    return [i['addr'] for i in inets]

def ips_in_24(ipaddress: str) -> list:
    quads = ipaddress.split(".")

    all_ips = []
    for x in range(256):
        quads[3] = str(x)
        all_ips.append(".".join(quads))

    return all_ips


def is_sub_socket_live(skt: zmq.Socket, max_time: datetime.timedelta) -> bool:
    poll_time_ms = max_time.seconds / 1000.0
    try:
        return skt.poll(timeout=poll_time_ms) > 0
    except zmq.error.ZMQError:
        return False


def is_ip_address_live(ip: str, timeout: datetime.timedelta, port: int=SCOPE_DEFAULT) -> bool:
    timeout_ms = timeout.total_seconds()
    with oscope.network.util.SubscribeSocket() as skt:
        skt.connect("tcp://{}:{}".format(ip, port))
        skt.subscribe("")
        return is_sub_socket_live(skt, timeout)