from pycrunch_tracer.api.tracing import Yoba


def xxx(x: int):
    y = x * 9
    xy = x * 2
    zalupa = dict(x=1, y='some_data')
    for i in range(xy):
        xy += i
        zalupa[str(i)] = i * 8
    return xy


yoba = Yoba()
yoba.start(session_name='network_demo2')


def run(param):
    param(4)


run(xxx)


yoba.stop()
