#!/usr/bin/env python3
# -*- mode: python -*-
import serial
import sys
import time

from clocktracker import ClockTracker

PERIOD = 0.1
BAUD = 115200

class Driver:

    def __init__(self, port):
        self._port = port
        self._conn = serial.Serial(port, BAUD)
        self._tracker = ClockTracker()

    def drive(self):
        start = time.monotonic()
        self._conn.write(b"t\r\n")
        data = b""
        while True:
            data += self._conn.read(1)
            if data[-1] == 10:
                break
        if data.startswith(b"b"):
            button_press = int(data.decode("ascii").split()[1])
            print(
                self._port,
                "button",
                self._tracker.seconds_for_timestamp(button_press),
            )
        else:
            end = time.monotonic()
            estimated_communication_time = (3 + len(data)) * (1 + 8 + 1) / BAUD
            roundtrip = end - start
            ediff = roundtrip - estimated_communication_time
            self._tracker.feed(start, int(data.decode("ascii").strip()), end)

            when = (start + end) / 2
            estimated_time = self._tracker.seconds_for_timestamp(self._tracker._last_timestamp)
            print(
                self._port,
                self._tracker._factor,
                "when",
                when,
                "estimated",
                estimated_time,
            )


def main():
    drivers = [Driver(a) for a in sys.argv[1:]]

    until = time.monotonic() + PERIOD
    while True:
        for driver in drivers:
            driver.drive()
        wait_for = until - time.monotonic()
        if wait_for > 0:
            time.sleep(wait_for)
        until += PERIOD
