import yaml

from . import AbstractFileFilter
from ..oop import AbstractFile


class CustomFileFilter(AbstractFileFilter):
    exclusions: tuple
    profile_file: AbstractFile
    _loaded: bool

    def __init__(self, profile_file: AbstractFile):
        self.profile_file = profile_file
        self._loaded = False
        self.exclusions = ()

    def all_exclusions(self):
        self._ensure_loaded()
        return list(self.exclusions)

    def should_trace(self, filename: str):
        self._ensure_loaded()
        if filename.startswith(self.exclusions) or filename.endswith(self.exclusions):
            # print('should_trace: false - filename= '+filename)
            return False
        return True

    def _ensure_loaded(self):
        if self._loaded:
            return

        self._load()
        self._loaded = True

    def _load(self):
        all = yaml.load(self.profile_file.as_bytes(), Loader=yaml.FullLoader)
        tmp = set()
        exclusions = all.get('exclusions')
        if exclusions:
            for e in exclusions:
                tmp.add(e)
        self.exclusions = tuple(tmp)

