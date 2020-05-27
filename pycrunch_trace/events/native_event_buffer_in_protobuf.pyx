from io import FileIO
from typing import Union, Dict

from pycrunch_trace.events.base_event import Event

from pycrunch_trace.native.native_models cimport NativeCodeEvent, NativeVariable, NativeStackFrame

from pycrunch_trace.proto import message_pb2
from pycrunch_trace.tracing.file_map import FileMap

cdef class NativeEventBufferInProtobuf:
    cdef object files
    cdef object event_buffer
    cdef object store_file_contents

    def __init__(self, event_buffer, files: Dict[str, int]):
        self.files = files
        self.event_buffer = event_buffer

    def as_bytes(self):
        cdef NativeCodeEvent e
        cdef object evt
        session = message_pb2.TraceSession()
        for e in self.event_buffer:
            evt = self.pb_event_from_py(e)

            session.events.append(evt)

            frame = message_pb2.StackFrame()
            if e.stack:

                frame.id = e.stack.id

                if not e.stack.cursor.line:
                    frame.line = -1
                    frame.file = ''
                    frame.function_name = '??'
                else:
                    frame.line = e.stack.cursor.line
                    frame.file = e.stack.cursor.file
                    frame.function_name = e.stack.cursor.function_name

                if e.stack and e.stack.parent:
                    frame.parent_id = e.stack.parent.id
                else:
                    frame.parent_id = -1
            else:
                frame.id = 0

            session.stack_frames.append(frame)

        self.add_files_to_pb_envelope(session)

        return session.SerializeToString()

    def add_files_to_pb_envelope(self, session):
        for (filename, file_id) in self.files.items():
            current_file = message_pb2.File()
            # print(f'file_id: {file_id}')
            # print(f'filename: {filename}')
            current_file.id = file_id
            current_file.file = filename
            session.files.append(current_file)


    cdef pb_event_from_py(self, NativeCodeEvent e):
        cdef NativeVariable v
        evt = message_pb2.TraceEvent()
        evt.event_name = e.event_name
        evt.ts = e.ts
        if e.event_name == 'line':
            if e.locals is not None:
                for v in e.locals.variables:
                    pb_var = message_pb2.Variable()
                    pb_var.name = v.name
                    pb_var.value = v.value
                    evt.locals.variables.append(pb_var)

        if e.event_name == 'method_enter':
            if e.input_variables is not None:
                for v in e.input_variables.variables:
                    pb_var = message_pb2.Variable()
                    pb_var.name = v.name
                    pb_var.value = v.value
                    evt.input_variables.variables.append(pb_var)

        if e.event_name == 'method_exit':
            if e.return_variables is not None:
                for v in e.return_variables.variables:
                    pb_var = message_pb2.Variable()
                    pb_var.name = v.name
                    pb_var.value = v.value
                    evt.return_variables.variables.append(pb_var)

        evt.cursor.file = e.cursor.file
        evt.cursor.line = e.cursor.line
        evt.cursor.function_name = e.cursor.function_name
        # ptask.task.MergeFrom(task)
        if e.stack:
            evt.stack_id = e.stack.id
        else:
            evt.stack_id = -1
        return evt
