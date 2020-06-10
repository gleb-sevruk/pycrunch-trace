import six

if six.PY3:
    from time import perf_counter
if six.PY2:
    from backports.time_perf_counter import perf_counter


class Clock:
    """
    Counts time since creating of the object
    """
    def __init__(self):
        self.started_at = self._system_clock()
        pass

    def now(self):
        return (perf_counter() - self.started_at) * 1000

    def _system_clock(self):
        return perf_counter()
