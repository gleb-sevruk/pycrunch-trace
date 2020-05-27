from pycrunch.insights import trace

import pycrunch_trace.tracing.simulation.models as sim
from pycrunch_trace.serialization import to_string
from pycrunch_trace.session.snapshot import snapshot
from pycrunch_trace.tracing.simple_tracer import SimpleTracer

absolute_path = '/pycrunch_tracer/samples/module_a.py'

def test_sim1():
    def code_method() -> sim.Code:
        code = sim.Code()
        code.co_filename = absolute_path
        code.co_name = 'some_method'
        code.co_argcount = 1
        code.co_argcount = 1
        return code

    method = code_method()

    def get_frame(line: int):
        frame = sim.Frame()
        frame.f_lineno = line
        frame.f_code = method
        frame.f_locals = dict(some_number=1)
        return frame
    event_buffer = []
    sut = SimpleTracer(event_buffer, 'testing',,
    sut.simple_tracer(get_frame(2), sim.EventKeys.call, None)
    sut.simple_tracer(get_frame(3), sim.EventKeys.line, None)
    sut.simple_tracer(get_frame(4), sim.EventKeys.line, None)

    sut.simple_tracer(get_frame(2), sim.EventKeys.call, None)
    sut.simple_tracer(get_frame(3), sim.EventKeys.line, None)
    sut.simple_tracer(get_frame(2), sim.EventKeys.call, None)
    sut.simple_tracer(get_frame(3), sim.EventKeys.line, None)
    sut.simple_tracer(get_frame(4), sim.EventKeys.line, None)
    sut.simple_tracer(get_frame(4), sim.EventKeys.event_return, None)
    sut.simple_tracer(get_frame(4), sim.EventKeys.line, None)
    sut.simple_tracer(get_frame(4), sim.EventKeys.event_return, None)

    sut.simple_tracer(get_frame(5), sim.EventKeys.line, None)
    sut.simple_tracer(get_frame(6), sim.EventKeys.line, None)
    sut.simple_tracer(get_frame(6), sim.EventKeys.event_return, 6)

    coe = sut.simulation.simulated_code()
    trace(coe=coe)
    trace(sixt=to_string(event_buffer[6]))
    trace(buffer=to_string(event_buffer))
    snapshot.save('a', event_buffer)
    # trace(x=x)
    pass






