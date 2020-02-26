class FileFilter:
    def should_trace(self, filename: str) -> bool:
        start_patterns = ('/Users/gleb/code/pycrunch_tracing/',)
        tuple_x = (
            'module_a.py',
            'module_b.py',
            'module_c.py',
            'invalid_picker_with_exception.py',
            'copyreg.py',
        )

        ending_exclusions = ('api/tracing.py',)
        # return True
        if filename.endswith(ending_exclusions):
            return False
        if filename.endswith(tuple_x):
            return True
        if filename.startswith(start_patterns):
            return True

        print('should_trace - false', filename)
        return False