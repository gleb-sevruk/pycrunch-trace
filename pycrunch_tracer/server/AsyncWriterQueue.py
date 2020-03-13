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

logger = logging.getLogger(__name__)




class AsyncWriterQueue:
    def __init__(self):
        self.thread_lock = threading.Lock()
        self.thread = None

        x = SessionStore()
        x.ensure_recording_directory_created()
        self.rec_dir = x.recording_directory
        self.queue = Queue()

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
        dir_path = Path(self.rec_dir)
        session_id = next_message.session_id
        rec_dir = dir_path.joinpath(session_id)
        if rec_dir.exists():
            shutil.rmtree(rec_dir)
        chunks_ordering.session_will_start(session_id)

        incoming_traces.trace_will_start(session_id)

    def recording_complete(self, next_message):
        session_id = next_message.session_id
        self.print_avarage_size(session_id)
        chunks_ordering.session_will_finish(session_id)

        dir_path = Path(self.rec_dir)
        rec_dir = dir_path.joinpath(next_message.session_id)
        x = SessionStore()
        metadata_file_path = rec_dir.joinpath(PersistedSession.metadata_filename)
        target_chunk_file = rec_dir.joinpath(PersistedSession.chunked_recording_filename)
        meta = TraceSessionMetadata()
        meta.files_in_session = list()
        meta.excluded_files = list()
        bytes_written = target_chunk_file.stat().st_size
        meta.file_size_in_bytes = bytes_written
        meta.file_size_on_disk = str(HumanReadableByteSize(bytes_written))
        meta.events_in_session = incoming_traces.get_session_with_id(next_message.session_id).total_events
        meta.name = str(next_message.session_id)
        with io.FileIO(metadata_file_path, mode='w') as file:
            result = jsonpickle.dumps(meta, unpicklable=False)
            bytes_written = file.write(result.encode('utf-8'))
            print(f'metadata saved to {metadata_file_path}')

    def print_avarage_size(self, session_id):
        avg_bytes_per_event = performance_insights.average_event_size(session_id)
        print(f'{session_id} avg size: {HumanReadableByteSize(avg_bytes_per_event).__str__()}')

    def flush_chunk_to_disk(self, next_message: events.PartialFileChunkEvent):
        session_id = next_message.session_id

        # this call might fail
        chunks_ordering.did_receive_chunk(session_id, next_message.event_number)

        target_file = self.get_chunked_trace_output_file(next_message)
        target_mode = self.get_write_mode_if_file_exist(target_file)
        with io.FileIO(target_file, target_mode) as file_to_write:
            bytes_to_write = next_message.bytes_to_write
            length_of_message = len(bytes_to_write)
            header_bytes = struct.pack("i", length_of_message)
            performance_insights.sample(session_id, next_message.events_in_payload, length_of_message)
            file_to_write.write(header_bytes + bytes_to_write)

        self.print_avarage_size(session_id)

    def get_write_mode_if_file_exist(self, target_file):
        target_mode = 'a'
        if not target_file.exists():
            target_mode = 'w'
        return target_mode

    def get_chunked_trace_output_file(self, next_message):
        dir_path = Path(self.rec_dir)
        rec_dir = dir_path.joinpath(next_message.session_id)
        x = SessionStore()
        x.ensure_directory_created(rec_dir)
        target_file = rec_dir.joinpath(PersistedSession.chunked_recording_filename)
        return target_file

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