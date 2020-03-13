class TracingServerEvent:
    event_name: str


class RecordingStartEvent(TracingServerEvent):
    session_id: str

    def __init__(self, session_id: str):
        self.session_id = session_id
        self.event_name = 'recording_start'


class RecordingCompleteEvent(TracingServerEvent):
    session_id: str

    def __init__(self, session_id: str):
        self.session_id = session_id
        self.event_name = 'recording_complete'


class PartialFileChunkEvent(TracingServerEvent):
    def __init__(self, event_number, session_id, bytes_to_write, events_in_payload):
        self.events_in_payload = events_in_payload
        self.bytes_to_write = bytes_to_write
        self.session_id = session_id
        self.event_number = event_number
        self.event_name = 'recording_chunk'
