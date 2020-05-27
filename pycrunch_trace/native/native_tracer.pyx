import time
import collections

from pycrunch_trace.client.networking.commands import EventsSlice, FileContentSlice, StopCommand
from pycrunch_trace.file_system.trace_session import TraceSession
from pycrunch_trace.tracing.file_map import FileMap
from pycrunch_trace.native.native_models cimport NativeCodeEvent, NativeExecutionCursor, NativeVariables, NativeVariable, NativeStackFrame

allowed_types = [int, str, float, dict, type(None), bool]
# allowed_types = [int, str, float,  type(None), bool]


cdef class NativeCallStack:
    cdef object stack
    cdef int last_id
    def __init__(self):
        self.stack = collections.deque()
        self.last_id = 0

    cdef NativeStackFrame enter_frame(self, NativeExecutionCursor execution_cursor):
        cdef NativeStackFrame new_candidate
        parent_frame = self.current_frame()
        # print(f"{execution_cursor.file}:{execution_cursor.line} -> {parent_frame} ")
        new_candidate = NativeStackFrame()
        new_candidate.cursor = execution_cursor
        new_candidate.parent = parent_frame
        new_candidate.id = self.next_id()

        self.stack.append(new_candidate)
        return new_candidate

    cdef int next_id(self):
        self.last_id += 1
        return self.last_id

    cdef NativeStackFrame new_cursor_in_current_frame(self, NativeExecutionCursor new_cursor):
        cdef NativeStackFrame cloned
        cdef NativeStackFrame parent
        parent = self.current_frame()

        cloned = NativeStackFrame()
        cloned.cursor = new_cursor
        if parent is not None:
            cloned.parent = parent.parent
        else:
            cloned.parent = parent

        cloned.id = self.next_id()

        if len(self.stack) > 0:
            self.stack.pop()
            self.stack.append(cloned)
            # self.stack[-1] = stack_frame
        else:
            # session just begin, not yet in any stack
            self.stack.append(cloned)
        return cloned

    cdef exit_frame(self):
        self.stack.pop()

    cdef NativeStackFrame top_level_frame_as_clone(self):
        cdef NativeStackFrame current
        cdef NativeStackFrame new_result
        current = self.current_frame()
        if current:
            new_result = NativeStackFrame()
            new_result.id = self.next_id()
            new_result.parent = current.parent
            new_result.cursor = current.cursor
            return new_result
        else:
            return None
        # ???
        # return current

    cdef NativeStackFrame current_frame(self):
        if len(self.stack) > 0:
            return self.stack[-1]
        return None

cdef class NativeBuffer:
    cdef list _buffer
    def __init__(self):
        self._buffer = []

    cdef void append(self, NativeCodeEvent evt):
        self._buffer.append(evt)

    cdef int count(self):
        return self._buffer.__len__()

    cdef finish_chunk(self):
        clone = self._buffer
        self._buffer = []
        return clone

cdef class NativeTracerPerf:
    cdef int total_samples
    cdef double total_time

    def __init__(self):
        self.total_samples = 1
        self.total_time = 0.00
        pass

    cdef void did_execute_line(self, double ts_diff):
        self.total_samples += 1
        self.total_time += ts_diff

    def print_avg_time(self):
        each = 1
        should_print = self.total_samples % each == 0
        should_print = True
        if should_print:
            time_per_sample = self.total_time / self.total_samples
            print(f'total_samples - {self.total_samples}')
            print(f'total overhead time - {round(self.total_time)} ms')
            print(f'                      {self.total_time}')
            print(f'{time_per_sample:.5f} ms avg call time overhead')

cdef class NativeClock:
    cdef double started_at

    def __init__(self):
        self.started_at = self._system_clock()
        pass

    cdef double now(self):
        cdef double now_without_offset
        now_without_offset = self._system_clock()
        return (now_without_offset - self.started_at) * 1000

    cdef double _system_clock(self):
        return time.perf_counter()
    pass

