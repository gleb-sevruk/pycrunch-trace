from pycrunch_trace.client.api.trace import Trace


def xxx(x: int):
    y = x * 9
    xy = x * 2
    data_container = dict(x=1, y='some_data')
    for i in range(xy):
        xy += i
        data_container[str(i)] = i * 8
    return xy


yoba = Trace()
yoba.start(session_name='network_demo3')


def run(param):
    param(4)


run(xxx)


yoba.stop()

print('stoped')
