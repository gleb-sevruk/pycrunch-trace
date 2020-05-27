import io
import shutil
import struct
from datetime import datetime
from pathlib import Path
from typing import Dict, List

import jsonpickle

from pycrunch_trace.file_system import tags
from pycrunch_trace.file_system.human_readable_size import HumanReadableByteSize
from pycrunch_trace.file_system.persisted_session import PersistedSession, TraceSessionMetadata
from pycrunch_trace.file_system.session_store import SessionStore
from pycrunch_trace.file_system.trace_file import TraceFile
from pycrunch_trace.server.chunks_ordering import PyCrunchTraceException
from pycrunch_trace.server.incoming_traces import incoming_traces


class TracePersistence:
    trace_files: Dict[str, TraceFile]

    def __init__(self):
        x = SessionStore()
        x.ensure_recording_directory_created()
        self.rec_dir = x.recording_directory
        self.trace_files = dict()
        pass

    def initialize_file(self, session_id: str):
        dir_path = Path(self.rec_dir)
        session_id = session_id
        rec_dir = dir_path.joinpath(session_id)
        if rec_dir.exists():
            shutil.rmtree(rec_dir)

        tf = TraceFile(session_id, self.get_chunked_trace_output_file(session_id))
        self.trace_files[session_id] = tf
        tf.write_header_placeholder()

    def recording_complete(self, session_id, files_included: List[str], files_excluded: List[str]):
        metadata_bytes, metadata_file_path = self.get_metadata_bytes(session_id, files_included, files_excluded)
        self.update_file_header_metadata_section(session_id, len(metadata_bytes))
        self.flush_chunk(session_id, tags.TRACE_TAG_METADATA, metadata_bytes)

        with io.FileIO(metadata_file_path, mode='w') as file:
            bytes_written = file.write(metadata_bytes)
            print(f'metadata saved to {metadata_file_path}')


    def get_metadata_bytes(self, session_id, files_included: List[str], files_excluded: List[str]):
        dir_path = Path(self.rec_dir)
        rec_dir = dir_path.joinpath(session_id)
        x = SessionStore()
        target_chunk_file = rec_dir.joinpath(PersistedSession.chunked_recording_filename)
        bytes_written = target_chunk_file.stat().st_size
        metadata_file_path = rec_dir.joinpath(PersistedSession.metadata_filename)
        meta = TraceSessionMetadata()
        meta.files_in_session = files_included
        meta.excluded_files = files_excluded
        meta.file_size_in_bytes = bytes_written
        meta.file_size_on_disk = str(HumanReadableByteSize(bytes_written))
        trace_in_progress = incoming_traces.get_session_with_id(session_id)
        meta.events_in_session = trace_in_progress.total_events
        meta.start_time = trace_in_progress.started_at
        meta.end_time = datetime.utcnow()
        meta.name = str(session_id)
        result = jsonpickle.dumps(meta, unpicklable=False)
        metadata_bytes = result.encode('utf-8')
        return metadata_bytes, metadata_file_path

    def flush_chunk(self, session_id, tag_id: int, bytes_to_write):
        trace_file = self._get_trace_file_or_throw(session_id)
        trace_file.flush_chunk(tag_id, bytes_to_write)

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

    def update_file_header_files_section(self, session_id, total_bytes):
        trace_file = self._get_trace_file_or_throw(session_id)
        trace_file.update_file_header_files_section(total_bytes)


    def _get_trace_file_or_throw(self, session_id) -> TraceFile:
        trace_file = self.trace_files.get(session_id)
        if not trace_file:
            raise PyCrunchTraceException(f'Cannot find trace file with session id {session_id}')
        return trace_file

    def update_file_header_metadata_section(self, session_id, metadata_bytes_len):
        trace_file = self._get_trace_file_or_throw(session_id)
        trace_file.update_file_header_metadata_section(metadata_bytes_len)

