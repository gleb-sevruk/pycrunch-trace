from typing import Dict, Any

from pycrunch_trace.file_system.human_readable_size import HumanReadableByteSize


class SessionStats:
    total_bytes: int
    total_events: int
    session_id: str
    total_samples: int


    def __init__(self, session_id: str):
        self.session_id = session_id
        self.total_events = 0
        self.total_bytes = 0
        self.total_samples = 0

    def sample(self, events, buffer_size):
        size_per_event = buffer_size / events
        print(f'{self.session_id}:{self.total_samples} avg bytes: {HumanReadableByteSize(size_per_event)} ')
        self.total_events += events
        self.total_bytes += buffer_size
        self.total_samples += 1

    def average_event_size(self):
        if self.total_events == 0:
            return 0
        return self.total_bytes / self.total_events

    def __str__(self):
        return f'SessionStats({self.session_id}) average: {self.average_event_size()}; total: {self.total_events}; bytes:{self.total_bytes}'

class PerformanceInsights:

    sessions: Dict[str, SessionStats]

    def __init__(self):
        self.sessions = dict()
        pass

    def sample(self, session_id, number_of_events, buffer_size):
        stats = self.get_or_create_session(session_id)

        stats.sample(number_of_events, buffer_size)

    def get_or_create_session(self, session_id):
        if session_id not in self.sessions:
            stats = SessionStats(session_id)
            self.sessions[session_id] = stats
        else:
            stats = self.sessions[session_id]
        return stats

    def average_event_size(self, session_id):
        stats = self.get_or_create_session(session_id)
        return stats.average_event_size()


performance_insights = PerformanceInsights()
