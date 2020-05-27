from time import sleep

from pycrunch_trace.tracing.inline_profiler import ProfilingScope, inline_profiler_instance


def call_some_funtion(i):
    with ProfilingScope('call_some_funtion'):
        sleep(0.1)
        pass


def test_nesting():
    with ProfilingScope('root'):
        for i in range(10):
            with ProfilingScope('loop'):
                call_some_funtion(i)
    inline_profiler_instance.print_timings()