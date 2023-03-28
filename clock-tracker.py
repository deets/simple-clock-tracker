#!/usr/bin/env python3
# -*- mode: python -*-
import serial
import sys
import time


PERIOD = 0.1

class ClockTracker:

    def __init__(self, seconds_base=1000, b=0.001):
        self._seconds_base = seconds_base
        self._last_timestamp = None
        self._last_seconds = None
        self._factor = None
        self._b = b

    def feed(self, start, timestamp, end):
        when = (start + end) / 2
        if self._last_timestamp is not  None:
            ts_diff = timestamp - self._last_timestamp
            seconds_diff = when - self._last_seconds
            f = (ts_diff / self._seconds_base) / seconds_diff
            if self._factor is None:
                self._factor = f
            else:
                self._factor = (1 - self._b) * self._factor + self._b * f

        self._last_timestamp = timestamp
        self._last_seconds = when

    def seconds_for_timestamp(self, timestamp):
        s = timestamp / self._seconds_base
        if self._factor is not None:
            s /= self._factor
        return s


class Driver:

    def __init__(self, port):
        self._port = port
        self._conn = serial.Serial(port, 115200)
        self._tracker = ClockTracker()

    def drive(self):
        start = time.monotonic()
        self._conn.write(b"command\r\n")
        data = b""
        while True:
            data += self._conn.read(1)
            if data[-1] == 10:
                break
        end = time.monotonic()
        self._tracker.feed(start, int(data.decode("ascii").strip()), end)
        corrected_time = self._tracker.seconds_for_timestamp(self._tracker._last_timestamp)
        raw_time = (self._tracker._last_timestamp / self._tracker._seconds_base) / 2
        print(
            self._port,
            self._tracker._factor,
            corrected_time,
            raw_time,
            corrected_time - raw_time
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


if __name__ == '__main__':
    main()
