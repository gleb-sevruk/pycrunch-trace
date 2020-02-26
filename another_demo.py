import pickle
import sys
from samples import module_a, module_c, invalid_picker_with_exception
from samples import module_b
from tracing_core.session.snapshot import snapshot

from tracing_core.workflow.simple_tracer import SimpleTracer

#
event_buffer = []
tracer = SimpleTracer(event_buffer)
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
