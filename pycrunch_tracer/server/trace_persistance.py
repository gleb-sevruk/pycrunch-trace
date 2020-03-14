import io
import shutil
import struct
from pathlib import Path

import jsonpickle

from pycrunch_tracer.file_system.human_readable_size import HumanReadableByteSize
from pycrunch_tracer.file_system.persisted_session import PersistedSession, TraceSessionMetadata
from pycrunch_tracer.file_system.session_store import SessionStore
from pycrunch_tracer.server.incoming_traces import incoming_traces


class TracePersistence:
    def __init__(self):
        x = SessionStore()
        x.ensure_recording_directory_created()
        self.rec_dir = x.recording_directory
        pass

    def initialize_file(self, session_id: str):
        dir_path = Path(self.rec_dir)
        session_id = session_id
        rec_dir = dir_path.joinpath(session_id)
        if rec_dir.exists():
            shutil.rmtree(rec_dir)

    def recording_complete(self, session_id):
        dir_path = Path(self.rec_dir)
        rec_dir = dir_path.joinpath(session_id)
        x = SessionStore()
        metadata_file_path = rec_dir.joinpath(PersistedSession.metadata_filename)
        target_chunk_file = rec_dir.joinpath(PersistedSession.chunked_recording_filename)
        meta = TraceSessionMetadata()
        meta.files_in_session = list()
        meta.excluded_files = list()
        bytes_written = target_chunk_file.stat().st_size
        meta.file_size_in_bytes = bytes_written
        meta.file_size_on_disk = str(HumanReadableByteSize(bytes_written))
        meta.events_in_session = incoming_traces.get_session_with_id(session_id).total_events
        meta.name = str(session_id)
        with io.FileIO(metadata_file_path, mode='w') as file:
            result = jsonpickle.dumps(meta, unpicklable=False)
            bytes_written = file.write(result.encode('utf-8'))
            print(f'metadata saved to {metadata_file_path}')

    def flush_chunk(self, session_id, bytes_to_write):
        target_file = self.get_chunked_trace_output_file(session_id)
        target_mode = self.get_write_mode_if_file_exist(target_file)
        length_of_message = len(bytes_to_write)
        with io.FileIO(target_file, target_mode) as file_to_write:
            header_bytes = struct.pack("i", length_of_message)
            file_to_write.write(header_bytes + bytes_to_write)

    def get_chunked_trace_output_file(self, session_id):
        dir_path = Path(self.rec_dir)
        rec_dir = dir_path.joinpath(session_id)
        x = SessionStore()
        x.ensure_directory_created(rec_dir)
        target_file = rec_dir.joinpath(PersistedSession.chunked_recording_filename)
        return target_file

    def get_write_mode_if_file_exist(self, target_file):
        target_mode = 'a'
        if not target_file.exists():
            target_mode = 'w'
        return target_mode
