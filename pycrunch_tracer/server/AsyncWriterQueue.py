import io
import shutil
import struct
import threading
from queue import Queue, Empty
from pathlib import Path

import jsonpickle

from pycrunch_tracer.file_system.human_readable_size import HumanReadableByteSize
from pycrunch_tracer.file_system.persisted_session import PersistedSession, TraceSessionMetadata
from pycrunch_tracer.file_system.session_store import SessionStore

import logging

from pycrunch_tracer.server import events, trace_in_progress
from pycrunch_tracer.server.chunks_ordering import chunks_ordering
from pycrunch_tracer.server.incoming_traces import incoming_traces
from pycrunch_tracer.server.perf import performance_insights
from pycrunch_tracer.server.trace_persistance import TracePersistence

logger = logging.getLogger(__name__)




class AsyncWriterQueue:
    def __init__(self):
        self.thread_lock = threading.Lock()
        self.thread = None
        self.queue = Queue()
        self.persistence = TracePersistence()

    def recording_will_start(self, session_id):
        self.queue.put_nowait(events.RecordingStartEvent(session_id))

    def add_chunk(self, event_number, session_id, byte_buffer, events_in_payload):
        self.queue.put_nowait(events.PartialFileChunkEvent(event_number, session_id, byte_buffer, events_in_payload))

    def recording_will_complete(self, session_id):
        self.queue.put_nowait(events.RecordingCompleteEvent(session_id))

    def thread_proc(self):
        while True:
            try:
                next_message: events.TracingServerEvent = self.queue.get()
                print(f'next_message = {next_message.event_name}')
                if next_message.event_name == 'recording_start':
                    self.recording_start(next_message)

                if next_message.event_name == 'recording_chunk':
                    self.flush_chunk_to_disk(next_message)
                if next_message.event_name == 'recording_complete':
                    self.recording_complete(next_message)
            except Empty as ex:
                # no messages
                pass
            except Exception as ex:
                print('Exception in thread_proc')
                print(ex)

    def recording_start(self, next_message: events.RecordingStartEvent):
        session_id = next_message.session_id

        self.persistence.initialize_file(session_id)

        chunks_ordering.session_will_start(session_id)
        incoming_traces.trace_will_start(session_id)

    def recording_complete(self, next_message):
        session_id = next_message.session_id
        self.print_avarage_size(session_id)
        chunks_ordering.session_will_finish(session_id)
        self.persistence.recording_complete(session_id)

    def print_avarage_size(self, session_id):
        avg_bytes_per_event = performance_insights.average_event_size(session_id)
        print(f'{session_id} avg size: {HumanReadableByteSize(avg_bytes_per_event).__str__()}')

    def flush_chunk_to_disk(self, next_message: events.PartialFileChunkEvent):

        session_id = next_message.session_id

        # this call might fail
        chunks_ordering.did_receive_chunk(session_id, next_message.event_number)

        bytes_to_write = next_message.bytes_to_write
        length_of_message = len(bytes_to_write)
        performance_insights.sample(session_id, next_message.events_in_payload, length_of_message)
        self.persistence.flush_chunk(session_id, bytes_to_write)

        self.print_avarage_size(session_id)


    def start_thread_if_not_running(self):
        with self.thread_lock:
            if self.thread is None:
                logger.info('Starting watch thread...')
                # logger.info('NOT')

                self.thread = threading.Thread(target=self.thread_proc)
                self.thread.start()
                # self.thread = True
                # loop = asyncio.get_event_loop()
                # loop.create_task(self.thread_proc())