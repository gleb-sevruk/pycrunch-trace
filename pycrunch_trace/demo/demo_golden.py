import requests

from pycrunch_trace.client.api import trace


def some_code(url):
    """

    :type url: str
    """
    for x in range(1):
        req = requests.get(url)
        code = req.status_code
        print(str(x))
        print(code)

@trace
def run_youtube_code(url):
    """

    :type url: str
    """
    some_code(url)


run_youtube_code('https://google.com')