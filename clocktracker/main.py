#!/usr/bin/env python3
# -*- mode: python -*-
import serial
import sys
import time


PERIOD = 0.1

class ClockTracker:
    """We want to estimate two quantities to lock
    the attached node's internal clock to our
    system clock.

     - offset: the MCU clock usually starts at system start at 0, while
       the host clock is possibly based on unix timestamps, or also from
       system start, but these two points don't coincide of course.
     - factor: the MCU clock runs fast or slow with respect to the host
       clock (our source of truth). This is expressed in a linear factor
       that will usually oscillate slightly around 1 (given that we normalize
       to seconds for all computations.

    Both quantities can only be measured with some (hopefully white)
    phase noise. This is due do a range of factors:

     - Noise in both clocks themselves (comparatively neglible).
     - Scheduling jitter especially on the host side.
     - Communication jitter (probably relatively low).

    Thus we estimate these by obtaining measurements and low-pass
    filtering the residual to affect our current guess.

    """

    def __init__(self, seconds_base=1000, gain=0.001):
        self._seconds_base = seconds_base
        self._last_timestamp = None
        self._last_host = None
        self._factor = None
        self._offset = None
        self._gain = gain

    def feed(self, start, timestamp, end):
        # We assume that the noise is symetrical
        # in our communication line, thus the moment
        # of obtaining the timestamp on the MCU is
        # supposed to be right in the middle of our
        # overall interval.
        when = (start + end) / 2
        if self._last_timestamp is not  None:
            ts_diff = (timestamp - self._last_timestamp) / self._seconds_base
            host_diff = when - self._last_host
            factor = ts_diff / host_diff
            if self._factor is None:
                self._factor = factor
            else:
                # Low pass filter applying gain to the residual of the
                # error.
                self._factor = (1 - self._gain) * self._factor + self._gain * factor
                projected_offset_diff = host_diff - host_diff * self._factor * self._seconds_base
                projected_offset = when - self._offset + projected_offset_diff
                current_offset = when - timestamp / self._seconds_base
                print("projected_offset", projected_offset, "current_offset", current_offset, "diff", projected_offset - current_offset)

            self._offset = when - timestamp / self._seconds_base

        self._last_timestamp = timestamp
        self._last_host = when

    def seconds_for_timestamp(self, timestamp):
        if self._factor is not None:
            diff = (timestamp - self._last_timestamp) / self._seconds_base
            return diff * self._factor + timestamp / self._seconds_base + self._offset
        return -1


class Driver:

    def __init__(self, port):
        self._port = port
        self._conn = serial.Serial(port, 115200)
        self._tracker = ClockTracker()

    def drive(self):
        start = time.monotonic()
        self._conn.write(b"t\r\n")
        data = b""
        while True:
            data += self._conn.read(1)
            if data[-1] == 10:
                break
        end = time.monotonic()
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
