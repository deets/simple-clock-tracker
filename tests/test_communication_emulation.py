import pytest
from scipy.stats import exponnorm

from clocktracker import ClockTracker

from clockmodels import LinearClock


class Emulator:
    """
    Produces triples of

    host_begin, mcu_timestamp, host_end

    that emulate a full roundtrip of querying the MCU
    for a timestamp.
    """

    def __init__(self, communication_distribution, mcu_clock, start=0.0):
        self._communication_distribution = communication_distribution
        self._mcu_clock = mcu_clock
        self._start = start

    def next(self, step, relative_position=0.5):
        """
        Calling this with step produces

        host_begin: last host_begin + step
        host_end: host_begin + communication_distribution value
        mcu_timestamp: queried with a timestamp betwen host_begin and host_end weighted
                       by relative_position
        """
        self._start = begin = self._start + step
        end = begin + self._communication_distribution()
        mcu_sampling_time = begin + (end - begin) * relative_position
        timestamp = self._mcu_clock.compute(mcu_sampling_time)
        return begin, timestamp, end


def test_clock_emulation():
    clock = LinearClock(slope=1.0)
    rsv = lambda: 1
    emulator = Emulator(rsv, clock)
    # Very simple: no variance because rsv is constant,
    begin, timestamp, end = emulator.next(0)
    assert begin == 0.0
    assert timestamp == 0.5
    assert end == 1.0

    begin, timestamp, end = emulator.next(100)
    assert begin == 100.0
    assert timestamp == 100.5
    assert end == 101.0


def test_rp2040_model_with_simple_linear_clock():
    # This is the timestamp command (t\r\n)
    # vs an average timestamp in millis
    # 1000000\r\n
    relative_position = 3 / 9
    mcu_clock_start = 100
    # This is what I programmed into the pico to do:
    # return millis() * 2
    clock = LinearClock(slope=2.0, start=mcu_clock_start)
    # This was determined by experiment on an actual
    # rp2040 attached to my M1 AirBook
    K, mu, sigma = (0.6205714778937732, 0.0006558221748244949, 6.786911545123386e-05)
    rsv = lambda: exponnorm.rvs(K, loc=mu, scale=sigma)
    emulator = Emulator(rsv, clock)
    tracker = ClockTracker(seconds_base=1.0)
    step = 0.1  # Every 100ms one communication
    while True:
        start, timestamp, end = emulator.next(step, relative_position)
        tracker.feed(start, timestamp, end)
        # When we are within 1 promille of the
        # actual factor, we're good enough.
        if tracker._factor == pytest.approx(2.0, 0.001):
            break

    assert tracker.seconds_for_timestamp(2000) == pytest.approx(1000.0, 0.01)
    assert tracker.seconds_for_timestamp(4000) == pytest.approx(2000.0, 0.01)
