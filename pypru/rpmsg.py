#!/usr/bin/python3
import argparse
import os


def find_rpmsg_endpoint():
    return [os.path.join("/dev", n) for n in os.listdir("/dev") if "pru" in n]


def send_rpmsg(msg: bytes):
    ep = find_rpmsg_endpoint()[0]
    print("Sending '{}' --> '{}'".format(msg.hex(), ep))
    with open(ep, "w+b") as f:
        f.write(msg)


def recv_rpmsg() -> bytes:
    ep = find_rpmsg_endpoint()[0]

    with open(ep, "rb") as f:
        msg = f.read()
    print("Received: '{}' --> '{}'".format(msg.hex(), ep))
    return msg


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("messages", nargs="+")
    args = parser.parse_args()

    for msg in args.messages:
        send_rpmsg(msg.encode("ascii"))
        recv_rpmsg()
