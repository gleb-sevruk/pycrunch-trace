from pycrunch_trace import config
from pycrunch_trace.filters import can_trace_type


def test_can_trace_int():
    assert can_trace_type(1)


def test_can_trace_float():
    assert can_trace_type(1.5)

def test_can_trace_bool():
    assert can_trace_type(True)

def test_can_trace_none():
    assert can_trace_type(None)

def test_can_trace_string():
    assert can_trace_type('some_str')

def test_can_trace_dict():
    assert can_trace_type(dict(kwargs=dict(a=1)))

def test_no_trace_module():
    assert not can_trace_type(config)
