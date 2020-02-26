from datetime import datetime


def some_method(some_number):
    a = 2
    b = 3
    b = 3*4
    b = 3*4
    b = 1*4
    result = a + b + some_number
    return result


def another_m(some_new_var):
    x = 2
    for i in range(some_new_var):
        if i % 2 == 0:
            x = 3 + i
        else:
            x = 2 * i

def string_m():
    return str(datetime.now())
# x = some_method(1)
# print(x)
