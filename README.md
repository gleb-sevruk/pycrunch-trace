# Quick start


[Interactive Demo](http://app.pytrace.com/?open=v0.1-interactive-demo)

[Documentation](http://beta.pytrace.com/docs/trace-viewer)

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

Use web app for replaying recording:

http://app.pytrace.com/

(Replays are not sent anywhere and processed entirely in-memory)
