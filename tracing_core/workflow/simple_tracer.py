
import tracing_core.simulation.models as models
import tracing_core.events.method_enter as events
from tracing_core.events.method_enter import ExecutionCursor
from tracing_core.filters.file_filtering import FileFilter
from tracing_core.filters.types_filter import can_trace_type
from tracing_core.simulation.models import EventKeys


class SimpleTracer:
    event_buffer: list

    def __init__(self, event_buffer):
        self.event_buffer = event_buffer
        self.file_filter = FileFilter()
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

        print(f"[{co.co_argcount}]{event}: {func_name} {line_no} -> {arg}")
        print(f"   {frame.f_locals}")
        return self.simple_tracer

    def process_events(self, event: str, frame: models.Frame, arg):
        cursor = events.ExecutionCursor(frame.f_code.co_filename, frame.f_lineno)
        if event == EventKeys.call:
            current = events.MethodEnterEvent(cursor)
            variables = current.input_variables
            self.push_traceable_variables(frame, variables)
            self.event_buffer.append(current)

        if event == EventKeys.line:
            current = events.LineExecutionEvent(cursor)
            self.push_traceable_variables(frame, current.locals)
            self.event_buffer.append(current)

        if event == EventKeys.event_return:
            current = events.MethodExitEvent(cursor)
            current.return_variables.push_variable('__return', arg)
            self.push_traceable_variables(frame, current.locals)
            self.event_buffer.append(current)

    def push_traceable_variables(self, frame, variables):
        for (name, value) in frame.f_locals.items():
            if can_trace_type(value):
                variables.push_variable(name, value)
            else:
                no_way_to_show_on_ui = str(type(value))
                variables.push_variable(name, no_way_to_show_on_ui)

