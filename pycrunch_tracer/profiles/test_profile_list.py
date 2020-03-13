from pathlib import Path
from typing import List, Any

import yaml

from ..filters import CustomFileFilter
from ..oop import Directory, AbstractFile
from ..oop import File


class Profiles:
    def __init__(self, directory: Directory):
        self.directory = directory


def test_profiles():
    directory = Directory(Path.joinpath(Path(__file__).parent.parent, 'pycrunch-profiles'))
    print(directory)
    all = directory.folders()
    all = directory.files('yaml')
    print(str(all[0].short_name()))




def test_profile_should_have_excluded():
    buffer = b"""
exclusions:
  - no_trace.py
  - /Library/
    """
    sut = CustomFileFilter(File.Mock(buffer))

    assert not sut.should_trace('no_trace.py')
    assert not sut.should_trace('/Library/a.py')
    assert sut.should_trace('b.py')
    assert sut.should_trace('/code/b.py')


def test_profile_trace_vars_false():
    buffer = b"""
trace_variables: false
    """
    sut = CustomFileFilter(File.Mock(buffer))

    assert not sut.should_record_variables()


def profiles_dir():
    return Directory(Path.joinpath(Path(__file__).parent, 'pycrunch-profiles'))