from pathlib import Path

from pycrunch_trace.filters import CustomFileFilter
from pycrunch_trace.oop import Clock, File
from pycrunch_trace.tracing.simulation import models
from pycrunch_trace.tracing.simple_tracer import SimpleTracer
from pycrunch_trace.tracing.simulator_sink import SimulationEvent


def create_event_1():
    code_clone = models.Code()
    code_clone.co_name = 'a___'
    code_clone.co_filename = '/pycrunch_tracer/demo/demo_tree_v1.py'
    code_clone.co_argcount = 0

    sim_frame = models.Frame()
    sim_frame.f_lineno = 23
    sim_frame.f_locals = {}
    sim_frame.f_code = code_clone
    evt = SimulationEvent(sim_frame, 'call', None)

    return evt


def create_event_2():
    code_clone = models.Code()
    code_clone.co_name = 'a___'
    code_clone.co_filename = '/pycrunch_tracer/demo/demo_tree_v1.py'
    code_clone.co_argcount = 0

    sim_frame = models.Frame()
    sim_frame.f_lineno = 24
    sim_frame.f_locals = {}
    sim_frame.f_code = code_clone
    evt = SimulationEvent(sim_frame, 'line', None)

    return evt


def create_event_3():
    code_clone = models.Code()
    code_clone.co_name = 'a___'
    code_clone.co_filename = '/pycrunch_tracer/demo/demo_tree_v1.py'
    code_clone.co_argcount = 0

    sim_frame = models.Frame()
    sim_frame.f_lineno = 25
    sim_frame.f_locals = {
        'a': 1}
    sim_frame.f_code = code_clone
    evt = SimulationEvent(sim_frame, 'line', None)

    return evt


def create_event_4():
    code_clone = models.Code()
    code_clone.co_name = 'a___'
    code_clone.co_filename = '/pycrunch_tracer/demo/demo_tree_v1.py'
    code_clone.co_argcount = 0

    sim_frame = models.Frame()
    sim_frame.f_lineno = 26
    sim_frame.f_locals = {
        'a': 1,
        'b': 2}
    sim_frame.f_code = code_clone
    evt = SimulationEvent(sim_frame, 'line', None)

    return evt


def create_event_5():
    code_clone = models.Code()
    code_clone.co_name = 'b___'
    code_clone.co_filename = '/pycrunch_tracer/demo/demo_tree_v1.py'
    code_clone.co_argcount = 0

    sim_frame = models.Frame()
    sim_frame.f_lineno = 15
    sim_frame.f_locals = {}
    sim_frame.f_code = code_clone
    evt = SimulationEvent(sim_frame, 'call', None)

    return evt


def create_event_6():
    code_clone = models.Code()
    code_clone.co_name = 'b___'
    code_clone.co_filename = '/pycrunch_tracer/demo/demo_tree_v1.py'
    code_clone.co_argcount = 0

    sim_frame = models.Frame()
    sim_frame.f_lineno = 16
    sim_frame.f_locals = {}
    sim_frame.f_code = code_clone
    evt = SimulationEvent(sim_frame, 'line', None)

    return evt


def create_event_7():
    code_clone = models.Code()
    code_clone.co_name = 'b___'
    code_clone.co_filename = '/pycrunch_tracer/demo/demo_tree_v1.py'
    code_clone.co_argcount = 0

    sim_frame = models.Frame()
    sim_frame.f_lineno = 17
    sim_frame.f_locals = {
        'a': 1}
    sim_frame.f_code = code_clone
    evt = SimulationEvent(sim_frame, 'line', None)

    return evt


def create_event_8():
    code_clone = models.Code()
    code_clone.co_name = 'c___'
    code_clone.co_filename = '/pycrunch_tracer/demo/demo_tree_v1.py'
    code_clone.co_argcount = 0

    sim_frame = models.Frame()
    sim_frame.f_lineno = 8
    sim_frame.f_locals = {}
    sim_frame.f_code = code_clone
    evt = SimulationEvent(sim_frame, 'call', None)

    return evt


def create_event_9():
    code_clone = models.Code()
    code_clone.co_name = 'c___'
    code_clone.co_filename = '/pycrunch_tracer/demo/demo_tree_v1.py'
    code_clone.co_argcount = 0

    sim_frame = models.Frame()
    sim_frame.f_lineno = 9
    sim_frame.f_locals = {}
    sim_frame.f_code = code_clone
    evt = SimulationEvent(sim_frame, 'line', None)

    return evt


