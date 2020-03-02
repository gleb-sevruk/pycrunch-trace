from typing import List, Optional


class LiveSession:
    sid: str
    session_name: str
    version: str

    def __init__(self, sid, version):
        self.sid = sid
        self.version = version


class ActiveConnections:
    tracers_online: List[LiveSession]
    clients: List[str]

    def __init__(self):
        self.tracers_online = []
        self.clients = []

    def client_did_connect(self, reference: str):
        self.clients.append(reference)

    def client_did_disconnect(self, reference: str):
        self.clients.remove(reference)
        self.remove_if_any_tracer(reference)

    def remove_if_any_tracer(self, reference: str) -> bool:
        possible_tracer = self.find_tracer_with_id(reference)
        if not possible_tracer:
            return False

        self.tracers_online.remove(possible_tracer)
        return True

    def find_tracer_with_id(self, reference) -> Optional[LiveSession]:
        for tracer in self.tracers_online:
            if tracer.sid == reference:
                return tracer

        return None

    def tracer_did_connect(self, sid, version):
        self.tracers_online.append(LiveSession(sid, version))
        pass

    def tracer_did_disconnect(self, sid):
        return self.remove_if_any_tracer(sid)

