import requests

from pycrunch_tracer.api.tracing import Yoba


def some_method():
    accum_counter = 1
    while accum_counter < 2:
        accum_counter += 1
        # try:
        r = requests.get('http://dev.iws.briteapps.space/')
        # print(r.status_code)
        # print(r.content)
        x = accum_counter
        # except Exception as e:
        #     print("!!!!! FAIL", e)


yoba = Yoba()
yoba.start('request_exce2',profile_name='default.profile.yaml')

some_method()

yoba.stop()

# print(yoba.command_buffer)
# x = 1