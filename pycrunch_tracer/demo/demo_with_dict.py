from pycrunch_tracer.client.api import yoba
from pycrunch_tracer.tracing.file_map import FileMap




@yoba
def run():
    loc = dict()
    fff = FileMap()
    id__ = fff.file_id('hui')
    loc['fff'] = fff
    loc['id__'] = id__
    loc['file'] = 'hui'



run()