import socketio

from . import version


class TracingClient:

    def __init__(self, host_url: str):
        self.sio = socketio.Client()
        connection_headers = dict(
            version=version.version,
            product='pycrunch-tracing-node',
        )
        self.sio.connect(url=host_url, headers=connection_headers, transports=['websocket'])

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

    def push_message(self, entire_tracing_sesssion):
        # dumps = pickle.dumps(entire_tracing_sesssion)
        # print(f'dumped {len(dumps)} bytes')
        try:
            print(f' ...sending bytes')

            self.sio.emit('event', dict(
                action='new_recording',
                # buffer=dumps,
            ))
            print(f' ...sent')
        except Exception as e:
            print('  -- !fail to send')
            print(str(e))

    def disconnect(self):

        self.sio.disconnect()
