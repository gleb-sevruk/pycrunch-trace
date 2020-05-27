from pycrunch_trace.client.api import trace


def nested_two(x):
    return x * 2

# down arrow (step over) should not enter this function
def nested_one(x):
    return x + 1


@trace
def demo_stepping_nested_calls():
    x = 1
    y = nested_one(nested_two(x))
    print(y)


demo_stepping_nested_calls()
