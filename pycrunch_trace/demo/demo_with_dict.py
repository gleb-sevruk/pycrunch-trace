from pycrunch_trace.client.api import trace
from pycrunch_trace.tracing.file_map import FileMap




@trace
def run():
    loc = dict()
    fff = FileMap()
    id__ = fff.file_id('test')
    loc['fff'] = fff
    loc['id__'] = id__
    loc['file'] = 'test'



run()