def create_event_10():
    code_clone = models.Code()
    code_clone.co_name = 'c___'
    code_clone.co_filename = '/pycrunch_tracer/demo/demo_tree_v1.py'
    code_clone.co_argcount = 0

    sim_frame = models.Frame()
    sim_frame.f_lineno = 10
    sim_frame.f_locals = {
        'a': 1}
    sim_frame.f_code = code_clone
    evt = SimulationEvent(sim_frame, 'line', None)

    return evt


def create_event_11():
    code_clone = models.Code()
    code_clone.co_name = 'c___'
    code_clone.co_filename = '/pycrunch_tracer/demo/demo_tree_v1.py'
    code_clone.co_argcount = 0

    sim_frame = models.Frame()
    sim_frame.f_lineno = 11
    sim_frame.f_locals = {
        'a': 1,
        'b': 2}
    sim_frame.f_code = code_clone
    evt = SimulationEvent(sim_frame, 'line', None)

    return evt


def create_event_12():
    code_clone = models.Code()
    code_clone.co_name = 'd___'
    code_clone.co_filename = '/pycrunch_tracer/demo/demo_tree_v1.py'
    code_clone.co_argcount = 0

    sim_frame = models.Frame()
    sim_frame.f_lineno = 3
    sim_frame.f_locals = {}
    sim_frame.f_code = code_clone
    evt = SimulationEvent(sim_frame, 'call', None)

    return evt


def create_event_13():
    code_clone = models.Code()
    code_clone.co_name = 'd___'
    code_clone.co_filename = '/pycrunch_tracer/demo/demo_tree_v1.py'
    code_clone.co_argcount = 0

    sim_frame = models.Frame()
    sim_frame.f_lineno = 4
    sim_frame.f_locals = {}
    sim_frame.f_code = code_clone
    evt = SimulationEvent(sim_frame, 'line', None)

    return evt


def create_event_14():
    code_clone = models.Code()
    code_clone.co_name = 'd___'
    code_clone.co_filename = '/pycrunch_tracer/demo/demo_tree_v1.py'
    code_clone.co_argcount = 0

    sim_frame = models.Frame()
    sim_frame.f_lineno = 5
    sim_frame.f_locals = {
        'a': 1}
    sim_frame.f_code = code_clone
    evt = SimulationEvent(sim_frame, 'line', None)

    return evt


def create_event_15():
    code_clone = models.Code()
    code_clone.co_name = 'd___'
    code_clone.co_filename = '/pycrunch_tracer/demo/demo_tree_v1.py'
    code_clone.co_argcount = 0

    sim_frame = models.Frame()
    sim_frame.f_lineno = 6
    sim_frame.f_locals = {
        'a': 1,
        'b': 2}
    sim_frame.f_code = code_clone
    evt = SimulationEvent(sim_frame, 'line', None)

    return evt


def create_event_16():
    code_clone = models.Code()
    code_clone.co_name = 'd___'
    code_clone.co_filename = '/pycrunch_tracer/demo/demo_tree_v1.py'
    code_clone.co_argcount = 0

    sim_frame = models.Frame()
    sim_frame.f_lineno = 6
    sim_frame.f_locals = {
        'a': 1,
        'b': 2,
        'c': 3}
    sim_frame.f_code = code_clone
    evt = SimulationEvent(sim_frame, 'return', None)

    return evt


def create_event_17():
    code_clone = models.Code()
    code_clone.co_name = 'c___'
    code_clone.co_filename = '/pycrunch_tracer/demo/demo_tree_v1.py'
    code_clone.co_argcount = 0

    sim_frame = models.Frame()
    sim_frame.f_lineno = 12
    sim_frame.f_locals = {
        'a': 1,
        'b': 2}
    sim_frame.f_code = code_clone
    evt = SimulationEvent(sim_frame, 'line', None)

    return evt


