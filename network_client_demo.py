from tracing_core.api.tracing import Yoba


def xxx(x: int):
    y = x * 4
    return y


yoba = Yoba()
yoba.start()

xxx(4)

yoba.stop()
