import socketio

from . import version
from ..serialization.shared import to_string


class TracingClient:

    def __init__(self, host_url: str):
        self.sio = socketio.Client()
        connection_headers = dict(
            version=version.version,
            product='pycrunch-tracing-node',
        )
        self.sio.connect(url=host_url, headers=connection_headers)

        @self.sio.event
        def message(data):
            print('CLIENT: I received a message!')

        @self.sio.on('my message')
        def on_message(data):
            print('CLIENT: I received a message!')

        @self.sio.event
        def connect():
            print("CLIENT: I'm connected!")

        @self.sio.event
        def connect_error():
            print("CLIENT: The connection failed!")

        @self.sio.event
        def disconnect():
            print("CLIENT: I'm disconnected!")

    def push_message(self, command_buffer):
        self.sio.emit('event', dict(
            action='updated_buffer',
            buffer=to_string(command_buffer),
        ))

    def disconnect(self):
        self.sio.disconnect()
