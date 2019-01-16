#/usr/bin/python3
import argparse
import os
import sys

REMOTEPROC_ROOT = "/sys/class/remoteproc/"

USAGE = """
This is a tool designed to start/stop and flash the PRU's
as configured on the current beablebone image

   pru [NUMBER] [--start] [--stop] [--state]

NUMBER must be either 0, or 1, which confusingly map to
the devices:
  - 0 /sys/class/remoteproc/remoteproc1
  - 1 /sys/class/remoteproc/remoteproc2

"""

def _pru_join(number: int, location: str):
    return os.path.join(REMOTEPROC_ROOT, "remoteproc%i" % (number + 1), location)


def _sanity_check_device(device_link: str):
    assert os.path.exists(pru0_device) and os.path.islink(pru0_device), pru0_device
    realpath = os.path.realpath(device_link)
    assert "pru" in realpath, realpath


pru0_device = _pru_join(0, "device")
_sanity_check_device(pru0_device)

pru1_device = _pru_join(1, "device")
_sanity_check_device(pru1_device)


def get_state(pru: int):
    with open(_pru_join(pru, "state")) as f:
        return f.read()


def set_state(pru: int, state: str):
    with open(_pru_join(pru, "state"), "r+") as f:
        f.write(state)


def is_pru_running(pru: int) -> bool:
    return get_state(pru) == "running"


def start_pru(pru: int):
    if is_pru_running(pru):
        print("WARNING: PRU%i is already running" % pru)
        return
    set_state(pru, "start")


def stop_pru(pru: int):
    if not is_pru_running(pru):
        print("WARNING: Can not stop PRU%i: %s" % (pru, get_state(pru)))
    set_state(pru, "stop")


def restart_pru(pru: int):
    stop_pru(pru)
    start_pru(pru)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=USAGE)
    parser.add_argument("pru", type=int, choices=[0, 1])
    parser.add_argument("--start", help="Start the pru specified", action="store_true")
    parser.add_argument("--stop", help="Stop the pru specified", action="store_true")
    args = parser.parse_args()

    if not args.start or args.stop:
        print(USAGE)
        sys.exit(1)

    if os.getuid() != 0:
        print("This utility must be run as root")
        sys.exit(1)

    if args.start:
        start_pru(args.pru)
    elif args.stop:
        stop_pru(args.pru)
