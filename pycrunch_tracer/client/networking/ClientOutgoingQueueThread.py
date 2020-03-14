import threading
import uuid
from queue import Queue, Empty
from time import sleep

import socketio
from socketio import Client

from pycrunch_tracer.client.networking.client_trace_introspection import client_introspection
from pycrunch_tracer.client.networking.commands import EventsSlice, StopCommand, AbstractNetworkCommand, StartCommand

from pycrunch_tracer.events.event_buffer_in_protobuf import EventBufferInProtobuf

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
    is_thread_running: bool
    _counter: int
    sio : Client
    def __init__(self):


        print(f'PID: {os.getpid()} ClientQueueThread init')
        self.host = 'http://0.0.0.0:8080'
        self.sio = None
        self._counter = 0
        self.so_far = 0
        self.is_connected = False
        self.outgoingQueue = Queue()
        self.is_thread_running = False
        self.manual_reset_event = threading.Event()

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
        self.sio = socketio.Client()
        x = threading.Thread(target=self.thread_proc, args=(42,))
        # x.setDaemon(True)
        x.setDaemon(False)
        x.start()
        # todo lock?
        self.is_thread_running = True


    def thread_proc(self, obj):
        logging.info("Thread ClientQueueThread::thread_proc: starting")

        # self.sio = socketio.Client()
        transports = ['websocket']
        # transports = ['polling']
        print('socketio connect')
        self.sio.connect(url=self.host,transports=transports, headers=self.connection_headers() )
        # self.sio.connect(url=self.host, headers=self.connection_headers() )

        @self.sio.event
        def message(data):
            logger.info('CLIENT: I received a message!')

        @self.sio.on('my message')
        def on_message(data):
            print('on_message')
            logger.info('CLIENT: I received a message!')

        @self.sio.event
        def connect():
            print('connect')
            self.is_connected = True
            self.manual_reset_event.set()
            logger.info("CLIENT: I'm connected!")

        @self.sio.event
        def connect_error():
            print('connect_error')
            logger.info("CLIENT: The connection failed!")

        @self.sio.event
        def disconnect():
            print('disconnect')
            # put everything in garbage?
            self.is_connected = False
            logger.info("Clearing event... until connection established back")
            self.manual_reset_event.clear()

            logger.info("CLIENT: I'm disconnected!")

        def callback():
            print(f'#callback : delivered')

            logger.info(f'#callback : delivered')
            print(f'#callback : event set')
            self.manual_reset_event.set()

            # logger.info(args)

        def callback_for_disconnection():
            print('Disconnection Callback')
            # self.sio.disconnect()

        while True:
            logger.info('outgoingQueue.get: Waiting for message...')
            try:
                x : AbstractNetworkCommand = self.outgoingQueue.get(True, 3)
                print(f'queue length {len(self.outgoingQueue.queue)}')


                if x is not None:
                    print(f'got evt {x.command_name}')
                    if x.command_name == 'StartCommand':
                        self.sio.emit('tracing_node_event',
                                      dict(
                                          action='events_stream_will_start',
                                          session_id=x.session_id),
                                      )

                if x.command_name == 'StopCommand':
                    logger.info('got '+ x.command_name)
                    sleep(1)
                    self.sio.emit('tracing_node_event', dict(action='events_stream_did_complete', session_id=x.session_id), callback=callback_for_disconnection)

                logger.info('Sending... '+ x.command_name)
                if x.command_name == 'EventsSlice':
                    x : EventsSlice = x
                    # client_introspection.save_events(x.events)
                    # client_introspection.print_to_console(x.files)
                    events_in_payload = len(x.events)
                    bytes_to_send = EventBufferInProtobuf(x.events, x.files).as_bytes()
                    print(f'manual_reset_event.waiting...')
                    self.manual_reset_event.wait()
                    print(f' -- done waiting for manual_reset_event, sending chunk')
                    payload_size = len(bytes_to_send)
                    print(f' -- sending chunk {x.chunk_number} of {x.session_id} with size {payload_size}')
                    self.sio.emit('tracing_node_event',
                                  dict(
                                      action='events_stream',
                                      session_id=x.session_id,
                                      event_number=x.chunk_number,
                                      bytes=bytes_to_send,
                                      events_in_payload=events_in_payload,
                                      payload_size=payload_size),
                                  callback=callback)
                    sleep(0.1)
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
        self.is_thread_running = False
        self.sio.disconnect()

    def connection_headers(self):
        from pycrunch_tracer.client.api.version import version
        connection_headers = dict(
            version=version,
            product='pycrunch-tracing-node',
        )
        return connection_headers

    def ensure_thread_started(self):
        if not self.is_thread_running:
            self.start()


event_queue: ClientQueueThread = ClientQueueThread()
