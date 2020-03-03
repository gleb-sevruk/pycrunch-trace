import asyncio
import io

# import aiohttp_debugtoolbar
import logging.config

import pickle
from pathlib import Path

import yaml
from aiohttp import web
import socketio

from pycrunch_tracer import oop
from pycrunch_tracer.config import config
from pycrunch_tracer.events.serialized_proto import EventBufferInProtobuf
from pycrunch_tracer.file_system.session_store import SessionStore
from pycrunch_tracer.file_system.trace_session import TraceSession
from pycrunch_tracer.oop.file import File
from pycrunch_tracer.serialization import to_string
from pycrunch_tracer.session import active_clients
from pycrunch_tracer.session.snapshot import snapshot

import cgitb
cgitb.enable(format='text')


package_directory = Path(__file__).parent
print(package_directory)
engine_directory = package_directory.parent
config.set_engine_directory(engine_directory)
configuration_yaml_ = package_directory.joinpath('logging-configuration.yaml')
print(configuration_yaml_)
with open(configuration_yaml_, 'r') as f:
    logging.config.dictConfig(yaml.safe_load(f.read()))


import logging

logger = logging.getLogger(__name__)


def run():
    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    sio = socketio.AsyncServer(cors_allowed_origins='*')
    app = web.Application()
    # aiohttp_debugtoolbar.setup(app)

    sio.attach(app)
    connections = active_clients.ActiveConnections()
    async def index(request):
        """Serve the client-side application."""
        with io.open(config.absolute_path, 'r') as f:
            lines = f.read()
            return web.Response(text=lines, content_type='application/json')

    @sio.event
    async def connect(sid, environ):
        print("connect -", sid)
        # print("connect - environ", environ)
        product_name = environ.get('HTTP_PRODUCT')
        if product_name:
            if product_name == 'pycrunch-tracing-node':
                version = environ.get('HTTP_VERSION')
                connections.tracer_did_connect(sid, version)
                await sio.emit('front', dict(
                    event_name='new_tracker',
                    sid=sid,
                    version=version,
                ))


    async def new_recording(req, sid):
        logger.info('Started saving new recording')
        event_buffer_bytes = req.get('buffer')
        # todo this is double loading
        x: TraceSession = pickle.loads(event_buffer_bytes)
        x.save()
        logger.info('Recording saved successfully')
        await load_sessions(None)
        # await sio.emit('reply', event_buffer)


    @sio.event
    async def event(sid, req):
        # print(req)
        action: str = req.get('action')
        logger.info(f'WebSocket event: {action}')

        if action == 'load_buffer':
            await load_buffer_event(action, sid)
        elif action == 'load_file':
            await load_file_event(req, sid)
        elif action == 'load_sessions':
            await load_sessions(sid)
        elif action == 'load_single_session':
            await load_single_session(req, sid)
        elif action == 'new_recording':
            print('new_recording')
            await new_recording(req, sid)
        else:
            await sio.emit('reply_unknown', room=sid)

    async def load_sessions(sid):
        logging.debug('Loading sessions')
        store = SessionStore()
        all_names = store.all_sessions()
        result = []
        for name in all_names:
            lazy_loaded = store.load_session(name)
            lazy_loaded.load_metadata()
            metadata = lazy_loaded.raw_metadata
            metadata['short_name'] = name
            result.append(metadata)

        logging.debug(f'Sessions loaded, sending back to client {sid}')
        await sio.emit('session_list_loaded', result, room=sid)
        pass

    async def load_single_session(req, sid):
        logger.info('begin: load_single_session...')
        store = SessionStore()
        session_name = req.get('session_name')
        logging.info(f'Loading session {session_name}')
        ses = store.load_session(session_name)
        ses.load_buffer()
        recording_file = File(ses.buffer_file)
        logger.info('sending reply...')
        # await sio.emit('reply', to_string(buffer), room=sid)
        try:

            file_as_bytes = recording_file.as_bytes()
            logger.info('bytes loaded...')
            await sio.emit('reply', data=file_as_bytes, room=sid)
            logger.info('Event sent')

        except Exception as ex:
            logger.exception('Failed to load session ' + session_name, exc_info=ex)



    async def load_file_event(req, sid):
        file_to_load = req.get('file_to_load')
        logger.debug(f'file_to_load: `{file_to_load}`')
        with io.open(file_to_load, 'r', encoding='utf-8') as f:
            lines = f.read()
            await sio.emit('file_did_load', dict(filename=file_to_load, contents=lines), room=sid)


    async def load_buffer_event(action, sid):
        # return
        print('reply ', action)
        event_buffer = snapshot.load('a')
        # old = build_testing_events()
        await sio.emit('reply', to_string(event_buffer), room=sid)


    @sio.event
    async def disconnect(sid):
        logging.info(f'disconnect {sid}')
        if connections.tracer_did_disconnect(sid):
            logging.debug(f' -- sending notification about disconnected tracker {sid}')
            await sio.emit('front', dict(
                event_name='tracker_did_disconnect',
                sid=sid,
            ))

    # app.router.add_static('/static', 'static')
    app.router.add_get('/', index)
    web.run_app(app)

if __name__ == '__main__':
   run()