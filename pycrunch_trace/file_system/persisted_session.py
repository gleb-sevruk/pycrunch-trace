import io
import json
import pickle
from datetime import datetime
from pathlib import Path
from typing import List

import jsonpickle

from pycrunch_trace.events.event_buffer_in_protobuf import EventBufferInProtobuf
from pycrunch_trace.file_system.chunked_trace import ChunkedTrace
from pycrunch_trace.file_system.human_readable_size import HumanReadableByteSize
from pycrunch_trace.proto import message_pb2
import logging

logger = logging.getLogger(__name__)


class TraceSessionMetadata:
    # time in UTC
    start_time: datetime
    end_time: datetime
    # size in bytes
    file_size_in_bytes: int
    file_size_on_disk: str
    files_in_session: List[str]

    events_in_session: int

    working_directory: str

    name: str


class LazyLoadedSession:
    metadata: TraceSessionMetadata
    trace_filename: Path
    metadata_file: Path
    raw_metadata: dict

    def __init__(self, buffer_file: Path, metadata_file: Path, chunked: bool):
        self.chunked = chunked
        self.trace_filename = buffer_file
        self.metadata_file = metadata_file
        self.raw_metadata = None

    def load_buffer(self):
        if not self.chunked:
            return self.load_unchunked()
        else:
            return ChunkedTrace(self.trace_filename).events()

    def load_unchunked(self):
        with io.FileIO(self.trace_filename, mode='r') as file:
            buffer = file.readall()
            # try:
            # result = json.loads(buffer)
            # except:

            # result = pickle.loads(buffer)

            result = message_pb2.TraceSession()
            result.ParseFromString(buffer)
            return result

    def load_metadata(self):
        with io.FileIO(self.metadata_file, 'r') as file:
            file_bytes = file.readall()
            json_representation = file_bytes.decode('utf-8')
            json_dict = json.loads(json_representation)
            self.raw_metadata = json_dict
            meta = TraceSessionMetadata()
            meta.files_in_session = json_dict.get('files_in_session')
            meta.excluded_files = json_dict.get('events_in_session')
            meta.events_in_session = json_dict.get('events_in_session')
            meta.file_size_in_bytes = json_dict.get('file_size_in_bytes')
            meta.file_size_on_disk = json_dict.get('file_size_on_disk')
            meta.name = json_dict.get('name')
            self.metadata = meta


class PersistedSession:
    def __init__(self, session_directory: Path):
        self.session_directory = session_directory

    metadata_filename = 'pycrunch-trace.meta.json'
    recording_filename = 'session.pycrunch-trace'
    chunked_recording_filename = 'session.chunked.pycrunch-trace'

    pass

    def save_with_metadata(self, event_buffer, files_in_session, excluded_files):
        file_to_save = self.session_directory.joinpath(self.recording_filename)
        bytes_written = -42
        with io.FileIO(file_to_save, mode='w') as file:
            try:
                result = self.serialize_to_bytes(event_buffer)
                bytes_written = file.write(result)
            except Exception as ex:
                logger.exception('failed to save session', exc_info=ex)

        meta = TraceSessionMetadata()
        meta.files_in_session = list(files_in_session)
        meta.excluded_files = list(excluded_files)
        meta.file_size_in_bytes = bytes_written
        meta.file_size_on_disk = str(HumanReadableByteSize(bytes_written))
        meta.events_in_session = len(event_buffer)
        meta.name = str(self.session_directory)
        print(f'tracing --- protobuf binary array results saved to file {file_to_save}')

        self.save_metadata(self.session_directory, meta)

    def serialize_to_bytes(self, event_buffer):
        return EventBufferInProtobuf(event_buffer, x.file_map).as_bytes()
        # todo add multiple serialization plugin/options
        # return pickle.dumps(event_buffer)

    def save_metadata(self, session_directory: Path, meta: TraceSessionMetadata):
        metadata_file_path = session_directory.joinpath(self.metadata_filename)

        with io.FileIO(metadata_file_path, mode='w') as file:
            result = self.serialize_to_json(meta)
            bytes_written = file.write(result.encode('utf-8'))

    def serialize_to_json(self, meta) -> str:
        return jsonpickle.dumps(meta, unpicklable=False)

    @classmethod
    def load_from_directory(cls, load_from_directory: Path) -> LazyLoadedSession:
        chunked = False
        joinpath = load_from_directory.joinpath(PersistedSession.recording_filename)
        if not joinpath.exists():
            joinpath = load_from_directory.joinpath(PersistedSession.chunked_recording_filename)
            chunked = True
        print(joinpath)
        return LazyLoadedSession(joinpath, load_from_directory.joinpath(PersistedSession.metadata_filename), chunked)
