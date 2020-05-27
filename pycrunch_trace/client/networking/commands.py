from typing import Dict, List


class AbstractNetworkCommand:
    command_name: str


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
    def __init__(self, session_id: str, files_included: List[str], files_excluded: List[str]):
        self.command_name = 'StopCommand'
        self.session_id = session_id
        self.files_included = files_included
        self.files_excluded = files_excluded

