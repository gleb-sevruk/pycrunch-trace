import threading
from queue import Queue, Empty

from pycrunch_trace.client.networking.commands import EventsSlice, StopCommand, AbstractNetworkCommand, StartCommand, FileContentSlice

import sys
import pyximport

from pycrunch_trace.client.networking.strategies.abstract_strategy import AbstractRecordingStrategy
from pycrunch_trace.file_system.trace_session import TraceSession

pyximport.install()
from pycrunch_trace.client.networking.strategies.native_write_strategy import NativeLocalRecordingStrategy
from pycrunch_trace.config import config


import logging


logger = logging.getLogger(__name__)

# root = logging.getLogger()
# root.setLevel(logging.DEBUG)
#
# handler = logging.StreamHandler(sys.stdout)
# handler.setLevel(logging.DEBUG)
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# handler.setFormatter(formatter)
# root.addHandler(handler)
# root.getChild('engineio.client').disabled = True
# root.getChild('socketio.client').disabled = True
# logger = logging.getLogger(__name__)


import os

class ClientQueueThread:
    available_recording_strategies = ['network', 'local']

    is_thread_running: bool
    _counter: int
    _strategy: AbstractRecordingStrategy

    def __init__(self):
        logger.debug(f'Initialized ClientQueueThread (PID: {os.getpid()})')
        self._counter = 0
        self.so_far = 0
        self.is_connected = False
        self.outgoingQueue = Queue()
        self.is_thread_running = False
        
        if config.s3_enabled:
            # Conditional import to avoid hard dependency on boto3
            try:
                from pycrunch_trace.client.networking.strategies.s3_strategy import S3RecordingStrategy
                self._strategy = S3RecordingStrategy()
                logger.info("Storage backend: S3 Recording Strategy enabled.")
            except ImportError:
                logger.error("Boto3 not found. Falling back to local recording strategy.")
                self._strategy = NativeLocalRecordingStrategy()
        else:
            self._strategy = NativeLocalRecordingStrategy()

    def tracing_will_start(self, session_id: str):
        self.ensure_thread_started()
        try:
            self.outgoingQueue.put_nowait(StartCommand(session_id))
        except Exception as e:
            logger.error('EXCEPTION in tracing_will_start', exc_info=True)


    def put_events(self, events: EventsSlice):
        self.so_far +=  len(events.events)
        logger.debug(f'{events.session_id} - put_events: so far: {self.so_far}')
        self.ensure_thread_started()
        try:
            self.outgoingQueue.put_nowait(events)
        except Exception as e:
            logger.error('EXCEPTION while put_events', exc_info=True)

    def put_file_slice(self, events: FileContentSlice):
        logger.debug('put_file_slice')
        self.ensure_thread_started()
        try:
            self.outgoingQueue.put_nowait(events)
        except Exception as e:
            logger.error('EXCEPTION while put_file_slice', exc_info=True)

    def tracing_did_complete(self, session_id, session: TraceSession):
        logger.debug('Tracing session completed.')
        self.ensure_thread_started()
        self.outgoingQueue.put_nowait(
            StopCommand(
                session_id,
                list(session.files_in_session.copy()),
                list(session.excluded_files.copy()),
            )
        )

    def start(self):
        if self.is_thread_running:
            return

        logger.info(f'Starting outgoing message dispatcher thread (PID: {os.getpid()}).')
        x = threading.Thread(target=self.thread_proc, args=(42,))
        x.daemon = True
        x.start()
        # todo lock?
        self.is_thread_running = True
        self._thread = x


    def thread_proc(self, obj):
        logger.debug("Message processing loop started.")

        self._strategy.prepare()


        while True:
            logger.debug('Dispatcher waiting for new message in queue...')
            try:
                x: AbstractNetworkCommand = self.outgoingQueue.get(True, 3)
                logger.debug(f'Queue length: {len(self.outgoingQueue.queue)}')

                if x is not None:
                    self.process_single_message(x)
            except Empty:
                logger.debug('Dispatcher timeout: no new messages. Ending loop.')
                break

            except Exception as ex:
                logger.error('Error while retrieving message from queue.', exc_info=True)
                continue
        # end while
        logger.info('Messenger thread stopped.')
        self._strategy.clean()
        self.is_thread_running = False

    def join(self):
        if self.is_thread_running and self._thread:
            # Put a sentinel to stop the thread if it's waiting
            # self.outgoingQueue.put(None)
            self._thread.join()

    def process_single_message(self, x: AbstractNetworkCommand):
        logger.debug(f'Processing command: {x.command_name}')
        if x.command_name == 'StartCommand':
            self._strategy.recording_start(x.session_id)
        if x.command_name == 'StopCommand':
            logger.debug(f'ACK: {x.command_name}')
            self._strategy.recording_stop(x.session_id, x.files_included, x.files_excluded)
        if x.command_name == 'FileContentSlice':
            logger.debug(f'ACK: {x.command_name}')
            self._strategy.files_slice(x)
        logger.debug(f'Sending {x.command_name}...')
        if x.command_name == 'EventsSlice':
            self._strategy.recording_slice(x)
            logger.debug(f'Successfully sent {x.command_name}.')

    def ensure_thread_started(self):
        if not self.is_thread_running:
            self.start()


event_queue: ClientQueueThread = ClientQueueThread()
