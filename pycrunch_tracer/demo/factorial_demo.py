from pycrunch_tracer.api.tracing import Yoba

x = Yoba()
x.start('factorial')


def my_factorial(num: int):
    if num == 1:
        return num
    else:
        return num * my_factorial(num - 1)


my_factorial(10)

x.stop()
print(x._tracer.simulation.simulated_code())