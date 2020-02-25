import asyncio
import io

import aiohttp_debugtoolbar
from aiohttp_debugtoolbar import toolbar_middleware_factory

from aiohttp import web
import socketio

import config
from tests.test_buffer import build_testing_events, to_string

sio = socketio.AsyncServer(cors_allowed_origins='*')
app = web.Application()
aiohttp_debugtoolbar.setup(app)

sio.attach(app)

async def index(request):
    """Serve the client-side application."""
    with io.open(config.absolute_path, 'r') as f:
        lines = f.read()
        return web.Response(text=lines, content_type='application/json')

@sio.event
def connect(sid, environ):
    print("connect ", sid)

@sio.event
async def event(sid, req):
    print(req)
    action = req.get('action')
    if action == 'load_buffer':
        print('reply ', action)
        await sio.emit('reply', to_string(build_testing_events()), room=sid)
    elif action == 'load_file':
        file_to_load = req.get('file_to_load')
        print(file_to_load)
        with io.open(config.absolute_path, 'r') as f:
            lines = f.read()
            await sio.emit('file_did_load', dict(filename=file_to_load, contents=lines), room=sid)
    else:
        await sio.emit('reply_unknown', room=sid)

@sio.event
def disconnect(sid):
    print('disconnec2t ', sid)

# app.router.add_static('/static', 'static')
app.router.add_get('/', index)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    web.run_app(app)