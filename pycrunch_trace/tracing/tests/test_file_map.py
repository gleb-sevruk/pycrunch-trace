from pycrunch_trace.events.method_enter import MethodEnterEvent, ExecutionCursor, StackFrame, MethodExitEvent
from pycrunch_trace.tracing.file_map import FileMap


def test_file_id():
    sut = FileMap()
    assert 1 == sut.file_id('a.py')


def test_same_file_should_return_same_id():
    sut = FileMap()
    assert 1 == sut.file_id('a.py')
    assert 1 == sut.file_id('a.py')
    assert 1 == sut.file_id('a.py')

def test_multiple_files():
    sut = FileMap()
    assert 1 == sut.file_id('a.py')
    assert 2 == sut.file_id('b.py')
    assert 3 == sut.file_id('c.py')
    assert 1 == sut.file_id('a.py')
    assert 2 == sut.file_id('b.py')
    assert 3 == sut.file_id('c.py')

def test_a():
    from pycrunch_trace.client.networking.client_trace_introspection import ClientTraceIntrospection
    sut = ClientTraceIntrospection()
    files = dict()
    files['c'] = 7
    files['a'] = 1
    files['b'] = 2
    sut.save_events([
        MethodEnterEvent(
            ExecutionCursor(7,1,'1'),
            StackFrame(-1, 1,1,'a'),
            1),
        MethodExitEvent(
            ExecutionCursor(1, 1, '1'),
            StackFrame(-1, 1, 1, 'a'),
            2),
        MethodExitEvent(
            ExecutionCursor(1, 1, '1'),
            StackFrame(-1, 1, 1, 'a'),
            2),
    ])
    sut.print_to_console(files)