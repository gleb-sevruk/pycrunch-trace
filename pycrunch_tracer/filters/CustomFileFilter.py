import yaml

from . import AbstractFileFilter
from ..oop import AbstractFile


class CustomFileFilter(AbstractFileFilter):
    exclusions: tuple
    _trace_variables: bool
    profile_file: AbstractFile
    _loaded: bool

    def __init__(self, profile_file: AbstractFile):
        self.profile_file = profile_file
        self._loaded = False
        self._trace_variables = True
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
        self.load_exclusions(all)
        self.load_variables(all)

    def load_exclusions(self, all):
        tmp = set()
        exclusions = all.get('exclusions')
        if exclusions:
            for e in exclusions:
                tmp.add(e)
        self.exclusions = tuple(tmp)

    def load_variables(self, all):
        trace_vars = all.get('trace_variables')
        if isinstance(trace_vars, bool):
            self._trace_variables = trace_vars
            if not self._trace_variables:
                print('!! PyCrunch - Variables will not be recorded in session')

    def should_record_variables(self) -> bool:
        self._ensure_loaded()
        return self._trace_variables

