import jsonpickle
from pycrunch.insights import trace

from pycrunch_trace.events import event_buffer_in_protobuf
from pycrunch_trace.filters import DefaultFileFilter
from pycrunch_trace.proto import message_pb2
from pycrunch_trace.serialization import to_string
from pycrunch_trace.tracing.simulation import models
from pycrunch_trace.tracing.simple_tracer import SimpleTracer
from pycrunch_trace.tracing.simulator_sink import SimulationEvent


def create_event_1():
    code_clone = models.Code()
    code_clone.co_name = 'my_factorial'
    code_clone.co_filename = '/Users/gleb/code/pycrunch_tracing/pycrunch_tracer/demo/factorial_demo.py'
    code_clone.co_argcount = 1

    sim_frame = models.Frame()
    sim_frame.f_lineno = 7
    sim_frame.f_locals = {
        'num': 10}
    sim_frame.f_code = code_clone
    evt = SimulationEvent(sim_frame, 'call', None)

    return evt


def create_event_2():
    code_clone = models.Code()
    code_clone.co_name = 'my_factorial'
    code_clone.co_filename = '/Users/gleb/code/pycrunch_tracing/pycrunch_tracer/demo/factorial_demo.py'
    code_clone.co_argcount = 1

    sim_frame = models.Frame()
    sim_frame.f_lineno = 8
    sim_frame.f_locals = {
        'num': 10}
    sim_frame.f_code = code_clone
    evt = SimulationEvent(sim_frame, 'line', None)

    return evt


def create_event_3():
    code_clone = models.Code()
    code_clone.co_name = 'my_factorial'
    code_clone.co_filename = '/Users/gleb/code/pycrunch_tracing/pycrunch_tracer/demo/factorial_demo.py'
    code_clone.co_argcount = 1

    sim_frame = models.Frame()
    sim_frame.f_lineno = 11
    sim_frame.f_locals = {
        'num': 10}
    sim_frame.f_code = code_clone
    evt = SimulationEvent(sim_frame, 'line', None)

    return evt


def create_event_4():
    code_clone = models.Code()
    code_clone.co_name = 'my_factorial'
    code_clone.co_filename = '/Users/gleb/code/pycrunch_tracing/pycrunch_tracer/demo/factorial_demo.py'
    code_clone.co_argcount = 1

    sim_frame = models.Frame()
    sim_frame.f_lineno = 7
    sim_frame.f_locals = {
        'num': 9}
    sim_frame.f_code = code_clone
    evt = SimulationEvent(sim_frame, 'call', None)

    return evt


def create_event_5():
    code_clone = models.Code()
    code_clone.co_name = 'my_factorial'
    code_clone.co_filename = '/Users/gleb/code/pycrunch_tracing/pycrunch_tracer/demo/factorial_demo.py'
    code_clone.co_argcount = 1

    sim_frame = models.Frame()
    sim_frame.f_lineno = 8
    sim_frame.f_locals = {
        'num': 9}
    sim_frame.f_code = code_clone
    evt = SimulationEvent(sim_frame, 'line', None)

    return evt


def create_event_6():
    code_clone = models.Code()
    code_clone.co_name = 'my_factorial'
    code_clone.co_filename = '/Users/gleb/code/pycrunch_tracing/pycrunch_tracer/demo/factorial_demo.py'
    code_clone.co_argcount = 1

    sim_frame = models.Frame()
    sim_frame.f_lineno = 11
    sim_frame.f_locals = {
        'num': 9}
    sim_frame.f_code = code_clone
    evt = SimulationEvent(sim_frame, 'line', None)

    return evt


def create_event_7():
    code_clone = models.Code()
    code_clone.co_name = 'my_factorial'
    code_clone.co_filename = '/Users/gleb/code/pycrunch_tracing/pycrunch_tracer/demo/factorial_demo.py'
    code_clone.co_argcount = 1

    sim_frame = models.Frame()
    sim_frame.f_lineno = 7
    sim_frame.f_locals = {
        'num': 8}
    sim_frame.f_code = code_clone
    evt = SimulationEvent(sim_frame, 'call', None)

    return evt


