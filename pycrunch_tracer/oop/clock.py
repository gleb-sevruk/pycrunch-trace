import time


class Clock:
    """
    Counts time since creating of the object
    """
    def __init__(self):
        self.started_at = self._system_clock()
        pass

    def now(self):
        return (time.perf_counter() - self.started_at) * 1000

    def _system_clock(self):
        return time.perf_counter()
