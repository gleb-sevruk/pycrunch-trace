import struct

from pycrunch_trace.events.method_enter import ExecutionCursor
from pycrunch_trace.tracing.simple_tracer import CallStack


def test_simple():
    x = struct.calcsize("i")
    print('size='+str(x))
    sut = CallStack()
    sut.enter_frame(ExecutionCursor('test', 1))
    sut.enter_frame(ExecutionCursor('test', 2))
    print(sut.top_level_frame_as_clone())
    sut.enter_frame(ExecutionCursor('test', 3))
    print(sut.top_level_frame_as_clone())
