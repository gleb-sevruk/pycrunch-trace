class AbstractFileFilter:
    def should_trace(self, filename: str) -> bool:
        self._abstract_exception()

    def should_record_variables(self) -> bool:
        self._abstract_exception()

    def _abstract_exception(self):
        raise Exception('AbstractFileFilter: called too abstract should_trace function')
