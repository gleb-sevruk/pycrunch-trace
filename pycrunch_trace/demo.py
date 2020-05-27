import sys
from ppretty import ppretty

def unnamed_method(x: str):
    print('unnamed_method')

def sum(a: int, b: int) -> int:
    print('!a')
    print('!b')
    unnamed_method('a')
    return a + b

def trace_calls(frame, event, arg):
    print(f'event: {event}')
    print('f_locals '+ ppretty(frame.f_locals))
    # print(ppretty(frame))
    if event != 'call':
        return
    frame__f_code = frame.f_code
    func_name = frame__f_code.co_name
    print(f'func_name: {func_name}')
    if func_name == 'write':
        # Ignore write() calls from printing
        return
    func_line_no = frame.f_lineno
    func_filename = frame__f_code.co_filename
    if not func_filename.endswith('demo.py'):
        # Ignore calls not in this module
        return
    caller = frame.f_back
    caller_line_no = caller.f_lineno
    caller_filename = caller.f_code.co_filename
    print('* Call to', func_name)
    print(f'*  on line {func_line_no} of {func_filename}')
    print(f'*  from line {caller_line_no} of {caller_filename}')
    return

print('--- begin')

sys.settrace(trace_calls)

result = sum(1, 2)
print(result)

print('--- poshel naxoi')

