from pycrunch_trace.client.api.trace import Trace

def d___():
    a = 1
    b = 2
    c = 3

def c___():
    a = 1
    b = 2
    d___()
    c = 3


def b___():
    a = 1
    c___()
    b = 2
    c = 3



def a___():
    a = 1
    b = 2
    b___()
    c = 3




tracer = Trace()
tracer.start('recording_name')

a___()

tracer.stop()
# print(y._tracer.simulation.simulated_code())
# import pydevd_pycharm
# pydevd_pycharm.settrace('localhost', port=44441, stdoutToServer=True, stderrToServer=True)
# for (x, cmd) in enumerate(y.command_buffer):
#     print(str(x+1) + ' - line:' + str(cmd.cursor.line) + ':' + str(cmd))