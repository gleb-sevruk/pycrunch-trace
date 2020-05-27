import io
import os
import struct
from pathlib import Path
from tempfile import NamedTemporaryFile

from pycrunch_trace.client.api import trace
from pycrunch_trace.file_system.trace_file import TraceFile


def test_trace_file_header():
    f = NamedTemporaryFile(prefix='pytracer', delete=False)
    name = f.name
    f.close()
    print(name)
    try:
        sut = TraceFile('dummy', Path(f.name))

        x = sut.write_header_placeholder()
        sut.update_file_header_files_section(123)
        with io.FileIO(name, 'r') as actual:
            # SIGNATURE
            buffer = actual.read(struct.calcsize('>i'))
            sig = struct.unpack('>i', buffer)[0]
            assert sig == 15051991

            buffer = actual.read(struct.calcsize('>i'))
            tag = struct.unpack('>i', buffer)[0]
            assert tag == 1

            buffer = actual.read(struct.calcsize('>i'))
            header_size = struct.unpack('>i', buffer)[0]
            assert header_size == 16 * 1024


            new_pos = actual.seek(header_size + 8 + 4, io.SEEK_SET)
            print(new_pos)
            # SIGNATURE
            buffer = actual.read(struct.calcsize('>i'))
            sig = struct.unpack('>i', buffer)[0]
            assert sig == 15051991

    finally:
        os.remove(f.name)
        pass
    pass