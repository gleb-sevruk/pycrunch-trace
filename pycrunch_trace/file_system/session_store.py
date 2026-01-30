from pathlib import Path
from typing import List

from pycrunch_trace.config import config
from pycrunch_trace.file_system.persisted_session import PersistedSession, LazyLoadedSession


class SessionStore:
    recording_directory: Path

    def __init__(self):
        self.recording_directory = config.recording_directory
        pass

    def all_sessions(self) -> List[str]:
        result = []
        self.ensure_recording_directory_created()
        
        # Look for directories that contains the metadata file
        # This supports both flat and date-organized structures
        for metadata_file in self.recording_directory.rglob(PersistedSession.metadata_filename):
            # The session name is the path relative to the recording directory
            session_path = metadata_file.parent.relative_to(self.recording_directory)
            result.append(str(session_path))
            
        return result

    def load_session(self, session_name: str) -> LazyLoadedSession:
        self.ensure_recording_directory_created()
        load_from = self.recording_directory.joinpath(session_name)
        session = PersistedSession.load_from_directory(load_from)
        return session

    def new_session(self, session_name) -> PersistedSession:
        self.ensure_recording_directory_created()
        session_directory = self.create_session_directory(session_name)
        return PersistedSession(session_directory)

    def create_session_directory(self, session_name):
        session_directory = self.recording_directory.joinpath(session_name)
        self.ensure_directory_created(session_directory)
        return session_directory

    def ensure_recording_directory_created(self):
        self.ensure_directory_created(self.recording_directory)

    def ensure_directory_created(self, directory: Path):
        if not directory.exists():
            directory.mkdir(parents=True, exist_ok=True)

