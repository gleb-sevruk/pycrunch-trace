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

Use web app for replaying recording:

http://app.pytrace.com/

In case if you want to run UI locally, instead of using hosted version:
[Link for web app source code](https://github.com/gleb-sevruk/pycrunch-tracing-webui)

(Replays are not sent anywhere and processed entirely in-memory)
