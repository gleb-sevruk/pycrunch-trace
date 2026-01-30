# UI Overview

![PyTrace UI](https://hsto.org/webt/vp/im/xd/vpimxdvufmcmirahmktwpii79vw.png)


# Quick start

[Interactive Demo](https://app.pytrace.com/?open=v0.1-interactive-demo)

[Documentation](https://pytrace.com)


`pip install pycrunch-trace`

Then, Add attribute `@trace` to the method you want to record

```python
from pycrunch_trace.client.api import trace

@trace
def run():
    some_code()
```

Or, alternatively, without decorator:

```python
from pycrunch_trace.client.api import Trace

tracer = Trace()
tracer.start('recording_name')

some_code()

tracer.stop()
```


Optional session_name can be also passed to decorator:
```python
@trace('my_custom_recording_name')
``` 

# Configuration via Environment Variables

You can configure the tracer using environment variables (or a `.env` file in your project root):

- `PYCRUNCH_S3_ENABLED`: Set to `true` to enable S3 storage (requires `boto3`).
- `PYCRUNCH_S3_BUCKET`: The name of your S3 bucket.
- `PYCRUNCH_S3_PREFIX`: Optional prefix (route) for S3 keys.
- `PYCRUNCH_EXCLUDE_BUILTINS`: Set to `true` (default) to automatically exclude builtin and frozen modules from traces.
- `PYCRUNCH_KEEP_SESSIONS`: Set to `true` (default) to append a unique 8-character ID to each trace, preventing executions from overwriting each other.
- `PYCRUNCH_ORGANIZE_BY_DATE`: Set to `true` to organize recordings in subfolders by date and time (e.g., `2026_01_29_22_47_04/my_function_UUID`).

# Logging

PyCrunch Trace uses the builtin Python `logging` module. You can configure the logging level and format in your project to see or hide tracer logs.

This will make easier to integrate with your logging system.

By default, it uses the `pycrunch_trace` logger. You can customize it as follows:

```python
import logging

# Configure PyCrunch logger
logging.getLogger('pycrunch_trace').setLevel(logging.INFO)
```

# S3 Storage Support

If you have `boto3` installed and configured in your environment, you can store traces directly in S3. 

1. Install `boto3`: `pip install boto3`
2. Configure environment variables:
   ```bash
    PYCRUNCH_S3_ENABLED=true
    PYCRUNCH_S3_BUCKET=my-trace-bucket
    PYCRUNCH_S3_PREFIX=traces/
   ```
3. The tracer will automatically upload files upon completion.

# Serverless (AWS Lambda / Cloud Functions)

When running in a serverless environment, ensure all events are flushed before the process exits:

- **Using `@trace` decorator**: Handling is **automatic**. The tracer ensures all events are flushed/uploaded before the decorated function returns.
- **Manual Tracing**: Ensure you call `tracer.stop()` to trigger the flush mechanism.

The tracer is optimized to wait for the background transmission thread to finish in such environments.

### Specifying custom folders/files to exclude 
this will greatly speed-up profiler, however calls to the ignored directories will be ignored. 

Exclusion will be considered if absolute file path either `starts_with` or `ends_with` with given stop-list. 

```python
from pycrunch_trace.client.api import Trace
 
t = Trace()
t.start(additional_excludes=[
             '/Users/gleb/.venvs/pycrunch_trace'
             '/Users/gleb/.pyenv/versions/3.6.15/',
             'unwanted_file.py',
        ])

some_code()

t.stop()

```

@trace(additional_excludes=['/Users/gleb/.venvs/pycrunch_trace'])
def run():
    some_code()
```

# Decorator Ordering

The order in which you apply decorators matters. Python decorators are applied from the **bottom up** (closest to the function first).

- **Outer `@trace` (Outermost)**: If you place `@trace` on top of other decorators, it will record the execution of those decorators as well. This is usually recommended for debugging cross-cutting concerns like authentication or caching.
- **Inner `@trace` (Innermost)**: If you place `@trace` directly above the function definition (below other decorators), it will only record the body of your function. The other decorators will not be tracked in the trace.

```python
# RECOMMENDED: Track everything, including other decorators
@trace
@my_auth_decorator
def my_function():
    ...

# Track ONLY the function body (auth logic will be invisible in trace)
@my_auth_decorator
@trace
def my_function():
    ...
```




Use web app for replaying recording:

http://app.pytrace.com/

In case if you want to run UI locally, instead of using hosted version:
[Link for web app source code](https://github.com/gleb-sevruk/pycrunch-tracing-webui)

(Replays are not sent anywhere and processed entirely in-memory)
