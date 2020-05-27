from time import sleep

import requests

from pycrunch_trace.client.api.trace import Trace


def some_method():
    accum_counter = 1
    while accum_counter < 2:
        accum_counter += 1
        # try:
        r = requests.get('http://dev.iws.briteapps.space/')
        # r = requests.get('https://google.com/')
        # print(r.status_code)
        # print(r.content)
        x = accum_counter
        # except Exception as e:
        #     print("!!!!! FAIL", e)


yoba = Trace()
yoba.start('request_exce2',profile_name='default.profile.yaml')

some_method()

yoba.stop()
sleep(10)
# print(yoba.command_buffer)
# x = 1