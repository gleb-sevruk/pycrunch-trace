import io
import os
import struct
from pathlib import Path

from pycrunch_trace.file_system.persisted_session import PersistedSession
from pycrunch_trace.file_system.session_store import SessionStore


def test_write():
    x = SessionStore()
    x.ensure_recording_directory_created()
    directory__joinpath = Path(x.recording_directory).joinpath('session_fake')
    x.ensure_directory_created(directory__joinpath)

    target_file = directory__joinpath.joinpath(PersistedSession.chunked_recording_filename)
    os.remove(target_file)

    write_once(target_file, 1)
    write_once(target_file, 2)
    write_once(target_file, 3)

def test_read():
    x = SessionStore()
    x.ensure_recording_directory_created()
    directory__joinpath = Path(x.recording_directory).joinpath('session_fake')
    x.ensure_directory_created(directory__joinpath)

    header_size = struct.calcsize("i")
    target_file = directory__joinpath.joinpath(PersistedSession.chunked_recording_filename)
    with io.FileIO(target_file, 'r') as file_to_read:
        while True:
            header_bytes = file_to_read.read(header_size)
            if len(header_bytes) <= 0:
                print(f' -- Read to end')

                break
            next_chunk_length = struct.unpack('i', header_bytes)[0]
            print(f'next_chunk_length {next_chunk_length}')
            read_bytes = file_to_read.read(next_chunk_length)
            result = read_bytes.decode('utf-8')
            print(f'result {result}')

    #
    # write_once(target_file, 1)
    # write_once(target_file, 2)
    # write_once(target_file, 3)


def write_once(target_file, index):
    target_mode = 'a'
    if not target_file.exists():
        target_mode = 'w'
    with io.FileIO(target_file, target_mode) as file_to_write:
        bytes_to_write = b'zalupa' + str(index).encode('utf-8')

        length_of_message = len(bytes_to_write)
        header_bytes = struct.pack("i", length_of_message)

        file_to_write.write(header_bytes + bytes_to_write)