def create_event_8():
    code_clone = models.Code()
    code_clone.co_name = 'my_factorial'
    code_clone.co_filename = '/Users/gleb/code/pycrunch_tracing/pycrunch_tracer/demo/factorial_demo.py'
    code_clone.co_argcount = 1

    sim_frame = models.Frame()
    sim_frame.f_lineno = 8
    sim_frame.f_locals = {
        'num': 8}
    sim_frame.f_code = code_clone
    evt = SimulationEvent(sim_frame, 'line', None)

    return evt


def create_event_9():
    code_clone = models.Code()
    code_clone.co_name = 'my_factorial'
    code_clone.co_filename = '/Users/gleb/code/pycrunch_tracing/pycrunch_tracer/demo/factorial_demo.py'
    code_clone.co_argcount = 1

    sim_frame = models.Frame()
    sim_frame.f_lineno = 11
    sim_frame.f_locals = {
        'num': 8}
    sim_frame.f_code = code_clone
    evt = SimulationEvent(sim_frame, 'line', None)

    return evt


def create_event_10():
    code_clone = models.Code()
    code_clone.co_name = 'my_factorial'
    code_clone.co_filename = '/Users/gleb/code/pycrunch_tracing/pycrunch_tracer/demo/factorial_demo.py'
    code_clone.co_argcount = 1

    sim_frame = models.Frame()
    sim_frame.f_lineno = 7
    sim_frame.f_locals = {
        'num': 7}
    sim_frame.f_code = code_clone
    evt = SimulationEvent(sim_frame, 'call', None)

    return evt


def create_event_11():
    code_clone = models.Code()
    code_clone.co_name = 'my_factorial'
    code_clone.co_filename = '/Users/gleb/code/pycrunch_tracing/pycrunch_tracer/demo/factorial_demo.py'
    code_clone.co_argcount = 1

    sim_frame = models.Frame()
    sim_frame.f_lineno = 8
    sim_frame.f_locals = {
        'num': 7}
    sim_frame.f_code = code_clone
    evt = SimulationEvent(sim_frame, 'line', None)

    return evt


def create_event_12():
    code_clone = models.Code()
    code_clone.co_name = 'my_factorial'
    code_clone.co_filename = '/Users/gleb/code/pycrunch_tracing/pycrunch_tracer/demo/factorial_demo.py'
    code_clone.co_argcount = 1

    sim_frame = models.Frame()
    sim_frame.f_lineno = 11
    sim_frame.f_locals = {
        'num': 7}
    sim_frame.f_code = code_clone
    evt = SimulationEvent(sim_frame, 'line', None)

    return evt


def create_event_13():
    code_clone = models.Code()
    code_clone.co_name = 'my_factorial'
    code_clone.co_filename = '/Users/gleb/code/pycrunch_tracing/pycrunch_tracer/demo/factorial_demo.py'
    code_clone.co_argcount = 1

    sim_frame = models.Frame()
    sim_frame.f_lineno = 7
    sim_frame.f_locals = {
        'num': 6}
    sim_frame.f_code = code_clone
    evt = SimulationEvent(sim_frame, 'call', None)

    return evt


def create_event_14():
    code_clone = models.Code()
    code_clone.co_name = 'my_factorial'
    code_clone.co_filename = '/Users/gleb/code/pycrunch_tracing/pycrunch_tracer/demo/factorial_demo.py'
    code_clone.co_argcount = 1

    sim_frame = models.Frame()
    sim_frame.f_lineno = 8
    sim_frame.f_locals = {
        'num': 6}
    sim_frame.f_code = code_clone
    evt = SimulationEvent(sim_frame, 'line', None)

    return evt


