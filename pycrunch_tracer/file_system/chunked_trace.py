import io
import struct
from pathlib import Path

from pycrunch_tracer.proto import message_pb2


class ChunkedTrace:
    header_size = struct.calcsize("i")

    def __init__(self, filename: Path):
        self.filename = filename


    def events(self) -> list:
        entire_session = message_pb2.TraceSession()
        events_so_far = 0
        with io.FileIO(self.filename, 'r') as file_to_read:
            while True:
                header_bytes = file_to_read.read(ChunkedTrace.header_size)
                if len(header_bytes) <= 0:
                    print(f' -- Read to end')

                    break
                next_chunk_length = struct.unpack('i', header_bytes)[0]
                print(f'next_chunk_length {next_chunk_length}')

                read_bytes = file_to_read.read(next_chunk_length)
                interrim = message_pb2.TraceSession()
                interrim.ParseFromString(read_bytes)

                print(f'total stack_frames {len(interrim.stack_frames)}')
                for stack_frame in interrim.stack_frames:
                    entire_session.stack_frames.append(stack_frame)
                events_so_far += len(interrim.events)
                print(f'total events {events_so_far}')
                for event in interrim.events:
                    entire_session.events.append(event)

        return entire_session
