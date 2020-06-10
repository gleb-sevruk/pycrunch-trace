from pathlib import Path
import six
if six.PY3:
    from typing import List

from pycrunch_trace.config import config
from pycrunch_trace.file_system.persisted_session import PersistedSession, LazyLoadedSession


class SessionStore:
    recording_directory = None #type: Path

    def __init__(self):
        self.recording_directory = config.recording_directory
        pass

    def all_sessions(self):
        # type: () -> List[str]
        result = []
        self.ensure_recording_directory_created()
        for maybe_be_folder in self.recording_directory.glob('*'):
            if maybe_be_folder.is_dir():
                result.append(maybe_be_folder.name)
        return result

    def load_session(self, session_name):
        # type: (str) -> LazyLoadedSession
        self.ensure_recording_directory_created()
        load_from = self.recording_directory.joinpath(session_name)
        session = PersistedSession.load_from_directory(load_from)
        return session

    def new_session(self, session_name) :
        # type: (str) -> PersistedSession
        self.ensure_recording_directory_created()
        session_directory = self.create_session_directory(session_name)
        return PersistedSession(session_directory)

    def create_session_directory(self, session_name):
        session_directory = self.recording_directory.joinpath(session_name)
        self.ensure_directory_created(session_directory)
        return session_directory

    def ensure_recording_directory_created(self):
        self.ensure_directory_created(self.recording_directory)

    def ensure_directory_created(self, directory):
        # type: (Path) -> ()
        if not directory.exists():
            directory.mkdir()

