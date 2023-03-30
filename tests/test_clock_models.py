from clockmodels import LinearClock


def test_first_timestamp_yields_start():
    linear_clock = LinearClock(slope=2.0, start=10.0)
    assert(linear_clock.timestamp(1000.0) == linear_clock.timestamp(1000.0))


def test_slope():
    linear_clock = LinearClock(slope=2.0, start=10.0)
    first = linear_clock.timestamp(1000.0)
    second = linear_clock.timestamp(2000.0)
    assert(second - first == 2000.0)
