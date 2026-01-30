import requests
import logging
from pycrunch_trace.client.api import trace

# Enable logging to see the tracer output
logging.basicConfig(
    level=logging.INFO,
    format='pycrunch-trace | %(asctime)s | %(levelname)-8s | %(message)s'
)


def some_code():
    for x in range(1):
        req = requests.get('https://google.com')
        code = req.status_code
        # print(str(x))
        # print(code)

@trace
def run_youtube_code():
    some_code()


run_youtube_code()