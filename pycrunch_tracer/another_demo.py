import sys
from pycrunch_tracer.samples import invalid_picker_with_exception
from pycrunch_tracer.session.snapshot import snapshot

from pycrunch_tracer.tracing.simple_tracer import SimpleTracer

#
event_buffer = []
tracer = SimpleTracer(event_buffer,,
sys.settrace(tracer.simple_tracer)

# module_b.some_method(3)
# module_b.another_m(5)
# module_b.string_m()
# module_c.find('x', 'axa')
# module_c.find('x', 'aaa')
invalid_picker_with_exception.op()

sys.settrace(None)

snapshot.save('a', event_buffer)
# x = pickle.dumps(event_buffer)