def create_event_15():
    code_clone = models.Code()
    code_clone.co_name = 'my_factorial'
    code_clone.co_filename = '/Users/gleb/code/pycrunch_tracing/pycrunch_tracer/demo/factorial_demo.py'
    code_clone.co_argcount = 1

    sim_frame = models.Frame()
    sim_frame.f_lineno = 11
    sim_frame.f_locals = {
        'num': 6}
    sim_frame.f_code = code_clone
    evt = SimulationEvent(sim_frame, 'line', None)

    return evt


def create_event_16():
    code_clone = models.Code()
    code_clone.co_name = 'my_factorial'
    code_clone.co_filename = '/Users/gleb/code/pycrunch_tracing/pycrunch_tracer/demo/factorial_demo.py'
    code_clone.co_argcount = 1

    sim_frame = models.Frame()
    sim_frame.f_lineno = 7
    sim_frame.f_locals = {
        'num': 5}
    sim_frame.f_code = code_clone
    evt = SimulationEvent(sim_frame, 'call', None)

    return evt


def create_event_17():
    code_clone = models.Code()
    code_clone.co_name = 'my_factorial'
    code_clone.co_filename = '/Users/gleb/code/pycrunch_tracing/pycrunch_tracer/demo/factorial_demo.py'
    code_clone.co_argcount = 1

    sim_frame = models.Frame()
    sim_frame.f_lineno = 8
    sim_frame.f_locals = {
        'num': 5}
    sim_frame.f_code = code_clone
    evt = SimulationEvent(sim_frame, 'line', None)

    return evt


def create_event_18():
    code_clone = models.Code()
    code_clone.co_name = 'my_factorial'
    code_clone.co_filename = '/Users/gleb/code/pycrunch_tracing/pycrunch_tracer/demo/factorial_demo.py'
    code_clone.co_argcount = 1

    sim_frame = models.Frame()
    sim_frame.f_lineno = 11
    sim_frame.f_locals = {
        'num': 5}
    sim_frame.f_code = code_clone
    evt = SimulationEvent(sim_frame, 'line', None)

    return evt


def create_event_19():
    code_clone = models.Code()
    code_clone.co_name = 'my_factorial'
    code_clone.co_filename = '/Users/gleb/code/pycrunch_tracing/pycrunch_tracer/demo/factorial_demo.py'
    code_clone.co_argcount = 1

    sim_frame = models.Frame()
    sim_frame.f_lineno = 7
    sim_frame.f_locals = {
        'num': 4}
    sim_frame.f_code = code_clone
    evt = SimulationEvent(sim_frame, 'call', None)

    return evt


def create_event_20():
    code_clone = models.Code()
    code_clone.co_name = 'my_factorial'
    code_clone.co_filename = '/Users/gleb/code/pycrunch_tracing/pycrunch_tracer/demo/factorial_demo.py'
    code_clone.co_argcount = 1

    sim_frame = models.Frame()
    sim_frame.f_lineno = 8
    sim_frame.f_locals = {
        'num': 4}
    sim_frame.f_code = code_clone
    evt = SimulationEvent(sim_frame, 'line', None)

    return evt


def create_event_21():
    code_clone = models.Code()
    code_clone.co_name = 'my_factorial'
    code_clone.co_filename = '/Users/gleb/code/pycrunch_tracing/pycrunch_tracer/demo/factorial_demo.py'
    code_clone.co_argcount = 1

    sim_frame = models.Frame()
    sim_frame.f_lineno = 11
    sim_frame.f_locals = {
        'num': 4}
    sim_frame.f_code = code_clone
    evt = SimulationEvent(sim_frame, 'line', None)

    return evt


def create_event_22():
    code_clone = models.Code()
    code_clone.co_name = 'my_factorial'
    code_clone.co_filename = '/Users/gleb/code/pycrunch_tracing/pycrunch_tracer/demo/factorial_demo.py'
    code_clone.co_argcount = 1

    sim_frame = models.Frame()
    sim_frame.f_lineno = 7
    sim_frame.f_locals = {
        'num': 3}
    sim_frame.f_code = code_clone
    evt = SimulationEvent(sim_frame, 'call', None)

    return evt


