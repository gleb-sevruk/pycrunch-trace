import six

if six.PY3:
    from typing import Dict, List


class AbstractNetworkCommand:
    command_name = None  #type: str


class StartCommand(AbstractNetworkCommand):
    def __init__(self, session_id):
        # type: (str) -> ()
        self.session_id = session_id
        self.command_name = 'StartCommand'

class EventsSlice(AbstractNetworkCommand):
    files = None  #type: Dict[str, int]

    def __init__(self, session_id, chunk_number, events, files):
        # type: (str, int, list, Dict[str, int]) -> ()
        self.files = files
        self.chunk_number = chunk_number
        self.events = events
        self.command_name = 'EventsSlice'
        self.session_id = session_id

class FileContentSlice(AbstractNetworkCommand):
    files = None # type: Dict[str, int]

    def __init__(self, session_id, files):
        # type: (str, Dict[str, int]) -> ()
        self.command_name = 'FileContentSlice'
        self.files = files
        self.session_id = session_id


class StopCommand(AbstractNetworkCommand):
    def __init__(self, session_id, files_included, files_excluded):
        # type: (str, List[str], List[str]) -> ()
        self.command_name = 'StopCommand'
        self.session_id = session_id
        self.files_included = files_included
        self.files_excluded = files_excluded

