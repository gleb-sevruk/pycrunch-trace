from io import FileIO
from typing import Union, Dict

from pycrunch_trace.events.base_event import Event

from pycrunch_trace.native.native_models cimport NativeCodeEvent, NativeVariable, NativeStackFrame

from pycrunch_trace.proto import message_pb2
from pycrunch_trace.tracing.file_map import FileMap

cdef class FileContentsInProtobuf:
    cdef object files

    def __init__(self, files: Dict[str, int]):
        self.files = files

    def as_bytes(self):
        session = message_pb2.FilesInSession()
        for (filename, file_id) in self.files.items():
            current_file_content = message_pb2.FileContent()
            current_file_content.id = file_id
            try:
                with FileIO(filename, 'r') as f:
                    current_file_content.content = f.readall()
            except Exception as e:
                print('error! at store_file_contents: ' + filename)
                print(e)
                current_file_content.content = b'error! at store_file_contents: ' + filename.encode('utf-8')
            session.files.append(current_file_content)

        return session.SerializeToString()