def create_event_23():
    code_clone = models.Code()
    code_clone.co_name = 'my_factorial'
    code_clone.co_filename = '/Users/gleb/code/pycrunch_tracing/pycrunch_tracer/demo/factorial_demo.py'
    code_clone.co_argcount = 1

    sim_frame = models.Frame()
    sim_frame.f_lineno = 8
    sim_frame.f_locals = {
        'num': 3}
    sim_frame.f_code = code_clone
    evt = SimulationEvent(sim_frame, 'line', None)

    return evt


def create_event_24():
    code_clone = models.Code()
    code_clone.co_name = 'my_factorial'
    code_clone.co_filename = '/Users/gleb/code/pycrunch_tracing/pycrunch_tracer/demo/factorial_demo.py'
    code_clone.co_argcount = 1

    sim_frame = models.Frame()
    sim_frame.f_lineno = 11
    sim_frame.f_locals = {
        'num': 3}
    sim_frame.f_code = code_clone
    evt = SimulationEvent(sim_frame, 'line', None)

    return evt


def create_event_25():
    code_clone = models.Code()
    code_clone.co_name = 'my_factorial'
    code_clone.co_filename = '/Users/gleb/code/pycrunch_tracing/pycrunch_tracer/demo/factorial_demo.py'
    code_clone.co_argcount = 1

    sim_frame = models.Frame()
    sim_frame.f_lineno = 7
    sim_frame.f_locals = {
        'num': 2}
    sim_frame.f_code = code_clone
    evt = SimulationEvent(sim_frame, 'call', None)

    return evt


def create_event_26():
    code_clone = models.Code()
    code_clone.co_name = 'my_factorial'
    code_clone.co_filename = '/Users/gleb/code/pycrunch_tracing/pycrunch_tracer/demo/factorial_demo.py'
    code_clone.co_argcount = 1

    sim_frame = models.Frame()
    sim_frame.f_lineno = 8
    sim_frame.f_locals = {
        'num': 2}
    sim_frame.f_code = code_clone
    evt = SimulationEvent(sim_frame, 'line', None)

    return evt


def create_event_27():
    code_clone = models.Code()
    code_clone.co_name = 'my_factorial'
    code_clone.co_filename = '/Users/gleb/code/pycrunch_tracing/pycrunch_tracer/demo/factorial_demo.py'
    code_clone.co_argcount = 1

    sim_frame = models.Frame()
    sim_frame.f_lineno = 11
    sim_frame.f_locals = {
        'num': 2}
    sim_frame.f_code = code_clone
    evt = SimulationEvent(sim_frame, 'line', None)

    return evt


def create_event_28():
    code_clone = models.Code()
    code_clone.co_name = 'my_factorial'
    code_clone.co_filename = '/Users/gleb/code/pycrunch_tracing/pycrunch_tracer/demo/factorial_demo.py'
    code_clone.co_argcount = 1

    sim_frame = models.Frame()
    sim_frame.f_lineno = 7
    sim_frame.f_locals = {
        'num': 1}
    sim_frame.f_code = code_clone
    evt = SimulationEvent(sim_frame, 'call', None)

    return evt


def create_event_29():
    code_clone = models.Code()
    code_clone.co_name = 'my_factorial'
    code_clone.co_filename = '/Users/gleb/code/pycrunch_tracing/pycrunch_tracer/demo/factorial_demo.py'
    code_clone.co_argcount = 1

    sim_frame = models.Frame()
    sim_frame.f_lineno = 8
    sim_frame.f_locals = {
        'num': 1}
    sim_frame.f_code = code_clone
    evt = SimulationEvent(sim_frame, 'line', None)

    return evt


