from pycrunch_tracer import config
from pycrunch_tracer.filters import FileFilter


def test_included():
    sut = FileFilter()
    assert sut.should_trace(config.absolute_path)

def test_not_included():
    sut = FileFilter()
    assert not sut.should_trace('/crap/module/x.py')
