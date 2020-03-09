from pycrunch_tracer.api.tracing import Yoba

yoba = Yoba()
yoba.start(session_name='demo_no_functon_calls')
# bellow should be traced even if no other calling function (via sys._getframe().f_back.f_trace = self._tracer.simple_tracer
x = 1
y = x * 3
print(y)

yoba.stop()
print(yoba._tracer.simulation.simulated_code())