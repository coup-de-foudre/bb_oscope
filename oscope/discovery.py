import datetime

import zmq

import netifaces as ni

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

class IPQuad:
    def __init__(self, octets: list):
        self.octets = self.assert_octets_valid(list(octets))

    def __str__(self):
        return self._fmt_octet(self.octets)

    @staticmethod
    def _fmt_octet(octets: list):
        return ".".join((str(e) for e in octets))

    @classmethod
    def from_string(cls, input: str):
        cls(int(e) for e in input.split("."))

    @staticmethod
    def assert_octets_valid(octets: list):
        assert len(octets) == 4, octets
        for ele in octets:
            assert isinstance(ele, int), type(ele)
            assert (ele >= 0) and (ele < 256), octets
        return octets

    def ips_in_24(self) -> list:
        all_ips = []
        for x in range(256):
            oct = list(self.octets)
            oct[3] = x
            all_ips.append(self._fmt_octet(oct))
        return all_ips

def is_sub_socket_live(skt: zmq.Socket, max_time: datetime.timedelta) -> bool:
    poll_time_ms = max_time.seconds / 1000.0
    return skt.poll(timeout=poll_time_ms) > 0
