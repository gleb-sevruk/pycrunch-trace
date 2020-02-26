import sys

from pycrunch_tracer.gleb_trace import GlebTracer
from pycrunch_tracer.src.my_code import cho_ti_suka


def trace_calls_and_returns(frame, event, arg):
    co = frame.f_code
    func_name = co.co_name
    if func_name == 'write':
        # Ignore write() calls from printing
        return
    line_no = frame.f_lineno
    filename = co.co_filename
    if not filename.endswith('sys_settrace_return.py'):
        # Ignore calls not in this module
        return
    if event == 'call':
        print('* Call to {} on line {} of {}'.format(
            func_name, line_no, filename))
        return trace_calls_and_returns
    elif event == 'return':
        print('* return:event -> function `{}` => {}'.format(func_name, arg))
    return


def b():
    print('inside b()')
    x = cho_ti_suka(4)
    return 'response_from_b '


def a():
    print('inside a()')
    val = b()
    return val * 2


ptacer = GlebTracer()
sys.settrace(ptacer.trace_calls_and_returns)
# sys.settrace(ptacer._trace)
a()

sys.settrace(None)

# import pydevd_pycharm
# pydevd_pycharm.settrace('localhost', port=44441, stdoutToServer=True, stderrToServer=True)

print('idiot')