def create_event_18():
    code_clone = models.Code()
    code_clone.co_name = 'c___'
    code_clone.co_filename = '/pycrunch_tracer/demo/demo_tree_v1.py'
    code_clone.co_argcount = 0

    sim_frame = models.Frame()
    sim_frame.f_lineno = 12
    sim_frame.f_locals = {
        'a': 1,
        'b': 2,
        'c': 3}
    sim_frame.f_code = code_clone
    evt = SimulationEvent(sim_frame, 'return', None)

    return evt


def create_event_19():
    code_clone = models.Code()
    code_clone.co_name = 'b___'
    code_clone.co_filename = '/pycrunch_tracer/demo/demo_tree_v1.py'
    code_clone.co_argcount = 0

    sim_frame = models.Frame()
    sim_frame.f_lineno = 18
    sim_frame.f_locals = {
        'a': 1}
    sim_frame.f_code = code_clone
    evt = SimulationEvent(sim_frame, 'line', None)

    return evt


def create_event_20():
    code_clone = models.Code()
    code_clone.co_name = 'b___'
    code_clone.co_filename = '/pycrunch_tracer/demo/demo_tree_v1.py'
    code_clone.co_argcount = 0

    sim_frame = models.Frame()
    sim_frame.f_lineno = 19
    sim_frame.f_locals = {
        'a': 1,
        'b': 2}
    sim_frame.f_code = code_clone
    evt = SimulationEvent(sim_frame, 'line', None)

    return evt


def create_event_21():
    code_clone = models.Code()
    code_clone.co_name = 'b___'
    code_clone.co_filename = '/pycrunch_tracer/demo/demo_tree_v1.py'
    code_clone.co_argcount = 0

    sim_frame = models.Frame()
    sim_frame.f_lineno = 19
    sim_frame.f_locals = {
        'a': 1,
        'b': 2,
        'c': 3}
    sim_frame.f_code = code_clone
    evt = SimulationEvent(sim_frame, 'return', None)

    return evt


def create_event_22():
    code_clone = models.Code()
    code_clone.co_name = 'a___'
    code_clone.co_filename = '/pycrunch_tracer/demo/demo_tree_v1.py'
    code_clone.co_argcount = 0

    sim_frame = models.Frame()
    sim_frame.f_lineno = 27
    sim_frame.f_locals = {
        'a': 1,
        'b': 2}
    sim_frame.f_code = code_clone
    evt = SimulationEvent(sim_frame, 'line', None)

    return evt


def create_event_23():
    code_clone = models.Code()
    code_clone.co_name = 'a___'
    code_clone.co_filename = '/pycrunch_tracer/demo/demo_tree_v1.py'
    code_clone.co_argcount = 0

    sim_frame = models.Frame()
    sim_frame.f_lineno = 27
    sim_frame.f_locals = {
        'a': 1,
        'b': 2,
        'c': 3}
    sim_frame.f_code = code_clone
    evt = SimulationEvent(sim_frame, 'return', None)

    return evt


def create_event_24():
    code_clone = models.Code()
    code_clone.co_name = 'stop'
    code_clone.co_filename = '/pycrunch_tracer/client/api/tracing.py'
    code_clone.co_argcount = 1

    sim_frame = models.Frame()
    sim_frame.f_lineno = 70
    sim_frame.f_locals = {
        'self': '< pycrunch_tracer.api.tracing'}

    sim_frame.f_code = code_clone
    evt = SimulationEvent(sim_frame, 'call', None)

    return evt


def create_event_25():
    code_clone = models.Code()
    code_clone.co_name = 'stop'
    code_clone.co_filename = '/pycrunch_tracer/client/api/tracing.py'
    code_clone.co_argcount = 1

    sim_frame = models.Frame()
    sim_frame.f_lineno = 71
    sim_frame.f_locals = {   'self': '< pycrunch_tracer.api.tracing'}
    sim_frame.f_code = code_clone
    evt = SimulationEvent(sim_frame, 'line', None)

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
    package_directory = Path(__file__).parent.parent.parent
    profile_name = 'default.profile.yaml'

    f_filter = CustomFileFilter(File(package_directory.joinpath('pycrunch-profiles', profile_name)))

    sut = SimpleTracer(events, 'sim_round2', f_filter, Clock(), self.outgoingQueue)
    for (i, x) in enumerate(events):
        if i > 24:
            break
        print(i)
        sut.simple_tracer(x.frame, x.event, x.arg)

