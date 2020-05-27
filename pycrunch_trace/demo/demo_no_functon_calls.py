

from pycrunch_trace.client.api.trace import Trace

yoba = Trace()
yoba.start(session_name='timing_datetime')

def f():
    import time
    from datetime import datetime
    from time import sleep
    diff = 0
    for _ in range(10000):
        start_time = datetime.now()
        # sleep(0.01)
        end_time = datetime.now()
        diff += (end_time - start_time).total_seconds()
    print(diff)

    diff = 0
    for _ in range(10000):
        start_time = time.perf_counter()
        # sleep(0.01)
        end_time = time.perf_counter()
        diff += (end_time - start_time)
    print(diff)

f()
yoba.stop()
# print(yoba._tracer.simulation.simulated_code())