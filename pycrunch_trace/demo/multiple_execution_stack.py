from pycrunch_trace.client.api.trace import Trace


def c(number):
    print('in c')
    response = number * 2
    return response


def b(y):
    print('opa')
    return y * 2


def a(x):
    y = x + 1
    res = b(y)
    y = res + 1
    res = c(res + 1)
    return res

yoba = Trace()
yoba.start('multiple_stack')

a(2)

yoba.stop()