import io

import yaml

from . import shared

from pycrunch_trace.events.event_buffer_in_protobuf import EventBufferInProtobuf
from pycrunch_trace.file_system.session_store import SessionStore
from pycrunch_trace.file_system.trace_session import TraceSession
from pycrunch_trace.filters import CustomFileFilter
from pycrunch_trace.oop import Directory, WriteableFile
from pycrunch_trace.oop.file import File
from pycrunch_trace.session import active_clients
from pycrunch_trace.session.snapshot import snapshot
import pickle


import logging

from .incoming_traces import incoming_traces
from .state import connections
from ..config import config
from ..file_system.human_readable_size import HumanReadableByteSize
from ..file_system.persisted_session import TraceSessionMetadata

logger = logging.getLogger(__name__)


@shared.tracer_socket_server.event
async def connect(sid, environ):
    print("connect -", sid)
    # print("connect - environ", environ)
    product_name = environ.get('HTTP_PRODUCT')
    if product_name:
        if product_name == 'pycrunch-tracing-node':
            version = environ.get('HTTP_VERSION')

            connections.tracer_did_connect(sid, version)
            await shared.tracer_socket_server.emit('front', dict(
                event_name='new_tracker',
                sid=sid,
                version=version,
            ))


async def new_recording(req, sid):
    logger.info('Started saving new recording')
    event_buffer_bytes = req.get('buffer')
    # todo this is double loading
    if (event_buffer_bytes):
        x: TraceSession = pickle.loads(event_buffer_bytes)
        x.save()

    logger.info('Recording saved successfully')
    await load_sessions(None)
    # await sio.emit('reply', event_buffer)

total_bytes = 0



@shared.tracer_socket_server.event
async def event(sid, req):
    # print(req)
    action: str = req.get('action')
    logger.info(f'WebSocket event: {action}')

    if action == 'load_buffer':
        pass
    elif action == 'load_file':
        await load_file_event(req, sid)
    elif action == 'load_profiles':
        await load_profiles_event(req, sid)
    elif action == 'load_sessions':
        await load_sessions(sid)
    elif action == 'load_profile_details':
        await load_profile_details(req, sid)
    elif action == 'load_single_session':
        await load_single_session(req, sid)
    elif action == 'save_profile_details':
        await save_profile_details(req, sid)
    elif action == 'new_recording':
        print('new_recording')
        await new_recording(req, sid)
    else:
        await shared.tracer_socket_server.emit('reply_unknown', room=sid)


async def load_sessions(sid):
    logging.debug('Loading sessions')
    store = SessionStore()
    all_names = store.all_sessions()
    result = []
    for name in all_names:
        try:
            lazy_loaded = store.load_session(name)
            lazy_loaded.load_metadata()
            metadata = lazy_loaded.raw_metadata
            metadata['short_name'] = name
        except:
            metadata = dict()
            metadata['short_name'] = name
            metadata['events_in_session'] = 'missing meta'

        result.append(metadata)

    logging.debug(f'Sessions loaded, sending back to client {sid}')
    await shared.tracer_socket_server.emit('session_list_loaded', result, room=sid)
    pass


async def load_single_session(req, sid):
    logger.info('begin: load_single_session...')
    store = SessionStore()
    session_name = req.get('session_name')
    logging.info(f'Loading session {session_name}')
    ses = store.load_session(session_name)

    # await sio.emit('reply', to_string(buffer), room=sid)
    try:

        logger.info('sending reply...')

        file_as_bytes = ses.load_buffer().SerializeToString()
        logger.info('bytes loaded...')
        #  todo maybe send back in chunks?
        await shared.tracer_socket_server.emit('reply', data=file_as_bytes
                                               , room=sid
                                               )
        logger.info('Event sent')

    except Exception as ex:
        logger.exception('Failed to load session ' + session_name, exc_info=ex)


async def save_profile_details(req, sid):
    logger.debug(f'save_profile_details: `{req}`')
    profile = req.get('profile')
    profile_name = profile.get('profile_name')
    xxx = yaml.dump(profile)
    logger.debug(xxx)
    profiles__joinpath = config.package_directory.joinpath('pycrunch-profiles').joinpath(profile_name)

    WriteableFile(profiles__joinpath, xxx.encode('utf-8')).save()


async def load_file_event(req, sid):
    file_to_load = req.get('file_to_load')
    logger.debug(f'file_to_load: `{file_to_load}`')
    with io.open(file_to_load, 'r', encoding='utf-8') as f:
        lines = f.read()
        await shared.tracer_socket_server.emit('file_did_load', dict(filename=file_to_load, contents=lines), room=sid)


async def load_profile_details(req, sid):
    d = Directory(config.package_directory.joinpath('pycrunch-profiles'))
    profile_name = req.get('profile_name')
    joinpath = config.package_directory.joinpath('pycrunch-profiles').joinpath(profile_name)
    print(joinpath)
    fff = CustomFileFilter(File(joinpath))

    raw = fff.all_exclusions()

    await shared.tracer_socket_server.emit('profile_details_loaded', dict(
        exclusions=raw,
        trace_variables=fff.should_record_variables(),
        profile_name=profile_name), room=sid)


async def load_profiles_event(req, sid):
    d = Directory(config.package_directory.joinpath('pycrunch-profiles'))
    res = d.files('yaml')
    print(res)
    raw = []
    for f in res:
        raw.append(f.short_name())
    await shared.tracer_socket_server.emit('profiles_loaded', dict(profiles=raw), room=sid)


@shared.tracer_socket_server.event
async def disconnect(sid):
    logging.info(f'disconnect {sid}')
    if connections.tracer_did_disconnect(sid):
        logging.debug(f' -- sending notification about disconnected tracker {sid}')
        await shared.tracer_socket_server.emit('front', dict(
            event_name='tracker_did_disconnect',
            sid=sid,
        ))
