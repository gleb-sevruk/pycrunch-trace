import sys


def trace_calls(frame, event, arg):
    if event != 'call':
        return
    co = frame.f_code
    func_name = co.co_name
    if func_name == 'write':
        # Ignore write() calls from printing
        return
    func_line_no = frame.f_lineno
    func_filename = co.co_filename
    if not func_filename.endswith('sys_settrace_call.py'):
        # Ignore calls not in this module
        return
    caller = frame.f_back
    caller_line_no = caller.f_lineno
    caller_filename = caller.f_code.co_filename
    print('* Call to', func_name)
    print('*  on line {} of {}'.format(
        func_line_no, func_filename))
    print('*  from line {} of {}'.format(
        caller_line_no, caller_filename))
    return


def b():
    print('inside b()\n')


def a():
    print('inside a()\n')
    b()


sys.settrace(trace_calls)
a()