from time import sleep

from pycrunch_trace.client.api import trace


def alternative_ways_to_trace():
    sleep(0.25)
    print('You can use Trace object to manually start and stop tracing')
    print(' Or by applying @trace decorator to the method')
    print(' See examples bellow')

def example_without_decorators():
    from pycrunch_trace.client.api import Trace

    tracer = Trace()
    tracer.start('recording_name')

    code_under_trace()
    another_code_to_trace()

    tracer.stop()


@trace
def example_with_decorator():
    # Recording will be named the same as the method name
    pass


@trace('this_is_custom_name')
def example_with_custom_name():
    pass