def create_event_30():
    code_clone = models.Code()
    code_clone.co_name = 'my_factorial'
    code_clone.co_filename = '/Users/gleb/code/pycrunch_tracing/pycrunch_tracer/demo/factorial_demo.py'
    code_clone.co_argcount = 1

    sim_frame = models.Frame()
    sim_frame.f_lineno = 9
    sim_frame.f_locals = {
        'num': 1}
    sim_frame.f_code = code_clone
    evt = SimulationEvent(sim_frame, 'line', None)

    return evt


def create_event_31():
    code_clone = models.Code()
    code_clone.co_name = 'my_factorial'
    code_clone.co_filename = '/Users/gleb/code/pycrunch_tracing/pycrunch_tracer/demo/factorial_demo.py'
    code_clone.co_argcount = 1

    sim_frame = models.Frame()
    sim_frame.f_lineno = 9
    sim_frame.f_locals = {
        'num': 1}
    sim_frame.f_code = code_clone
    evt = SimulationEvent(sim_frame, 'return', 1)

    return evt


def create_event_32():
    code_clone = models.Code()
    code_clone.co_name = 'my_factorial'
    code_clone.co_filename = '/Users/gleb/code/pycrunch_tracing/pycrunch_tracer/demo/factorial_demo.py'
    code_clone.co_argcount = 1

    sim_frame = models.Frame()
    sim_frame.f_lineno = 11
    sim_frame.f_locals = {
        'num': 2}
    sim_frame.f_code = code_clone
    evt = SimulationEvent(sim_frame, 'return', 2)

    return evt


def create_event_33():
    code_clone = models.Code()
    code_clone.co_name = 'my_factorial'
    code_clone.co_filename = '/Users/gleb/code/pycrunch_tracing/pycrunch_tracer/demo/factorial_demo.py'
    code_clone.co_argcount = 1

    sim_frame = models.Frame()
    sim_frame.f_lineno = 11
    sim_frame.f_locals = {
        'num': 3}
    sim_frame.f_code = code_clone
    evt = SimulationEvent(sim_frame, 'return', 6)

    return evt


def create_event_34():
    code_clone = models.Code()
    code_clone.co_name = 'my_factorial'
    code_clone.co_filename = '/Users/gleb/code/pycrunch_tracing/pycrunch_tracer/demo/factorial_demo.py'
    code_clone.co_argcount = 1

    sim_frame = models.Frame()
    sim_frame.f_lineno = 11
    sim_frame.f_locals = {
        'num': 4}
    sim_frame.f_code = code_clone
    evt = SimulationEvent(sim_frame, 'return', 24)

    return evt


def create_event_35():
    code_clone = models.Code()
    code_clone.co_name = 'my_factorial'
    code_clone.co_filename = '/Users/gleb/code/pycrunch_tracing/pycrunch_tracer/demo/factorial_demo.py'
    code_clone.co_argcount = 1

    sim_frame = models.Frame()
    sim_frame.f_lineno = 11
    sim_frame.f_locals = {
        'num': 5}
    sim_frame.f_code = code_clone
    evt = SimulationEvent(sim_frame, 'return', 120)

    return evt


def create_event_36():
    code_clone = models.Code()
    code_clone.co_name = 'my_factorial'
    code_clone.co_filename = '/Users/gleb/code/pycrunch_tracing/pycrunch_tracer/demo/factorial_demo.py'
    code_clone.co_argcount = 1

    sim_frame = models.Frame()
    sim_frame.f_lineno = 11
    sim_frame.f_locals = {
        'num': 6}
    sim_frame.f_code = code_clone
    evt = SimulationEvent(sim_frame, 'return', 720)

    return evt


