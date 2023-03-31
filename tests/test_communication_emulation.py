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
        timestamp = self._mcu_clock.compute(begin + (end - begin) * relative_position)
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
