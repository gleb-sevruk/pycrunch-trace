from time import sleep

from pycrunch_tracer.client.api import yoba


@yoba('timings_precision')
def run(x):
    y = x
    sleep(0.3)
    b()
    sleep(1)


def x():
    sleep(0.1)


def b():
    y = 'sleeped 01'
    sleep(0.2)
    for i in range(10):
        x()
    c()


def c():
    y = 'sleeped 01'
    sleep(0.7)
    y = 'sleeped 1 sec total'


run(1)

