import io
from pathlib import Path
from typing import Union

class AbstractFile:
    def as_bytes(self):
        pass

    def short_name(self):
        pass

class File(AbstractFile):
    class Mock(AbstractFile):
        def __init__(self, buffer: bytes, filename: str = None):
            if filename:
                self.filename = filename
            else:
                self.filename = 'mock'

            self.buffer = buffer

        def as_bytes(self):
            return self.buffer

        def short_name(self):
            return self.buffer
    filename: str

    def __init__(self, filename: Union[str, Path]):
        if type(filename) == str:
            self.filename = filename
        elif isinstance(filename, Path):
            self.filename = str(filename)

    def as_bytes(self):
        with io.FileIO(self.filename, mode='r') as current_file:
            return current_file.readall()

    def short_name(self) -> str:
        return Path(self.filename).name

    def __str__(self):
        return self.filename

