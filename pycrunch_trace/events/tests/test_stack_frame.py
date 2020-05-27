from pycrunch.insights import trace

from pycrunch_trace.events.method_enter import ExecutionCursor
from pycrunch_trace.tracing.simple_tracer import CallStack


def test_1():
    sut = CallStack()
    sut.enter_frame(ExecutionCursor('a', 1))
    sut.enter_frame(ExecutionCursor('b', 2))
    sut.enter_frame(ExecutionCursor('c', 3))
    sut.new_cursor_in_current_frame(ExecutionCursor('b', 3))
    sut.exit_frame()

    x = sut.current_frame()
    ex = sut.top_level_frame_as_clone()
    # trace(yyy=str(x))
    trace(ex=str(ex))
