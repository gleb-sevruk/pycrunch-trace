from typing import List, Any, Optional

from pycrunch_trace.tracing.simulation import models
from pycrunch_trace.tracing.simulation.models import Frame


class SimulationEvent:
    frame: Frame
    event: str
    arg: Optional[Any]

    def __init__(self, frame: models.Frame, event: str, arg: Optional[Any]):
        self.arg = arg
        self.event = event
        self.frame = frame


class SimulationEventAsCode:
    origin: SimulationEvent

    def __init__(self, origin: SimulationEvent):
        self.origin = origin

    def as_python_code(self, index: int):
        x = f"""
def create_event_{index}():
    code_clone = models.Code()
    code_clone.co_name = '{self.origin.frame.f_code.co_name}'
    code_clone.co_filename = '{self.origin.frame.f_code.co_filename}'
    code_clone.co_argcount = {self.origin.frame.f_code.co_argcount}
    
    sim_frame = models.Frame()
    sim_frame.f_lineno = {self.origin.frame.f_lineno}
    sim_frame.f_locals = {self.origin.frame.f_locals}
    sim_frame.f_code = code_clone
    evt = SimulationEvent(sim_frame, '{self.origin.event}', {self.origin.arg})

    return evt
    
"""
        return x

class DisabledSimulatorSink(object):
    def save_for_simulator(self, frame: models.Frame, event: str, arg):
        pass

class SimulatorSink:
    current_index: int
    simulation: List[str]

    def __init__(self):
        self.simulation = []
        self.current_index = 1

    def simulated_code(self):
        imports_code = """
from pycrunch_trace.simulation import models
from pycrunch_trace.tracing.simulator_sink import SimulationEvent

        """

        events = ''.join(self.simulation)

        test_code = """
def test_simulated():
    events = []"""
        for x in range(1, self.current_index):
            test_code += f'\n    events.append(create_event_{x}())'
        return imports_code + events + test_code

    def save_for_simulator(self, frame: models.Frame, event: str, arg):
        code = frame.f_code

        code_clone = models.Code()
        code_clone.co_name = code.co_name
        code_clone.co_filename = code.co_filename
        code_clone.co_argcount = code.co_argcount

        clone = models.Frame()
        clone.f_lineno = frame.f_lineno
        clone.f_locals = frame.f_locals
        clone.f_code = code_clone
        self.simulation.append(SimulationEventAsCode(SimulationEvent(clone, event, arg)).as_python_code(self.current_index))
        self.current_index += 1
