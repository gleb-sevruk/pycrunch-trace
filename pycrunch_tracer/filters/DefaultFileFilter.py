from random import Random

from . import AbstractFileFilter


class DefaultFileFilter(AbstractFileFilter):
    def should_trace(self, filename: str) -> bool:
        # start or end with
        exclusions = (
            '/Users/gleb/code/pycrunch_tracing/',
            '/Users/gleb/code/bc/briteapps-admin/',
            'module_a.py',
            'module_b.py',
            'module_c.py',
            'invalid_picker_with_exception.py',
            '/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6'
            '/Users/gleb/venv/PyCrunch/lib/python3.6/site-packages/',
            # 'copyreg.py',
            '/Users/gleb/venv/PyCrunch/lib/python3.6/site-packages/py/',
            'api/tracing.py'
        )

        # r= Random()
        # if r.choice(range(0, 10)) == 1:
        #     return True
        # return True
        if filename.endswith(exclusions) or filename.startswith(exclusions):
            return False

        return True

        if filename.endswith(end_patterns):
            return True
        if filename.startswith(start_patterns):
            return True

        print('should_trace - false', filename)
        return False