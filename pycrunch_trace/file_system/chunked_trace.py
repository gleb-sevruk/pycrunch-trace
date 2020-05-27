import io
import struct
from pathlib import Path

from pycrunch_trace.proto import message_pb2


class ChunkedTrace:
    # size in bytes; this return 4 on my machine
    header_size = struct.calcsize("i")

    def __init__(self, filename: Path):
        self.filename = filename


    def events(self) -> list:
        file_map = dict()
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
                try:
                    interrim.ParseFromString(read_bytes)
                except Exception as eeeeeee:
                    print(eeeeeee)
                    raise

                for stack_frame in interrim.stack_frames:
                    entire_session.stack_frames.append(stack_frame)
                print(f'total stack_frames {len(entire_session.stack_frames)}')
                events_so_far += len(interrim.events)
                print(f'total events {events_so_far}')
                for event in interrim.events:
                    entire_session.events.append(event)

                for f in interrim.files:
                    file_map[f.file] = f.id

                if events_so_far > 10000000:
                    break
        for (file, file_id) in file_map.items():
            result_file = message_pb2.File()
            result_file.id = file_id
            result_file.file = file
            entire_session.files.append(result_file)

        return entire_session
