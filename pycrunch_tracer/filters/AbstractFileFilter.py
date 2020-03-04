class AbstractFileFilter:
    def should_trace(self, filename: str) -> bool:
        raise Exception('AbstractFileFilter: called too abstract should_trace function')