import threading
from queue import Queue, Empty

from pycrunch_tracer.client.networking.commands import EventsSlice, StopCommand, AbstractNetworkCommand, StartCommand
from pycrunch_tracer.client.networking.strategies.local_write_strategy import LocalRecordingStrategy
from pycrunch_tracer.client.networking.strategies.network_strategy import AbstractRecordingStrategy, OverWireRecordingStrategy

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
        current_strategy = 'local'
        if current_strategy == 'network':
            self._strategy = OverWireRecordingStrategy()
        if current_strategy == 'local':
            self._strategy = LocalRecordingStrategy()

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
            print('EXCEPTION')
            print(e)
            print('zalupa=' + str(events.zalupa))


    def tracing_did_complete(self, session_id):
        self.outgoingQueue.put_nowait(StopCommand(session_id))

    def start(self):
        print(f'{os.getpid()} start')
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
                    print(f'got evt {x.command_name}')
                    if x.command_name == 'StartCommand':
                        self._strategy.recording_start(x.session_id)

                    if x.command_name == 'StopCommand':
                        logger.info('got '+ x.command_name)
                        self._strategy.recording_stop(x.session_id)


                    logger.info('Sending... '+ x.command_name)
                    if x.command_name == 'EventsSlice':
                        self._strategy.recording_slice(x, )
                        logger.info('Sent... '+ x.command_name)
            except Empty:
                print('Timeout while waiting for new msg... Thread will stop for now')
                break
                pass

            except Exception as ex:
                logger.info('Ex while getting message from queue')
                print('===!!! Ex while getting message from queue')
                print(str(ex))
                continue
        # end while
        print('Thread stopped')
        self._strategy.clean()
        self.is_thread_running = False


    def ensure_thread_started(self):
        if not self.is_thread_running:
            self.start()


event_queue: ClientQueueThread = ClientQueueThread()
