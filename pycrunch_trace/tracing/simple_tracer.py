import sys

import pycrunch_trace.tracing.simulation.models as models
import pycrunch_trace.events.method_enter as events
from pycrunch_trace.client.command_buffer import ArrayCommandBuffer
from pycrunch_trace.client.networking.commands import EventsSlice
from pycrunch_trace.file_system.trace_session import TraceSession
from pycrunch_trace.filters import AbstractFileFilter
from pycrunch_trace.oop import Clock
from pycrunch_trace.tracing.call_stack import CallStack
from pycrunch_trace.tracing.file_map import FileMap
from pycrunch_trace.tracing.perf import TracerPerf
from pycrunch_trace.tracing.simulation import EventKeys
from pycrunch_trace.tracing.simulator_sink import SimulatorSink, DisabledSimulatorSink


class SimpleTracer:
    file_map: FileMap
    event_number: int
    file_filter: AbstractFileFilter
    event_buffer: ArrayCommandBuffer
    call_stack: CallStack
    session: TraceSession
    simulation: SimulatorSink
    events_so_far: int

    def __init__(self, event_buffer, session_name, file_filter: AbstractFileFilter, clock: Clock, queue):
        self.event_number = 1
        self.events_so_far = 0
        self.clock = clock
        self.event_buffer = event_buffer
        self.file_filter = file_filter
        self.should_record_variables = file_filter.should_record_variables()
        self.call_stack = CallStack()
        self.session = TraceSession()
        self.simulation = DisabledSimulatorSink()
        # self.simulation = SimulatorSink()
        self.file_map = FileMap()
        self.perf = TracerPerf()
        self.queue = queue
        self.max_events_before_send = 1000
        self.threshold_before_switching_to_sampling = 1000000
        self.skip = False
        # interval = sys.getscheckinterval()
        # print(f'interval {interval}')
        # sys.setcheckinterval(100000000)

        # interval = sys.getswitchinterval()
        #
        # print(f'getswitchinterval {interval}')
        # sys.setswitchinterval(3)
        # interval = sys.getswitchinterval()
        # print(f'getswitchinterval {interval}')

    def simple_tracer(self, frame: models.Frame, event: str, arg):
        entered_at = self.clock.now()
        self.process_events(entered_at, event, frame, arg)
        # self.simulation.save_for_simulator(frame, event, arg)

        # print(f"[{co.co_argcount}]{event}: {func_name} {line_no} -> {arg}")
        # print(f"   {frame.f_locals}")

        end_at = self.clock.now()
        diff = end_at - entered_at
        self.perf.did_execute_line(diff)
        return self.simple_tracer

    def process_events(self, now: float, event: str, frame: models.Frame, arg):
        file_path_under_cursor = frame.f_code.co_filename
        if not self.file_filter.should_trace(file_path_under_cursor):
            will_record_current_event = False
            self.session.will_skip_file(file_path_under_cursor)
        else:
            will_record_current_event = True
            self.events_so_far += 1
            self.session.did_enter_traceable_file(file_path_under_cursor)

        if event == EventKeys.line:
            over_threshold = self.events_so_far > self.threshold_before_switching_to_sampling
            if will_record_current_event and not over_threshold:
                cursor = self.create_cursor(file_path_under_cursor, frame)
                self.call_stack.new_cursor_in_current_frame(cursor)

                stack = self.get_execution_stack()
                current = events.LineExecutionEvent(cursor, stack, now)
                if self.should_record_variables:
                    self.push_traceable_variables(frame, current.locals)
                self.add_to_event_buffer(current)

        if event == EventKeys.call:
            cursor = self.create_cursor(file_path_under_cursor, frame)
            self.call_stack.enter_frame(cursor)
            # lets try to add methods
            # [if sampling mode]
            if will_record_current_event:
                current = events.MethodEnterEvent(cursor, self.get_execution_stack(), now)
                if self.should_record_variables:
                    variables = current.input_variables
                    self.push_traceable_variables(frame, variables)
                self.add_to_event_buffer(current)

        if event == EventKeys.event_return:
            self.call_stack.exit_frame()
            # [? is sampling]
            if will_record_current_event:
                cursor = self.create_cursor(file_path_under_cursor, frame)
                current = events.MethodExitEvent(cursor, self.get_execution_stack(), now)
                if self.should_record_variables:
                    current.return_variables.push_variable('__return', arg)
                    self.push_traceable_variables(frame, current.locals)
                self.add_to_event_buffer(current)

        self.flush_queue_if_full()

    def add_to_event_buffer(self, current):
        # todo: is this caused because of array dynamic size/doubling?
        # if True:
        #     return
        self.event_buffer.add_event(current)

    def create_cursor(self, file_path_under_cursor, frame):
        file_id = self.file_map.file_id(file_path_under_cursor)
        cursor = events.ExecutionCursor(file_id, frame.f_lineno, frame.f_code.co_name)
        return cursor

    def get_execution_stack(self):
        return self.call_stack.current_frame()

    def push_traceable_variables(self, frame, variables):
        for (name, value) in frame.f_locals.items():
            # todo use variable values diffing
            variables.push_variable(name, value)

    def flush_outstanding_events(self):
        old_buffer = self.event_buffer.finish_chunk()
        self.perf.print_avg_time()

        self.queue.put_events(EventsSlice(self.session.session_name, self.event_number, old_buffer, self.file_map.files.copy()))
        self.event_number += 1

    def flush_queue_if_full(self):
        if self.event_buffer.how_many_events() >= self.max_events_before_send:
            self.flush_outstanding_events()
