import collections
from typing import List

import pycrunch_tracer.tracing.simulation.models as models
import pycrunch_tracer.events.method_enter as events
from pycrunch_tracer.client.networking.commands import EventsSlice
from pycrunch_tracer.file_system.trace_session import TraceSession
from pycrunch_tracer.filters import AbstractFileFilter
from pycrunch_tracer.oop import Clock
from pycrunch_tracer.tracing.simulation import EventKeys
from pycrunch_tracer.tracing.simulator_sink import SimulatorSink, DisabledSimulatorSink


class CallStack:
    def __init__(self):
        self.stack = collections.deque()

    def enter_frame(self, execution_cursor: events.ExecutionCursor):
        parent_frame = self.get_parent_frame()
        # print(f"{execution_cursor.file}:{execution_cursor.line} -> {parent_frame} ")
        frame = events.StackFrame.new(parent_frame, execution_cursor)
        self.stack.append(frame)

    def get_parent_frame(self):
        if len(self.stack) > 0:
            return self.stack[-1]
        return None

    def new_cursor_in_current_frame(self, new_cursor: events.ExecutionCursor):
        stack_frame: events.StackFrame = self.top_level_frame_as_clone()
        stack_frame.line = new_cursor.line
        stack_frame.file = new_cursor.file
        stack_frame.function_name = new_cursor.function_name
        # todo this is probably dirty hack?
        # or just replacing last-known stack frame
        if len(self.stack) > 0:
            self.stack[-1] = stack_frame
        else:
            # session just begin, not yet in any stack
            self.stack.append(stack_frame)


    def exit_frame(self):
        self.stack.pop()

    def top_level_frame_as_clone(self):
        current: events.StackFrame = self.current_frame()
        # print('top_level_frame_as_clone ->' + str(current))
        return events.StackFrame.clone(current)
        # ???
        # return current

    def current_frame(self):
        frame = self.get_parent_frame()
        return frame

class SimpleTracer:
    event_number: int
    file_filter: AbstractFileFilter
    event_buffer: List
    call_stack: CallStack
    session: TraceSession
    simulation: SimulatorSink
    
    def __init__(self, event_buffer, session_name, file_filter: AbstractFileFilter, clock: Clock, queue):
        self.event_number = 1
        self.clock = clock
        self.event_buffer = event_buffer
        self.file_filter = file_filter
        self.call_stack = CallStack()
        self.session = TraceSession(session_name)
        self.simulation = DisabledSimulatorSink()
        # self.simulation = SimulatorSink()

        self.queue = queue
        self.max_events_before_send = 5000

    def simple_tracer(self, frame: models.Frame, event: str, arg):
        # f_type = type(frame)
        # print(f_type.__module__ + '.' + f_type.__qualname__)
        co = frame.f_code
        # func_name = co.co_name
        file_path_under_cursor = co.co_filename
        # line_no = frame.f_lineno
        if not self.file_filter.should_trace(file_path_under_cursor):
            self.session.will_skip_file(file_path_under_cursor)
            # Ignore calls not in this module
            # self.session.did_enter_traceable_file(file_path_under_cursor)
            # todo this should return immediately ?
            #
            # return self.simple_tracer
        else:
            self.session.did_enter_traceable_file(file_path_under_cursor)

        self.process_events(event, frame, arg)
        self.simulation.save_for_simulator(frame, event, arg)

        # print(f"[{co.co_argcount}]{event}: {func_name} {line_no} -> {arg}")
        # print(f"   {frame.f_locals}")
        return self.simple_tracer

    def process_events(self, event: str, frame: models.Frame, arg):
        now = self.clock.now()
        will_record_current_event = False
        file_path_under_cursor = frame.f_code.co_filename
        cursor = events.ExecutionCursor(frame.f_code.co_filename, frame.f_lineno, frame.f_code.co_name)
        if not self.file_filter.should_trace(file_path_under_cursor):
            self.session.will_skip_file(file_path_under_cursor)
        else:
            will_record_current_event = True
            self.session.did_enter_traceable_file(file_path_under_cursor)

        if event == EventKeys.call:
            self.call_stack.enter_frame(cursor)
            if will_record_current_event:
                current = events.MethodEnterEvent(cursor, self.get_execution_stack(), now)
                variables = current.input_variables
                if self.file_filter.should_record_variables():
                    self.push_traceable_variables(frame, variables)
                self.event_buffer.append(current)

        if event == EventKeys.line:
            # self.call_stack.new_cursor_in_current_frame(cursor)
            if will_record_current_event:
                self.call_stack.new_cursor_in_current_frame(cursor)
                current = events.LineExecutionEvent(cursor, self.get_execution_stack(), now)
                if self.file_filter.should_record_variables():
                    self.push_traceable_variables(frame, current.locals)
                self.event_buffer.append(current)

        if event == EventKeys.event_return:
            self.call_stack.exit_frame()
            if will_record_current_event:
                current = events.MethodExitEvent(cursor, self.get_execution_stack(), now)
                current.return_variables.push_variable('__return', arg)
                if self.file_filter.should_record_variables():
                    self.push_traceable_variables(frame, current.locals)
                self.event_buffer.append(current)

        self.flush_queue_if_full()

    def get_execution_stack(self):
        return self.call_stack.current_frame()

    def push_traceable_variables(self, frame, variables):
        for (name, value) in frame.f_locals.items():
            # todo use variable values diffing
            variables.push_variable(name, value)

    def flush_outstanding_events(self):
        old_buffer = self.event_buffer
        self.event_buffer = []

        self.queue.put_events(EventsSlice(self.session.session_name, self.event_number, old_buffer))
        self.event_number += 1

    def flush_queue_if_full(self):
        if len(self.event_buffer) >= self.max_events_before_send:
            self.flush_outstanding_events()



