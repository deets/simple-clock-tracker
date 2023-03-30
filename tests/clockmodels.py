class LinearClock:

    def __init__(self, slope=1.0, start=0.0):
        self._slope = slope
        self._start = start
        self._first_host_timestamp = None

    def timestamp(self, host_time):
        if self._first_host_timestamp is None:
            self._first_host_timestamp = host_time
        diff = host_time - self._first_host_timestamp
        return self._start + self._slope * diff
