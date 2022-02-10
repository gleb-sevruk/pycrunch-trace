from functools import wraps
from pycrunch_trace.client.api.trace import Trace



def trace(session_name_or_func=None, additional_excludes=None, *decorator_args, **decorator_kws):
    """
       Starts tracing using PyCrunch tracing toolkit
   """
    def _decorator(func):
        @wraps(func)
        def wrapper(*args, **kws):
            internal_additional_exclude = None
            if 'additional_excludes' in locals():
                internal_additional_exclude = additional_excludes

            if 'session_name_or_func' not in locals() \
                    or callable(session_name_or_func) \
                    or session_name_or_func is None:
                session_name = str(func.__name__)
            else:
                session_name = session_name_or_func
            pycrunch_tracer = Trace()
            pycrunch_tracer.start(session_name, additional_excludes=internal_additional_exclude)
            try:
                results = func(*args, **kws)
                return results
            except Exception as e:
                message_code = str(e)
                raise
            finally:
                pycrunch_tracer.stop()

        return wrapper

    return _decorator(session_name_or_func) if callable(session_name_or_func) else _decorator
