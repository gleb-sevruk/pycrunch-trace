from pycrunch_trace.client.api.trace import Trace




def my_factorial(num: int):
    if num == 1:
        return num
    else:
        return num * my_factorial(num - 1)

yoba = Trace()
yoba.start(session_name='factorial')

my_factorial(10)

yoba.stop()
# print(x._tracer.simulation.simulated_code())