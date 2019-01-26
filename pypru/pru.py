#!/usr/bin/python3

import argparse
import os
import shutil
import subprocess
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


def require_root_or_die():
    if os.getuid() != 0:
        print("This utility must be run as root")
        sys.exit(1)


def files_ending_with(directory: str, extension: str):
    """
    Walk `directory` searching for files that end with `extension`.

    Return a possibly empty list which points to files as anchored at the
    base of directory.
    """
    results = []
    for dirpath, _, filenames in os.walk(directory):
        for filename in [f for f in filenames if f.endswith(extension)]:
            results.append(os.path.join(dirpath, filename))
    return results



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


class PRU:
    def __init__(self, pru: int):
        require_root_or_die()
        _sanity_check_device(_pru_join(pru, "device"))
        self.pru = pru

    def _state_file_path(self) -> str:
        path = _pru_join(self.pru, "state")
        assert os.path.exists(path), path
        return path

    def _report_change(self, change: str):
        print("PRU%i -> %s" % (self.pru, change))
    
    def get_state(self) -> str:
        with open(self._state_file_path()) as f:
            return f.read().strip()

    def set_state(self, state: str):
        self._report_change("Pending: %s" % state)
        with open(self._state_file_path(), "r+") as f:
            f.write(state)
        self._report_change("Completed: %s" % state)
              
    def is_pru_running(self) -> bool:
        return self.get_state() == "running"

    def start_pru(self):
        if self.is_pru_running():
            print("WARNING: PRU%i is already running" % self.pru)
            return
        self.set_state("start")
        
    def stop_pru(self):
        if not self.is_pru_running():
            print("WARNING: Requested to stop PRU%i, but already in state '%s'" % (self.pru, self.get_state()))
            return

        self.set_state("stop")
        
    def restart_pru(self):
        self.stop_pru()
        self.start_pru()

    def read_firmware_name(self) -> str:
        fw_name_file = _pru_join(self.pru, "firmware")
        with open(fw_name_file) as f:
            return f.read()

    def load_firmware(self, path: str):
        assert os.path.exists(path), path
        firmware_dest = os.path.join("/lib/firmware", self.read_firmware_name())                                                         
        print("Loading firmware for PRU%i (%s -> %s)" % (self.pru, path, firmware_dest))
        shutil.move(path, firmware_dest)
        self._report_change("Restarting")
        self.restart_pru()
        self._report_change("Restarted")



class FirmwareCompiler:
    FIRMWARE_EXTENSION = ".out"

    def __init__(self, path: str):
        assert os.path.isdir(path), path
        assert os.path.exists(os.path.join(path, "Makefile")), "Missing makefile"
        self._path = path

    def compile(self):
        try:
            subprocess.check_call("make", cwd=self._path)
        except subprocess.CalledProcessError as e:
            print("make failed:")
            print("**" * 10 + "STDOUT" + "**" * 10)
            print(e.stdout)

            print("**" * 10 + "STDERR" + "**" * 10)
            print(e.stderr)
            raise

    def find_output(self):
        return files_ending_with(self._path, self.FIRMWARE_EXTENSION)


if __name__ == "__main__":
    PRUS = (0, 1)
    parser = argparse.ArgumentParser(description=USAGE)
    parser.add_argument(
        "--prus", nargs="+", choices=PRUS,
        help="Which PRU(s) to target")
    parser.add_argument(
        "--start", type=int, choices=PRUS,
        help="Start the pru specified (REQUIRES ROOT)")
    parser.add_argument(
        "--stop", type=int, choices=PRUS,
        help="Stop the pru specified  (REQUIRES ROOT)")
    parser.add_argument(
        "--compile", nargs=1, type=str, metavar="TARGET",
        help="Make, load and start from source.")
    parser.add_argument(
        "--load", nargs=1, type=str, metavar="TARGET",
        help="Make, load and start from source (REQUIRES ROOT)")
    args = parser.parse_args()

    if not (args.start or args.stop or args.compile or args.load):
        parser.print_help()
        sys.exit(1)

    if args.start:
        PRU(args.start).start_pru()

    elif args.stop:
        PRU(args.start).stop_pru()

    elif args.compile:
        fw = FirmwareCompiler(args.compile[0])
        fw.compile()
        print(fw.find_output())

    elif args.load:
        fw = FirmwareCompiler(args.load[0])

        for n, fw in enumerate(fw.find_output()):
            PRU(n).load_firmware(fw)
    else:
        parser.print_usage()
        sys.exit(1)
