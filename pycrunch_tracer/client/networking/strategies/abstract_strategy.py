from pycrunch_tracer.client.networking.commands import EventsSlice


class AbstractRecordingStrategy:
    def prepare(self):
        pass

    def recording_start(self, session_id: str):
        pass

    def recording_stop(self, session_id: str):
        pass

    def recording_slice(self, x: EventsSlice):
        pass

    def clean(self):
        pass