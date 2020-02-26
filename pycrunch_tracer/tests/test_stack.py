from pycrunch_tracer.events.method_enter import ExecutionCursor
from pycrunch_tracer.tracing.simple_tracer import CallStack


def test_simple():
    sut = CallStack()
    sut.enter_frame(ExecutionCursor('test', 1))
    sut.enter_frame(ExecutionCursor('test', 2))
    print(sut.to_list())
    sut.enter_frame(ExecutionCursor('test', 3))
    print(sut.to_list())
