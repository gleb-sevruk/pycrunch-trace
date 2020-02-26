import asyncio
import io

# import aiohttp_debugtoolbar

from aiohttp import web
import socketio

from pycrunch_tracer import config
from pycrunch_tracer.serialization import to_string
from pycrunch_tracer.session import active_clients
from pycrunch_tracer.session.snapshot import snapshot

import cgitb
cgitb.enable(format='text')

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
        print("connect ", sid)
        print("connect - environ", environ)
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


    async def notify_about_updated_buffer(req, sid):
        event_buffer = req.get('buffer')
        await sio.emit('reply', event_buffer)


    @sio.event
    async def event(sid, req):
        print(req)
        action: str = req.get('action')

        if action == 'load_buffer':
            await load_buffer_event(action, sid)
        elif action == 'load_file':
            await load_file_event(req, sid)
        elif action == 'updated_buffer':
            print('updated_buffer')
            await notify_about_updated_buffer(req, sid)
        else:
            await sio.emit('reply_unknown', room=sid)


    async def load_file_event(req, sid):
        file_to_load = req.get('file_to_load')
        print(file_to_load)
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
    def disconnect(sid):
        print('disconnec2t ', sid)

    # app.router.add_static('/static', 'static')
    app.router.add_get('/', index)
    web.run_app(app)

if __name__ == '__main__':
   run()