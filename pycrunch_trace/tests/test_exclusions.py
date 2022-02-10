from pathlib import Path

from pycrunch_trace.filters import CustomFileFilter
from pycrunch_trace.oop import File


def test_additional_exclusions_considered():
    package_directory = Path(__file__).parent.parent

    sut = CustomFileFilter(File(package_directory.joinpath('pycrunch-profiles', 'default.profile.yaml')))
    sut._ensure_loaded()
    sut.add_additional_exclusions(['/this/is/excluded'])

    actual = sut.should_trace('/this/is/excluded/some.py')
    assert actual is False

    assert sut.should_trace('/this/is/included/main.py')
