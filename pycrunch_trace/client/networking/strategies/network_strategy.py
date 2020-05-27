import threading
from time import sleep

import socketio
from socketio import Client

import logging

from pycrunch_trace.client.networking.commands import EventsSlice
from pycrunch_trace.client.networking.strategies.abstract_strategy import AbstractRecordingStrategy
from pycrunch_trace.events.event_buffer_in_protobuf import EventBufferInProtobuf

logger = logging.getLogger(__name__)


class OverWireRecordingStrategy(AbstractRecordingStrategy):
    sio : Client

    def __init__(self):
        self.sio = socketio.Client()
        self.host = 'http://0.0.0.0:8080'
        self.sio = None
        self.manual_reset_event = threading.Event()

        pass
    def clean(self):
        self.sio.disconnect()

    def callback(self):
        print(f'#callback : delivered')

        logger.info(f'#callback : delivered')
        print(f'#callback : event set')
        self.manual_reset_event.set()

        # logger.info(args)

    def callback_for_disconnection(self):
        print('Disconnection Callback')
        # self.sio.disconnect()

    def recording_start(self, session_id: str):
        self.sio.emit('tracing_node_event',
                      dict(
                          action='events_stream_will_start',
                          session_id=session_id),
                      )
    def recording_stop(self, session_id: str):
        sleep(1)
        self.sio.emit('tracing_node_event', dict(action='events_stream_did_complete', session_id=session_id), callback=self.callback_for_disconnection)

    def recording_slice(self, x: EventsSlice):
        x: EventsSlice = x
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
                      callback=self.callback)
        sleep(0.01)

    def prepare(self):
        transports = ['websocket']
        # transports = ['polling']
        print('socketio connect')

        self.sio = socketio.Client()

        # self.sio.connect(url=self.host, headers=self.connection_headers() )
        self.sio.connect(url=self.host, transports=transports, headers=self.connection_headers())

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


    def connection_headers(self):
        from pycrunch_trace.client.api.version import version
        connection_headers = dict(
            version=version,
            product='pycrunch-tracing-node',
        )
        return connection_headers

