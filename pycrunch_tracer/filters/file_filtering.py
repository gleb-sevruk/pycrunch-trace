from random import Random


class FileFilter:
    def should_trace(self, filename: str) -> bool:
        start_patterns = (
            '/Users/gleb/code/pycrunch_tracing/',
            '/Users/gleb/code/bc/briteapps-admin/',
        )
        end_patterns = (
            'module_a.py',
            'module_b.py',
            'module_c.py',
            'invalid_picker_with_exception.py',
            # 'copyreg.py',
        )

        ending_exclusions = ('api/tracing.py',)

        # r= Random()
        # if r.choice(range(0, 10)) == 1:
        #     return True
        if filename.endswith(ending_exclusions):
            return False
        if filename.endswith(end_patterns):
            return True
        if filename.startswith(start_patterns):
            return True

        print('should_trace - false', filename)
        return False