import logging
from . import AbstractFileFilter

logger = logging.getLogger(__name__)

class DefaultFileFilter(AbstractFileFilter):
    def should_trace(self, filename: str) -> bool:
        if not filename:
            return False
            
        exclusions = (
            '/Users/gleb/code/pycrunch_tracing/',
            '/Users/gleb/code/bc/briteapps-admin/',
            'module_a.py',
            'module_b.py',
            'module_c.py',
            'invalid_picker_with_exception.py',
            '/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6',
            '/Users/gleb/venv/PyCrunch/lib/python3.6/site-packages/',
            # 'copyreg.py',
            '/Users/gleb/venv/PyCrunch/lib/python3.6/site-packages/py/',
            'api/tracing.py'
        )

        if filename.startswith(exclusions) or filename.endswith(exclusions):
            return False

        if 'pycrunch_trace' in filename:
            return False

        if '<' in filename:
            return False
            
        return True