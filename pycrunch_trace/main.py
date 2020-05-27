import asyncio
import io

# import aiohttp_debugtoolbar
import logging.config

from pathlib import Path

import yaml
from aiohttp import web
import socketio
from pycrunch.api.shared import sio
from pycrunch_trace.config import config

import cgitb
cgitb.enable(format='text')





package_directory = Path(__file__).parent
print(package_directory)
engine_directory = package_directory.parent
config.set_package_directory(package_directory)
config.set_engine_directory(engine_directory)
configuration_yaml_ = package_directory.joinpath('logging-configuration.yaml')
print(configuration_yaml_)
with open(configuration_yaml_, 'r') as f:
    logging.config.dictConfig(yaml.safe_load(f.read()))


import logging

logger = logging.getLogger(__name__)



import sys

if sys.platform == 'win32':
    policy = asyncio.get_event_loop_policy()
    policy._loop_factory = asyncio.ProactorEventLoop

async def shutdown(loop, signal=None):
    print('PTrace Server: shutdown')
    """Cleanup tasks tied to the service's shutdown."""
    if signal:
        logging.info(f"Received exit signal {signal.name}...")
    logging.info("Closing database connections")

def handle_exception(loop, context):
    # context["message"] will always be there; but context["exception"] may not
    print('PTrace Server: !!!PISOS')
    print('PTrace Server: handle_exception')
    msg = context.get("exception", context["message"])
    print('error was : ' + str(msg))

    logging.error(f"Caught exception: {msg}")
    logging.info("Shutting down...")
    # asyncio.create_task(shutdown(loop))

def run():
    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    loop.set_exception_handler(handle_exception)

    app = web.Application()
    # aiohttp_debugtoolbar.setup(app)


    #  keep import outside main
    from pycrunch_trace.server.shared import tracer_socket_server

    # attach sio events
    # noinspection PyUnresolvedReferences
    import pycrunch_trace.server.recording_server_websocket

    tracer_socket_server.attach(app)


    async def index(request):
        """Serve the client-side application."""
        with io.open(config.absolute_path, 'r') as f:
            lines = f.read()
            return web.Response(text=lines, content_type='application/json')


    # app.router.add_static('/static', 'static')
    app.router.add_get('/', index)
    web.run_app(app)

if __name__ == '__main__':
   run()