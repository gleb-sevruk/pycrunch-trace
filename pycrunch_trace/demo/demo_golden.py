import requests

from pycrunch_trace.client.api import trace


def some_code():
    for x in range(1):
        req = requests.get('https://google.com')
        code = req.status_code
        print(str(x))
        print(code)

@trace
def run_youtube_code():
    some_code()


run_youtube_code()