cdef class NativeTracer:
    cdef int event_number
    cdef int events_so_far
    cdef bint should_trace_variables
    cdef str session_name
    cdef NativeClock clock
    cdef NativeTracerPerf perf
    cdef NativeBuffer event_buffer
    cdef int max_events_before_send
    cdef object file_map
    cdef object file_filter
    cdef object queue
    cdef object session
    cdef NativeCallStack call_stack

    # cpdef ClientQueueThread queue

    def __init__(self, session_name, queue, file_filter):
        self.events_so_far = 0
        self.clock = NativeClock()
        self.perf = NativeTracerPerf()
        self.event_buffer = NativeBuffer()
        self.session_name = session_name
        self.max_events_before_send = 500
        self.file_map = FileMap()
        self.file_filter = file_filter
        self.should_trace_variables = file_filter.should_record_variables()
        self.session = TraceSession()

        self.queue = queue
        self.call_stack = NativeCallStack()

    def simple_tracer(self, frame, str event, arg):
        self.internal_c_call(frame, event, arg)
        return self.simple_tracer

    cdef internal_c_call(self, frame, str evt, arg):
        cdef str func_name
        cdef double entered_at
        cdef double end_at
        cdef double diff
        entered_at = self.clock.now()
        self.wip(entered_at, frame, evt, arg)
        self.events_so_far += 1
        # self.process_events(entered_at, event, frame, arg)
        # self.simulation.save_for_simulator(frame, event, arg)
        # print(f"[{co.co_argcount}]{event}: {func_name} {line_no} -> {arg}")
        # print(f"   {frame.f_locals}")
        end_at = self.clock.now()
        diff = end_at - entered_at
        self.perf.did_execute_line(diff)

    cdef wip(self, double entered_at, frame, str event, arg):
        # cdef boolean will_record_current_event
        cdef NativeCodeEvent current
        cdef NativeVariables input_variables
        cdef NativeVariables return_variables
        cdef NativeVariables locals_v
        cdef NativeExecutionCursor current_cursor
        cdef NativeVariable return_var
        cdef NativeStackFrame stack
        cdef int line_no
        cdef bint will_record_current_event
        cdef str function_name
        file_path_under_cursor = frame.f_code.co_filename

        if not self.file_filter.should_trace(file_path_under_cursor):
            will_record_current_event = False
            self.session.will_skip_file(file_path_under_cursor)
        else:
            will_record_current_event = True
            self.events_so_far += 1
            self.session.did_enter_traceable_file(file_path_under_cursor)

        line_no = frame.f_lineno
        function_name = frame.f_code.co_name
        current = NativeCodeEvent()

        if event == 'call' or event == 'line' or event == 'return':
            file_id = self.file_map.file_id(file_path_under_cursor)
            current_cursor = NativeExecutionCursor()
            current_cursor.file = file_id
            current_cursor.line = line_no
            current_cursor.function_name = function_name

            if event == 'line':
                current.event_name = 'line'
                stack = self.call_stack.new_cursor_in_current_frame(current_cursor)

            if event == 'call':
                current.event_name = 'method_enter'
                stack = self.call_stack.enter_frame(current_cursor)
            if event == 'return':
                current.event_name = 'method_exit'
                self.call_stack.exit_frame()
                stack = self.call_stack.current_frame()
            if not will_record_current_event:
                # do not go any further
                return

            current.cursor = current_cursor
            current.stack = stack
            current.ts = entered_at
            if self.should_trace_variables:
                if event == 'line':
                    locals_v = NativeVariables()
                    locals_v.variables = []
                    self.push_traceable_variables(frame, locals_v)
                    current.locals = locals_v

                if event == 'call':
                    input_variables = NativeVariables()
                    input_variables.variables = []
                    self.push_traceable_variables(frame, input_variables)
                    current.input_variables = input_variables
                if event == 'return':
                    return_variables = NativeVariables()
                    return_variables.variables = []
                    return_var = NativeVariable()
                    return_var.name = '__return'
                    return_var.value = self.ensure_safe_for_serialization(arg)
                    return_variables.variables.append(return_var)
                    current.return_variables = return_variables

            self.add_to_event_buffer(current)

        self.flush_queue_if_full()

    cdef str ensure_safe_for_serialization(self, value):
        current_type = type(value)
        if current_type not in allowed_types:
            return str(current_type)
        # return 'a'
        # todo is this slowdown?
        return str(value)

    cdef push_traceable_variables(self, frame, NativeVariables locals):
        cdef NativeVariable current
        for (name, value) in frame.f_locals.items():
            current = NativeVariable()
            current.name = name
            current.value = self.ensure_safe_for_serialization(value)
            locals.variables.append(current)

    def add_to_event_buffer(self, current):
        # todo: is this caused because of array dynamic size/doubling?
        # if True:
        #     return
        self.event_buffer.append(current)

    # def create_cursor(self, file_path_under_cursor, frame):
    #     file_id = self.file_map.file_id(file_path_under_cursor)
    #     cursor = events.ExecutionCursor(file_id, frame.f_lineno, frame.f_code.co_name)
    #     return cursor

    # def get_execution_stack(self):
    #     return self.call_stack.current_frame()
    #
    # def push_traceable_variables(self, frame, variables):
    #     for (name, value) in frame.f_locals.items():
    #         # todo use variable values diffing
    #         variables.push_variable(name, value)

    def flush_outstanding_events(self):
        self.perf.print_avg_time()
        print(f'total events C: {self.event_buffer.count()}')

        old_buffer = self.event_buffer.finish_chunk()
        # self.perf.print_avg_time()
        #
        self.queue.put_events(EventsSlice(self.session_name, self.event_number, old_buffer, self.file_map.files.copy()))

    def finalize(self):
        print('finalizing native tracer')
        self.queue.put_file_slice(FileContentSlice(self.session_name, self.file_map.files.copy()))

        self.queue.tracing_did_complete(
            self.session_name,
            self.session,
        )

    cdef flush_queue_if_full(self):
        if self.event_buffer.count() >= self.max_events_before_send:
            self.flush_outstanding_events()
