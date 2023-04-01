import pytest
from clockmodels import LinearClock, PiecewiseClock


def test_linearclock_first_timestamp_yields_start():
    start = 10.0
    linear_clock = LinearClock(slope=2.0, start=start)
    assert linear_clock.timestamp(1000.0) == linear_clock.timestamp(1000.0)
    assert linear_clock.timestamp(1000.0) == start


def test_linearclock_slope():
    linear_clock = LinearClock(slope=2.0, start=10.0)
    first = linear_clock.timestamp(1000.0)
    second = linear_clock.timestamp(2000.0)
    assert second - first == 2000.0


def test_linearclock_inverse():
    linear_clock = LinearClock(slope=2.0, start=10.0)
    for t in range(0, 10000, 10):
        timestamp = linear_clock.timestamp(t)
        assert t == pytest.approx(linear_clock.inverse(timestamp))


def test_piecewise_first_timestamp_yields_start():
    start = 23.0
    piecewise_clock = PiecewiseClock(
        # length, slope
        [
          (3.0, 2.0),
          (2.0, 1.5)
        ],
        start=start,
    )
    assert piecewise_clock.timestamp(1000.0) == piecewise_clock.timestamp(1000.0)
    assert piecewise_clock.timestamp(1000.0) == start


def test_piecewise_slope_reproduced_within_first_segment():
    start = 23.0
    piecewise_clock = PiecewiseClock(
        # length, slope
        [
          (3.0, 2.0),
          (2.0, 1.5)
        ],
        start=start,
    )
    first = piecewise_clock.timestamp(0.0)
    # less than the first segments length
    second = piecewise_clock.timestamp(2.5)
    assert (second - first) / 2.5 == 2.0


def test_piecewise_slope_reproduced_within_second_segment():
    start = 0.0
    piecewise_clock = PiecewiseClock(
        # length, slope
        [
          (3.0, 2.0),
          (2.0, 1.5)
        ],
        start=start,
    )
    # seed the start timestamp
    piecewise_clock.timestamp(0.0)
    first = piecewise_clock.timestamp(3.1)
    second = piecewise_clock.timestamp(3.1 + 1)
    assert (second - first) / 1 == pytest.approx(1.5)


def test_piecewise_slope_inverse():
    start = 0.0
    piecewise_clock = PiecewiseClock(
        # length, slope
        [
          (3.0, 2.0),
          (2.0, 1.5)
        ],
        start=start,
    )
    for t in range(0, 10000, 10):
        timestamp = piecewise_clock.timestamp(t)
        assert t == pytest.approx(piecewise_clock.inverse(timestamp))
