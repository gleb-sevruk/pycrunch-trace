import config
from tracing_core.filters.file_filtering import FileFilter


def test_included():
    sut = FileFilter()
    assert sut.should_trace(config.absolute_path)

def test_not_included():
    sut = FileFilter()
    assert not sut.should_trace('/crap/module/x.py')
