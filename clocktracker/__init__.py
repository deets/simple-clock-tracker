# Copyright: 2023, Diez B. Roggisch, Berlin . All rights reserved.


class ClockTracker:
    """
    We want to estimate the factor the MCU clock runs fast or slow
    with respect to the host clock (our source of truth). This is
    expressed in a linear factor that will usually oscillate
    slightly around 1 (given that we normalize to seconds for all
     computations.

    It can only be measured with some (hopefully white)
    phase noise. This is due do a range of factors:

     - Noise in both clocks themselves (comparatively neglible).
     - Scheduling jitter especially on the host side, but also MCU side.
     - Communication jitter (probably relatively low).

    Thus we estimate these by obtaining measurements and low-pass
    filtering the residual to affect our current guess.
    """

    def __init__(self, seconds_base=1000, gain=0.001):
        self._seconds_base = seconds_base
        self._last_timestamp = None
        self._last_host = None
        self._factor = None
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

        self._last_timestamp = timestamp
        self._last_host = when

    def seconds_for_timestamp(self, timestamp):
        if self._factor is not None:
            diff = (timestamp - self._last_timestamp) / self._seconds_base
            return diff / self._factor + self._last_host
        return -1
