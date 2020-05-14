from typing import Dict

from pycrunch_tracer.tracing.file_map import FileMap


class AbstractNetworkCommand:
    command_name: str

zalupa = 0


class StartCommand(AbstractNetworkCommand):
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.command_name = 'StartCommand'

class EventsSlice(AbstractNetworkCommand):
    files: Dict[str, int]

    def __init__(self, session_id: str, chunk_number: int, events: list, files: Dict[str, int]):
        self.files = files
        self.chunk_number = chunk_number
        self.events = events
        self.command_name = 'EventsSlice'
        self.session_id = session_id

class FileContentSlice(AbstractNetworkCommand):
    files: Dict[str, int]

    def __init__(self, session_id: str, files: Dict[str, int]):
        self.command_name = 'FileContentSlice'
        self.files = files
        self.session_id = session_id


class StopCommand(AbstractNetworkCommand):
    def __init__(self, session_id: str):
        self.command_name = 'StopCommand'
        self.session_id = session_id

