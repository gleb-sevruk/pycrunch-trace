class TraceInProgress:
    session_id: str
    total_events: int

    def __init__(self, session_id: str):
        self.session_id = session_id
        self.total_events = 0

    def add_events(self, events_count):
        self.total_events += events_count
