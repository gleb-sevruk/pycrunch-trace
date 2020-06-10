from datetime import datetime

import six

if six.PY2:
    import pytz as pytz

if six.PY3:
    from datetime import timezone


def utc_now():
    if six.PY2:
        datetime.utcnow().replace(tzinfo=pytz.utc)
    else:
        # use standard lib when possible
        return datetime.utcnow().replace(tzinfo=timezone.utc)

class TraceInProgress:
    session_id = None #type: str
    total_events = None #type: int
    started_at = None #type: datetime

    def __init__(self, session_id):
        #type: (str) -> ()
        self.session_id = session_id
        self.total_events = 0
        self.started_at = utc_now()

    def add_events(self, events_count):
        self.total_events += events_count
