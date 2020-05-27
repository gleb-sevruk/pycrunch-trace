from typing import Dict, Any

import logging

from pycrunch_trace.server.trace_in_progress import TraceInProgress

logger = logging.getLogger(__name__)




class IncomingTraces:
    sessions_by_id: Dict[str, TraceInProgress]

    def __init__(self):
        self.sessions_by_id = dict()

    def trace_will_start(self, session_id):
        self.delete_possible_old_session(session_id)
        self._create_trace_in_progress(session_id)

    def _create_trace_in_progress(self, session_id):
        self.sessions_by_id[session_id] = TraceInProgress(session_id)

    def did_receive_more_events(self, session_id, events_count):
        current = self.get_session_with_id(session_id)
        current.add_events(events_count)

    def get_session_with_id(self, session_id) -> TraceInProgress:
        return self.sessions_by_id[session_id]

    def delete_possible_old_session(self, session_id):
        if session_id in self.sessions_by_id:
            self.log('Deleting stale/old session')
            del self.sessions_by_id[session_id]

    def log(self, msg):
        logger.info(msg)

incoming_traces: IncomingTraces = IncomingTraces()
