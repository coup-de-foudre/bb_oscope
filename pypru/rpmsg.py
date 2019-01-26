#!/usr/bin/python3
import argparse
import datetime
import os

THREE_SECONDS = datetime.timedelta(seconds=3)


def find_rpmsg_endpoint(timeout: datetime.timedelta = THREE_SECONDS):
    end_time = datetime.datetime.now() + timeout

    while True:
        results = [os.path.join("/dev", n) for n in os.listdir("/dev") if "pru" in n]
        if len(results) != 0:
            return results

        if datetime.datetime.now() > end_time:
            raise TimeoutError("No remoteproc endpoint found in %i seconds" % timeout.total_seconds())    


def send_rpmsg(msg: bytes):
    ep = find_rpmsg_endpoint()[0]
    print("Sending '{}' --> '{}'".format(msg.hex(), ep))
    with open(ep, "wb") as f:
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
