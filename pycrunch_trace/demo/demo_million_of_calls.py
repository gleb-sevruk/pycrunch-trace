from pycrunch_trace.client.api import trace, Trace
from pycrunch_trace.oop import Clock


def nested_function(input_a2):
    input_a2 += 2
    return input_a2

def another_function(input_argument):
    x = nested_function(input_argument)
    y = nested_function(input_argument + 1)
    return x + y

def million_of_calls():
    # 20000 = 300008
    max_events = 10
    max_events = 100000
    for x in range(max_events):
        another_function(x)

clock = Clock()
my_yoba = Trace()
my_yoba.start('million_of_calls')
start = clock.now()

print('before', start)
million_of_calls()
end = clock.now()
print('after', end)
print('diff', end - start)

my_yoba.stop()
# print(my_yoba._tracer.simulation.simulated_code())
