import sys
import uuid
from time import sleep

from pycrunch_tracer.api import network_client
from pycrunch_tracer.file_system.session_store import SessionStore
from pycrunch_tracer.session.snapshot import snapshot
from pycrunch_tracer.tracing.simple_tracer import SimpleTracer


class Yoba:
    _tracer: SimpleTracer

    def __init__(self):
        self.default_host = 'http://0.0.0.0:8080'
        self.command_buffer = []
        self.is_tracing = False
        self.session_name = None
        self._tracer = None
        self._client: network_client.TracingClient = None
        self.host = None

    def generate_session_name(self) -> str:
        return str(uuid.uuid4())

    def start(self, session_name: str = None, host: str = None):
        if self.is_tracing:
            raise Exception('PyCrunch tracer ERROR: tracing already started')

        self.prepare_state(host, session_name)
        self.warn_if_another_tracing_set()

        self._client = network_client.TracingClient(self.host)

        self._tracer = SimpleTracer(self.command_buffer, self.session_name)
        sys.settrace(self._tracer.simple_tracer)

        self.is_tracing = True

    def warn_if_another_tracing_set(self):
        if sys.gettrace():
            # there is already trace
            print('PyCrunch tracer WARNING:')
            print('  -- there is already trace function set. ')
            print('  -- continuing will result in errors ')

    def prepare_state(self, host, session_name):
        if not session_name:
            self.session_name = self.generate_session_name()
        else:
            self.session_name = session_name
        if host:
            self.host = host
        else:
            self.host = self.default_host

    def stop(self):
        sys.settrace(None)

        # import pydevd_pycharm
        # pydevd_pycharm.settrace('localhost', port=44441, stdoutToServer=True, stderrToServer=True)
        print('tracing complete, sending results')
        self.is_tracing = False
        self._tracer.session.buffer_became_available(self.command_buffer)
        # snapshot.save('a', self.command_buffer)

        self._client.push_message(self._tracer.session)
        print('tracing --- sent results to backend')
        sleep(10)
        self._client.disconnect()
