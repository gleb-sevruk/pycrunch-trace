from pathlib import Path
from typing import Union

from .file import File


class Directory:
    path: Path

    def __init__(self, path: Union[str, Path]):
        if type(path) == str:
            self.path = Path(path)
        elif isinstance(path, Path):
            self.path = path
        else:
            raise Exception('Not supported path: ' + str(path))

    def folders(self):
        result = []
        self._ensure_created()
        for maybe_be_folder in self.path.glob('*'):
            if maybe_be_folder.is_dir():
                result.append(maybe_be_folder.name)
        return result

    def files(self, extension: str):
        if not self._exists():
            return []

        result = []
        for file in self.path.glob(f'*.{extension}'):
            result.append(File(file))
        return result

    def _ensure_created(self):
        if not self._exists():
            self.path.mkdir(exist_ok=True)

    def _exists(self):
        return self.path.exists()

    def __str__(self):
        return str(self.path)
