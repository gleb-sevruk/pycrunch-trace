from pycrunch_tracer.proto import message_pb2


class EventBufferInProtobuf:
    def __init__(self, event_buffer):
        self.event_buffer = event_buffer

    def as_bytes(self):
        session = message_pb2.TraceSession()
        aaaa = 0
        for e in self.event_buffer:
            aaaa +=1
            evt = message_pb2.TraceEvent()
            evt.event_name = e.event_name
            evt.cursor.file = e.cursor.file
            evt.cursor.line = e.cursor.line

            # ptask.task.MergeFrom(task)
            evt.stack_id = e.stack.as_id()

            evt = message_pb2.TraceEvent()

            session.events.append(evt)

            frame = message_pb2.StackFrame()
            frame.id = e.stack.id


            if not e.stack.line:
                frame.line = -1
                frame.file = ''
                print('suka')
                print(e.stack)
            else:
                frame.line = e.stack.line
                frame.file = e.stack.file
            if e.stack.parent:
                frame.parent_id = e.stack.parent.id
            else:
                frame.parent_id = -1
            print('e.stack.line - ' + str(e.stack.line))
            print('e.stack.line - ' + str(e.stack.file))
            print(aaaa)
            session.stack_frames.append(frame)

        return session.SerializeToString()
