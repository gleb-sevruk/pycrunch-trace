from typing import Dict, Any


class FileMap:
    # this is for size reduction
    # filename.py -> id
    files: Dict[str, int]

    def __init__(self):
        self.files = dict()
        pass

    def file_id(self, filename: str) -> int:
        file_id = self.files.get(filename)
        if not file_id:
            file_id = len(self.files) + 1
            self.files[filename] = file_id

        return file_id

    def filename_by_id(self, search_for_file_id : int):
#         slow
        for (name, file_id) in self.files.items():
            if file_id == search_for_file_id:
                return name
        return f'file {search_for_file_id} not found'

    @classmethod
    def from_reverse(cls, files: Dict[str, int]):
        x = FileMap()
        x.files = files
        return x
