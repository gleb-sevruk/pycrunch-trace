from functools import wraps
from pycrunch_tracer.client.api.yoba import Yoba



def yoba(session_name_or_func=None, *decorator_args, **decorator_kws):
    """
       Starts tracing using PyCrunch tracing toolkit
   """
    def _decorator(func):
        @wraps(func)
        def wrapper(*args, **kws):
            if 'session_name_or_func' not in locals() \
                    or callable(session_name_or_func) \
                    or session_name_or_func is None:
                session_name = str(func.__name__)
            else:
                session_name = session_name_or_func
            pycrunch_tracer = Yoba()
            pycrunch_tracer.start(session_name)

            results = func(*args, **kws)
            pycrunch_tracer.stop()
            return results

        return wrapper

    return _decorator(session_name_or_func) if callable(session_name_or_func) else _decorator
