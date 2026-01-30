import datetime
import sys
import uuid
from pathlib import Path
from typing import List

from pycrunch_trace.client.command_buffer import ArrayCommandBuffer
from pycrunch_trace.client.networking import event_queue
from pycrunch_trace.filters import CustomFileFilter
from pycrunch_trace.oop import File, Clock, SafeFilename
from pycrunch_trace.tracing.inline_profiler import inline_profiler_instance
from pycrunch_trace.config import config

import pyximport
pyximport.install()
from pycrunch_trace.native.native_tracer import NativeTracer

from pycrunch_trace.tracing.simple_tracer import SimpleTracer
import logging

logger = logging.getLogger(__name__)


class Trace:
    clock: Clock
    _tracer: SimpleTracer

    def __init__(self):
        self.default_host = 'http://0.0.0.0:8080'
        self.command_buffer = ArrayCommandBuffer()
        self.is_tracing = False
        self.session_name = None
        self._tracer = None
        # self._client: network_client.TracingClient = None
        self.clock = None
        self.host = None
        self.outgoingQueue = None

    def generate_session_name(self) -> str:
        iso_time = datetime.datetime.now().replace(microsecond=0).isoformat()
        return f'{iso_time}_{str(uuid.uuid4())[:5]}'

    def start(self, session_name: str = None, host: str = None, profile_name: str = None, additional_excludes: List[str] = None):

        if self.is_tracing:
            logger.error('Tracing has already been started for this session.')
            raise Exception('Tracing already started.')

        self.prepare_state(host, session_name)
        self.warn_if_another_tracing_set()

        if not profile_name:
            profile_name = 'default.profile.yaml'
        package_directory = Path(__file__).parent.parent.parent
        file_filter = CustomFileFilter(File(package_directory.joinpath('pycrunch-profiles', profile_name)))
        file_filter._ensure_loaded()

        if additional_excludes is not None:
            file_filter.add_additional_exclusions(additional_excludes)

        self.start_queue()

        self.clock = Clock()
        # todo maybe move command buffer to tracer?
        # self._tracer = SimpleTracer(self.command_buffer, self.session_name, f_filter, self.clock, self.outgoingQueue)
        # TODO windows test
        self._tracer = NativeTracer(self.session_name, self.outgoingQueue, file_filter)
        self.outgoingQueue.start()

        self.outgoingQueue.tracing_will_start(self.session_name)

        # also trace parent function
        sys._getframe().f_back.f_trace = self._tracer.simple_tracer

        sys.settrace(self._tracer.simple_tracer)

        self.is_tracing = True

    def start_queue(self):
        self.outgoingQueue = event_queue
        self.outgoingQueue.start()

    def warn_if_another_tracing_set(self):
        if sys.gettrace():
            logger.warning('Another trace function is already set. Tracing might result in errors.')

    def prepare_state(self, host, session_name):
        if not session_name:
            final_name = self.generate_session_name()
        else:
            final_name = session_name
            if config.keep_sessions:
                # Append 5 chars UUID to ensure uniqueness
                u = str(uuid.uuid4())[:5]
                final_name = f"{final_name}_{u}"
        
        safe_name = SafeFilename(final_name).__str__()
        
        if config.organize_by_date:
            # Create a structured date folder (e.g., 2026_01_29_22_47_04)
            date_prefix = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
            self.session_name = f"{date_prefix}/{safe_name}"
        else:
            self.session_name = safe_name
            
        if host:
            self.host = host
        else:
            self.host = self.default_host

    def stop(self):
        sys.settrace(None)

        inline_profiler_instance.print_timings()
        # import pydevd_pycharm
        # pydevd_pycharm.settrace('localhost', port=44441, stdoutToServer=True, stderrToServer=True)
        logger.info('Tracing complete. Saving results...')
        self.is_tracing = False
        # snapshot.save('a', self.command_buffer)
        local = False
        # local = True
        if local:
            self._tracer.session.buffer_became_available(self.command_buffer)
            self._tracer.session.save()

        self._tracer.flush_outstanding_events()
        self._tracer.finalize()
        
        # Ensure all events are flushed via the queue thread
        if self.outgoingQueue:
            logger.info("Waiting for the event queue to flush before exit...")
            self.outgoingQueue.join()

            # self._tracer.session.save()


        # self._client.push_message(self._tracer.session)
        # self._client.disconnect()
