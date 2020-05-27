from pycrunch_trace.file_system.session_store import SessionStore
from pycrunch_trace.file_system.trace_session import TraceSession
from pycrunch_trace.tests.test_buffer import build_testing_events

def a():
    pass

def test_1():
    x = TraceSession()
    x.save('a', build_testing_events())

def test_session_store():
    x = SessionStore()
    session = x.load_session('a')
    session.load_metadata()
    print(vars(session.metadata))
def test_load_sessions():
    x = SessionStore()
    print(x.all_sessions())

def test_multiple_files():
    x = TraceSession('aaa')
    x.did_enter_traceable_file('a')
    x.did_enter_traceable_file('a2')
    x.did_enter_traceable_file('b')
    print('aaa')
    x.will_skip_file('c')
    x.will_skip_file('c')
    x.will_skip_file('d')
    x.buffer_became_available(build_testing_events())
    x.save()
