import threading
from queue import Queue, Empty

from pycrunch_trace.client.networking.commands import EventsSlice, StopCommand, AbstractNetworkCommand, StartCommand, FileContentSlice

import sys
import pyximport

from pycrunch_trace.client.networking.strategies.abstract_strategy import AbstractRecordingStrategy
from pycrunch_trace.file_system.trace_session import TraceSession

pyximport.install()
from pycrunch_trace.client.networking.strategies.native_write_strategy import NativeLocalRecordingStrategy


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
        print(f'PID: {os.getpid()} ClientQueueThread init')
        self._counter = 0
        self.so_far = 0
        self.is_connected = False
        self.outgoingQueue = Queue()
        self.is_thread_running = False
        current_strategy = 'native_local'
        if current_strategy == 'native_local':
            self._strategy = NativeLocalRecordingStrategy()

    def tracing_will_start(self, session_id: str):
        self.ensure_thread_started()
        try:
            self.outgoingQueue.put_nowait(StartCommand(session_id))
        except Exception as e:
            print('EXCEPTION')
            print(e)


    def put_events(self, events: EventsSlice):
        self.so_far +=  len(events.events)
        print(f'{events.session_id} - put_events: so far: {self.so_far}')
        self.ensure_thread_started()
        try:
            self.outgoingQueue.put_nowait(events)
        except Exception as e:
            print('EXCEPTION while put_events')
            print(e)

    def put_file_slice(self, events: FileContentSlice):
        print('put_file_slice')
        self.ensure_thread_started()
        try:
            self.outgoingQueue.put_nowait(events)
        except Exception as e:
            print('EXCEPTION while put_file_slice')
            print(e)

    def tracing_did_complete(self, session_id, session: TraceSession):
        print('tracing_did_complete')
        self.ensure_thread_started()
        self.outgoingQueue.put_nowait(
            StopCommand(
                session_id,
                list(session.files_in_session.copy()),
                list(session.excluded_files.copy()),
            )
        )

    def start(self):
        print(f'start thread dispather queue with pid: {os.getpid()}')
        if self.is_thread_running:
            return

        print('socketio init')
        x = threading.Thread(target=self.thread_proc, args=(42,))
        # x.setDaemon(True)
        x.setDaemon(False)
        x.start()
        # todo lock?
        self.is_thread_running = True


    def thread_proc(self, obj):
        logging.info("Thread ClientQueueThread::thread_proc: starting")

        self._strategy.prepare()


        while True:
            logger.info('outgoingQueue.get: Waiting for message...')
            try:
                x: AbstractNetworkCommand = self.outgoingQueue.get(True, 3)
                print(f'queue length {len(self.outgoingQueue.queue)}')

                if x is not None:
                    self.process_single_message(x)
            except Empty:
                print('Timeout while waiting for new msg... Thread will stop for now')
                break
                pass

            except Exception as ex:
                logger.info('Ex while getting message from queue')
                print('===!!! Ex while getting message from queue')
                print(str(ex))
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
                continue
        # end while
        print('Thread stopped')
        self._strategy.clean()
        self.is_thread_running = False

    def process_single_message(self, x: AbstractNetworkCommand):
        print(f'got evt {x.command_name}')
        if x.command_name == 'StartCommand':
            self._strategy.recording_start(x.session_id)
        if x.command_name == 'StopCommand':
            logger.info('got ' + x.command_name)
            self._strategy.recording_stop(x.session_id, x.files_included, x.files_excluded)
        if x.command_name == 'FileContentSlice':
            logger.info('got ' + x.command_name)
            self._strategy.files_slice(x)
        logger.info('Sending... ' + x.command_name)
        if x.command_name == 'EventsSlice':
            self._strategy.recording_slice(x)
            logger.info('Sent... ' + x.command_name)

    def ensure_thread_started(self):
        if not self.is_thread_running:
            self.start()


event_queue: ClientQueueThread = ClientQueueThread()
