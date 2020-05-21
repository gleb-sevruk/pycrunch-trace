
from datetime import datetime, timezone

def utc_now():
    return datetime.utcnow().replace(tzinfo=timezone.utc)

class TraceInProgress:
    session_id: str
    total_events: int
    started_at: datetime

    def __init__(self, session_id: str):
        self.session_id = session_id
        self.total_events = 0
        self.started_at = utc_now()

    def add_events(self, events_count):
        self.total_events += events_count
