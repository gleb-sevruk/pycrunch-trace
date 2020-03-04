from pycrunch_tracer.api.tracing import Yoba




def my_factorial(num: int):
    if num == 1:
        return num
    else:
        return num * my_factorial(num - 1)

yoba = Yoba()
yoba.start(session_name='factorial')

my_factorial(10)

yoba.stop()
# print(x._tracer.simulation.simulated_code())