def create_event_37():
    code_clone = models.Code()
    code_clone.co_name = 'my_factorial'
    code_clone.co_filename = '/Users/gleb/code/pycrunch_tracing/pycrunch_tracer/demo/factorial_demo.py'
    code_clone.co_argcount = 1

    sim_frame = models.Frame()
    sim_frame.f_lineno = 11
    sim_frame.f_locals = {
        'num': 7}
    sim_frame.f_code = code_clone
    evt = SimulationEvent(sim_frame, 'return', 5040)

    return evt


def create_event_38():
    code_clone = models.Code()
    code_clone.co_name = 'my_factorial'
    code_clone.co_filename = '/Users/gleb/code/pycrunch_tracing/pycrunch_tracer/demo/factorial_demo.py'
    code_clone.co_argcount = 1

    sim_frame = models.Frame()
    sim_frame.f_lineno = 11
    sim_frame.f_locals = {
        'num': 8}
    sim_frame.f_code = code_clone
    evt = SimulationEvent(sim_frame, 'return', 40320)

    return evt


def create_event_39():
    code_clone = models.Code()
    code_clone.co_name = 'my_factorial'
    code_clone.co_filename = '/Users/gleb/code/pycrunch_tracing/pycrunch_tracer/demo/factorial_demo.py'
    code_clone.co_argcount = 1

    sim_frame = models.Frame()
    sim_frame.f_lineno = 11
    sim_frame.f_locals = {
        'num': 9}
    sim_frame.f_code = code_clone
    evt = SimulationEvent(sim_frame, 'return', 362880)

    return evt


def create_event_40():
    code_clone = models.Code()
    code_clone.co_name = 'my_factorial'
    code_clone.co_filename = '/Users/gleb/code/pycrunch_tracing/pycrunch_tracer/demo/factorial_demo.py'
    code_clone.co_argcount = 1

    sim_frame = models.Frame()
    sim_frame.f_lineno = 11
    sim_frame.f_locals = {
        'num': 10}
    sim_frame.f_code = code_clone
    evt = SimulationEvent(sim_frame, 'return', 3628800)

    return evt


def test_simulated():
    events = []
    events.append(create_event_1())
    events.append(create_event_2())
    events.append(create_event_3())
    events.append(create_event_4())
    events.append(create_event_5())
    events.append(create_event_6())
    events.append(create_event_7())
    events.append(create_event_8())
    events.append(create_event_9())
    events.append(create_event_10())
    events.append(create_event_11())
    events.append(create_event_12())
    events.append(create_event_13())
    events.append(create_event_14())
    events.append(create_event_15())
    events.append(create_event_16())
    events.append(create_event_17())
    events.append(create_event_18())
    events.append(create_event_19())
    events.append(create_event_20())
    events.append(create_event_21())
    events.append(create_event_22())
    events.append(create_event_23())
    events.append(create_event_24())
    events.append(create_event_25())
    events.append(create_event_26())
    events.append(create_event_27())
    events.append(create_event_28())
    events.append(create_event_29())
    events.append(create_event_30())
    events.append(create_event_31())
    events.append(create_event_32())
    events.append(create_event_33())
    events.append(create_event_34())
    events.append(create_event_35())
    events.append(create_event_36())
    events.append(create_event_37())
    events.append(create_event_38())
    events.append(create_event_39())
    events.append(create_event_40())

    event_buffer = []
    sut = SimpleTracer(event_buffer, 'sim_round', DefaultFileFilter(),)
    for x in events:
        sut.simple_tracer(x.frame, x.event, x.arg)

    x2 = to_string(event_buffer)
    trace(x2=x2)

    array_round = jsonpickle.decode(x2)
    # trace(array_round=array_round)
    # ss = SessionStore()
    # ses = ss.new_session('round_demo')
    # ses.save_with_metadata()

    bytesAsString = event_buffer_in_protobuf.EventBufferInProtobuf(event_buffer, x.file_map).as_bytes()
    trace(vbbbb=str(bytesAsString))
    print(len(bytesAsString))
    session_round = message_pb2.TraceSession()

    x = session_round.ParseFromString(bytesAsString)
    print(x)