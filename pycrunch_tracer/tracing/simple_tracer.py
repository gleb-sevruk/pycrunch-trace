import collections
from typing import List

import pycrunch_tracer.tracing.simulation.models as models
import pycrunch_tracer.events.method_enter as events
from pycrunch_tracer.client.command_buffer import ArrayCommandBuffer
from pycrunch_tracer.client.networking.commands import EventsSlice
from pycrunch_tracer.file_system.trace_session import TraceSession
from pycrunch_tracer.filters import AbstractFileFilter
from pycrunch_tracer.oop import Clock
from pycrunch_tracer.tracing.file_map import FileMap
from pycrunch_tracer.tracing.inline_profiler import ProfilingScope
from pycrunch_tracer.tracing.perf import TracerPerf
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
        #  todo what about performance ?
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
    file_map: FileMap
    event_number: int
    file_filter: AbstractFileFilter
    event_buffer: ArrayCommandBuffer
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
        self.file_map = FileMap()
        self.perf = TracerPerf()

        self.queue = queue
        self.max_events_before_send = 20000
        self.skip = False

    def simple_tracer(self, frame: models.Frame, event: str, arg):
        with ProfilingScope('simple_tracer'):
            entered_at = self.clock.now()

            with ProfilingScope('process_events'):
                self.process_events(entered_at, event, frame, arg)
            # self.simulation.save_for_simulator(frame, event, arg)

            # print(f"[{co.co_argcount}]{event}: {func_name} {line_no} -> {arg}")
            # print(f"   {frame.f_locals}")

            with ProfilingScope('perf.did_execute_line'):
                end_at = self.clock.now()
                diff = end_at - entered_at
                self.perf.did_execute_line(diff)
            return self.simple_tracer


    def process_events(self, now: float, event: str, frame: models.Frame, arg):
        will_record_current_event = False
        file_path_under_cursor = frame.f_code.co_filename
        with ProfilingScope('process_events->should_trace'):
            if not self.file_filter.should_trace(file_path_under_cursor):
                self.session.will_skip_file(file_path_under_cursor)
            else:
                will_record_current_event = True
                self.session.did_enter_traceable_file(file_path_under_cursor)

        if event == EventKeys.line:
            with ProfilingScope('line'):
                if will_record_current_event:
                    cursor = self.create_cursor(file_path_under_cursor, frame)
                    with ProfilingScope('new_cursor_in_current_frame'):
                        self.call_stack.new_cursor_in_current_frame(cursor)

                    stack = self.get_execution_stack()
                    with ProfilingScope('create_LineExecutionEvent'):
                        current = events.LineExecutionEvent(cursor, stack, now)
                    if self.file_filter.should_record_variables():
                        self.push_traceable_variables(frame, current.locals)
                    self.add_to_event_buffer(current)

        if event == EventKeys.call:
            with ProfilingScope('call'):
                cursor = self.create_cursor(file_path_under_cursor, frame)
                with ProfilingScope('enter_frame'):
                    self.call_stack.enter_frame(cursor)
                # lets try to add methods
                # [if sampling mode]
                if will_record_current_event:
                    current = events.MethodEnterEvent(cursor, self.get_execution_stack(), now)
                    if self.file_filter.should_record_variables():
                        variables = current.input_variables
                        self.push_traceable_variables(frame, variables)
                    self.add_to_event_buffer(current)


        if event == EventKeys.event_return:
            with ProfilingScope('event_return'):
                with ProfilingScope('exit_frame'):
                    self.call_stack.exit_frame()
                # [? is sampling]
                if will_record_current_event:
                    cursor = self.create_cursor(file_path_under_cursor, frame)
                    current = events.MethodExitEvent(cursor, self.get_execution_stack(), now)
                    if self.file_filter.should_record_variables():
                        current.return_variables.push_variable('__return', arg)
                        self.push_traceable_variables(frame, current.locals)
                    self.add_to_event_buffer(current)

        self.flush_queue_if_full()

    def add_to_event_buffer(self, current):
        # todo: is this caused because of array dynamic size/doubling?
        # if True:
        #     return
        with ProfilingScope('add_to_event_buffer'):
            self.event_buffer.add_event(current)

    def create_cursor(self, file_path_under_cursor, frame):
        with ProfilingScope('create_cursor'):
            file_id = self.file_map.file_id(file_path_under_cursor)
            cursor = events.ExecutionCursor(file_id, frame.f_lineno, frame.f_code.co_name)
            return cursor

    def get_execution_stack(self):
        with ProfilingScope('get_execution_stack'):
            return self.call_stack.current_frame()

    def push_traceable_variables(self, frame, variables):
        with ProfilingScope('push_traceable_variables'):
            for (name, value) in frame.f_locals.items():
                # todo use variable values diffing
                variables.push_variable(name, value)

    def flush_outstanding_events(self):
        with ProfilingScope('flush_outstanding_events'):
            old_buffer = self.event_buffer.finish_chunk()
            self.perf.print_avg_time()

            self.queue.put_events(EventsSlice(self.session.session_name, self.event_number, old_buffer, self.file_map.files.copy()))
            self.event_number += 1

    def flush_queue_if_full(self):
        with ProfilingScope('flush_queue_if_full'):
            if self.event_buffer.how_many_events() >= self.max_events_before_send:
                self.flush_outstanding_events()



