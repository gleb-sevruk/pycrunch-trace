import socketio

from . import version
import logging

logger = logging.getLogger(__name__)


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
            logger.debug('CLIENT: I received a message!')

        @self.sio.on('my message')
        def on_message(data):
            logger.debug('CLIENT: I received a message!')

        @self.sio.event
        def connect():
            logger.info("CLIENT: I'm connected!")

        @self.sio.event
        def connect_error(data):
            logger.error(f"CLIENT: The connection failed! {data}")

        @self.sio.event
        def disconnect():
            logger.info("CLIENT: I'm disconnected!")

    def push_message(self, entire_tracing_sesssion):
        # dumps = pickle.dumps(entire_tracing_sesssion)
        # print(f'dumped {len(dumps)} bytes')
        try:
            logger.debug(f' ...sending bytes')

            self.sio.emit('event', dict(
                action='new_recording',
                # buffer=dumps,
            ))
            logger.debug(f' ...sent')
        except Exception as e:
            logger.error('  -- !fail to send', exc_info=True)

    def disconnect(self):

        self.sio.disconnect()
