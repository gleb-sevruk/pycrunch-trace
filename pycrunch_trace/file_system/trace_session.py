from datetime import datetime
from pathlib import Path
from typing import List, Set, Any

from pycrunch_trace.events.base_event import Event
from pycrunch_trace.file_system.session_store import SessionStore




class TraceSession:
    recording_directory : Path
    files_in_session: Set[str]
    excluded_files : Set[str]
    environment_during_run: dict
    event_buffer: List[Any]

    def __init__(self):
        self.files_in_session = set()
        self.excluded_files = set()
        self.environment_during_run = dict()
        self.session_store = SessionStore()

    def buffer_became_available(self, event_buffer):
        self.event_buffer = event_buffer

    def did_enter_traceable_file(self, filename: str):
        self.files_in_session.add(filename)

    def will_skip_file(self, filename: str):
        self.excluded_files.add(filename)

    def save(self):
        persistent_session = self.session_store.new_session(self.session_name)
        persistent_session.save_with_metadata(self.event_buffer, self.files_in_session, self.excluded_files)







