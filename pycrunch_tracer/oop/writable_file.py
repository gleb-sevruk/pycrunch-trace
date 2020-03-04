import io


class WriteableFile:
    def __init__(self, file_name: str, buffer: bytes):
        self.buffer = buffer
        self.file_name = file_name

    def save(self):
        with io.FileIO(self.file_name, 'w') as file:
            file.write(self.buffer)
