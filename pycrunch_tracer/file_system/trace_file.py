import io
import struct
from pathlib import Path

from . import tags


class TLV:
    length: int
    offset: int
    tag: int

    def __init__(self):
        self.length = None
        self.offset = None
        self.tag = None

    def data_offset(self):
        int_size = 4
        # TAG 4b | LEN 4b | <-----
        return self.offset + int_size * 2

class TraceFile:
    header: TLV
    file_section: TLV
    chunked_recording_filename = 'session.chunked.pycrunch-trace'

    def __init__(self, session_id: str, target_file: Path):
        self.target_file = target_file
        self.session_id = session_id
        # Header size may change in future
        self.header_size = 16 * 1024
        self.version_major = 0
        self.version_minor = 1

        self.header = None
        self.file_section = None


    def update_file_header_metadata_section(self, metadata_bytes_len):
        int_size = struct.calcsize(">i")
        uint64_size = struct.calcsize(">Q")

        bytes_written = self.target_file.stat().st_size

        with io.FileIO(self.target_file, 'r+') as file_to_write:
            header_metadata_begins_at = int_size * 2 + (uint64_size * 2)
            file_to_write.seek(self.header.data_offset())
            self.skip_to_free_header_chunk(file_to_write)

            # Q - unsigned = 8 bytes

            file_to_write.write(Int32(tags.HEADER_TAG_METADATA).bytes())
            file_to_write.write(Int32(uint64_size*2).bytes())

            file_to_write.write(Int64(bytes_written).bytes())
            file_to_write.write(Int64(metadata_bytes_len).bytes())

    def update_file_header_files_section(self, total_bytes):
        bytes_written = self.target_file.stat().st_size

        with io.FileIO(self.target_file, 'r+') as file_to_write:
            # Magic_Number | HEADER_SIZE | FILES_BEGINS | FILES_SIZE

            header_begins_at = self.header.data_offset()
            file_to_write.seek(header_begins_at)
            self.skip_to_free_header_chunk(file_to_write)

            # Q - unsigned = 8 bytes
            file_to_write.write(Int32(tags.HEADER_TAG_FILES).bytes())
            file_to_write.write(Int32(16).bytes())
            file_to_write.write(Int64(bytes_written).bytes())
            file_to_write.write(Int64(total_bytes).bytes())

    def skip_to_free_header_chunk(self, file_to_write):
        print('skip_to_free_header_chunk')
        print(f'pos = {file_to_write.tell()}')
        int_size = struct.calcsize(">i")
        has_data = True
        while has_data:
            buffer = file_to_write.read(int_size)
            tag = struct.unpack('>i', buffer)[0]
            if tag == 0:
                has_data = False
                # return cursor to free space
                file_to_write.seek(-int_size, io.SEEK_CUR)
                break
            buffer = file_to_write.read(int_size)
            next_payload_length = struct.unpack('>i', buffer)[0]
            # skip to next record
            file_to_write.seek(next_payload_length, io.SEEK_CUR)
        print(f'after pos = {file_to_write.tell()}')

    def write_header_placeholder(self):
        target_mode = 'w'
        with io.FileIO(self.target_file, target_mode) as file_to_write:
            self.write_signature(file_to_write)
            self.write_header(file_to_write)

    def write_signature(self, file_to_write):
        signature = Int32(15051991).bytes()
        file_to_write.write(signature)

    def write_header(self, file_to_write):
        self.header = TLV()
        self.header.offset = file_to_write.tell()

        # SIG | [ Tag | Len | Val ]

        self.header.length = self.header_size
        print(f'offse {self.header.offset}')
        print(f'l {self.header.length}')
        file_to_write.write(Int32(tags.TRACE_TAG_HEADER).bytes())
        file_to_write.write(Int32(self.header_size).bytes())

        file_to_write.write(Int32(tags.HEADER_TAG_VERSION).bytes())
        file_to_write.write(Int32(8).bytes())
        file_to_write.write(Int32(self.version_major).bytes())
        file_to_write.write(Int32(self.version_minor).bytes())

        ppp = file_to_write.seek(
            self.header.offset + 0 + 4 + 4 + self.header.length, io.SEEK_SET
        )
        print(f'hs={self.header_size}')
        print(f'ppp={ppp}')
        # this is to make sure file will have 16kb allocated at the beginning
        self.write_signature(file_to_write)

    def flush_chunk(self, tag_id: int, bytes_to_write):
        length_of_message = len(bytes_to_write)
        with io.FileIO(self.target_file, 'a') as file_to_write:
            # TLV triplet again
            file_to_write.write(Int32(tag_id).bytes())
            file_to_write.write(Int32(length_of_message).bytes())
            file_to_write.write(bytes_to_write)

class Int32:
    def __init__(self, value: int):
        self._value = value

    def bytes(self):
        return struct.pack(">i", self._value)

class Int64:
    def __init__(self, value: int):
        self._value = value

    def bytes(self):
        return struct.pack(">Q", self._value)
