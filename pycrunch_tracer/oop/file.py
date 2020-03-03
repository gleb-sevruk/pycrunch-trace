import io


class File:
    def __init__(self, filename: str):
        self.filename = filename

    def as_bytes(self):
        with io.FileIO(self.filename, mode='r') as current_file:
            return current_file.readall()
