from typing import Union

from pycrunch_tracer.proto import message_pb2


class EventBufferInProtobuf:
    def __init__(self, event_buffer):
        self.event_buffer = event_buffer

    def as_bytes(self):
        session = message_pb2.TraceSession()
        aaaa = 0
        for e in self.event_buffer:
            # print('aaaa = ' + str(aaaa))
            aaaa +=1
            evt = self.pb_event_from_py(e)

            session.events.append(evt)

            frame = message_pb2.StackFrame()
            if e.stack:
                frame.id = e.stack.id


                if not e.stack.line:
                    frame.line = -1
                    frame.file = ''
                    print('suka')
                    print(e.stack)
                else:
                    frame.line = e.stack.line
                    frame.file = e.stack.file

                if e.stack and e.stack.parent:
                    frame.parent_id = e.stack.parent.id
                else:
                    frame.parent_id = -1
            else:
                frame.id = 0

            # print(aaaa)
            session.stack_frames.append(frame)

        return session.SerializeToString()

    def pb_event_from_py(self, e):
        evt = message_pb2.TraceEvent()
        evt.event_name = e.event_name
        if e.event_name == 'line' or e.event_name == 'method_exit':
            for key, value in e.locals.variables.items():
                pb_var = message_pb2.Variable()
                pb_var.name = key
                pb_var.value = str(value)
                evt.locals.variables.append(pb_var)

        if e.event_name == 'method_enter':
            for key, value in e.input_variables.variables.items():
                pb_var = message_pb2.Variable()
                pb_var.name = key
                pb_var.value = str(value)
                evt.input_variables.variables.append(pb_var)

        if e.event_name == 'method_exit':
            for key, value in e.return_variables.variables.items():
                pb_var = message_pb2.Variable()
                pb_var.name = key
                pb_var.value = str(value)
                evt.return_variables.variables.append(pb_var)

        evt.cursor.file = e.cursor.file
        evt.cursor.line = e.cursor.line
        # ptask.task.MergeFrom(task)
        if e.stack:
            evt.stack_id = e.stack.id
        return evt
