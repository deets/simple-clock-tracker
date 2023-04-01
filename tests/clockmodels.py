from itertools import cycle
from scipy.optimize import minimize_scalar

class BaseClock:

    def __init__(self, start):
        self._start = start
        self._first_host_timestamp = None

    def timestamp(self, host_time):
        if self._first_host_timestamp is None:
            self._first_host_timestamp = host_time
        diff = host_time - self._first_host_timestamp
        return self._start + self.compute(diff)

    def inverse(self, timestamp):
        res = minimize_scalar(
            lambda x: abs(self.timestamp(x) - timestamp)
        )
        return res.x



class LinearClock(BaseClock):

    def __init__(self, slope=1.0, start=0.0):
        super().__init__(start)
        self._slope = slope

    def compute(self, diff):
        return self._slope * diff


    def inverse(self, timestamp):
        tdiff = timestamp - self._start
        return self._first_host_timestamp + tdiff / self._slope


class PiecewiseClock(BaseClock):

    def __init__(self, pieces, start=0.0):
        super().__init__(start)
        self._pieces = pieces

    def compute(self, diff):
        value = 0.0
        for length, slope in cycle(self._pieces):
            if diff >= length:
                diff -= length
                value += length * slope
            else:
                return value + diff * slope
