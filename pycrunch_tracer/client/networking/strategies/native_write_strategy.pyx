from pycrunch_tracer.client.networking.commands import EventsSlice, FileContentSlice
from pycrunch_tracer.client.networking.strategies.abstract_strategy import AbstractRecordingStrategy

import pyximport

from pycrunch_tracer.events.file_contents_in_protobuf import FileContentsInProtobuf

pyximport.install()
from pycrunch_tracer.events.native_event_buffer_in_protobuf import NativeEventBufferInProtobuf

from pycrunch_tracer.server.incoming_traces import incoming_traces
from pycrunch_tracer.server.trace_persistance import TracePersistence


class NativeLocalRecordingStrategy(AbstractRecordingStrategy):
    def __init__(self):
        self.persistence = TracePersistence()
        pass

    def prepare(self):
        # nothing to prepare here
        pass

    def recording_start(self, session_id: str):
        incoming_traces.trace_will_start(session_id)
        self.persistence.initialize_file(session_id)

    def recording_stop(self, session_id: str):
        self.persistence.recording_complete(session_id)

    def recording_slice(self, x: EventsSlice):
        incoming_traces.did_receive_more_events(x.session_id, len(x.events))
        bytes_to_disk = NativeEventBufferInProtobuf(x.events, x.files).as_bytes()

        self.persistence.flush_chunk(x.session_id, bytes_to_disk)

    def files_slice(self, x: FileContentSlice):
        bytes_to_disk = FileContentsInProtobuf(x.files).as_bytes()

        self.persistence.update_file_header(x.session_id)
        self.persistence.flush_chunk(x.session_id, bytes_to_disk)



    def clean(self):
        #  nothing to clean
        pass