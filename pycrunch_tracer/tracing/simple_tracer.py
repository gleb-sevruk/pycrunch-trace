import collections

import pycrunch_tracer.simulation.models as models
import pycrunch_tracer.events.method_enter as events
from pycrunch_tracer.filters import FileFilter
from pycrunch_tracer.simulation import EventKeys


class CallStack:
    def __init__(self):
        self.stack = collections.deque()

    def enter_frame(self, execution_cursor: events.ExecutionCursor):
        self.stack.append(execution_cursor)

    def exit_frame(self):
        self.stack.pop()

    def to_list(self):
        results = []
        for x in self.stack:
            results.append(f'{x.file}:{x.line}')

        return list(reversed(results))


class SimpleTracer:
    event_buffer: list
    call_stack: CallStack

    def __init__(self, event_buffer):
        self.event_buffer = event_buffer
        self.file_filter = FileFilter()
        self.call_stack = CallStack()
        pass

    def simple_tracer(self, frame: models.Frame, event: str, arg):
        f_type = type(frame)
        # print(f_type.__module__ + '.' + f_type.__qualname__)
        co = frame.f_code
        func_name = co.co_name
        func_filename = co.co_filename
        line_no = frame.f_lineno
        if not self.file_filter.should_trace(func_filename):
            # Ignore calls not in this module
            return

        self.process_events(event, frame, arg)

        # print(f"[{co.co_argcount}]{event}: {func_name} {line_no} -> {arg}")
        # print(f"   {frame.f_locals}")
        return self.simple_tracer

    def process_events(self, event: str, frame: models.Frame, arg):
        cursor = events.ExecutionCursor(frame.f_code.co_filename, frame.f_lineno)
        if event == EventKeys.call:
            self.call_stack.enter_frame(cursor)
            current = events.MethodEnterEvent(cursor, self.get_execution_stack())
            variables = current.input_variables
            self.push_traceable_variables(frame, variables)
            self.event_buffer.append(current)

        if event == EventKeys.line:
            current = events.LineExecutionEvent(cursor, self.get_execution_stack())
            self.push_traceable_variables(frame, current.locals)
            self.event_buffer.append(current)

        if event == EventKeys.event_return:
            self.call_stack.exit_frame()
            current = events.MethodExitEvent(cursor, self.get_execution_stack())
            current.return_variables.push_variable('__return', arg)
            self.push_traceable_variables(frame, current.locals)
            self.event_buffer.append(current)

    def get_execution_stack(self):
        return self.call_stack.to_list()

    def push_traceable_variables(self, frame, variables):
        for (name, value) in frame.f_locals.items():
            variables.push_variable(name, value)

