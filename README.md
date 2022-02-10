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

This is also possible via decorator:

```python
from pycrunch_trace.client.api import trace

@trace(additional_excludes=['/Users/gleb/.venvs/pycrunch_trace'])
def run():
    some_code()
```




Use web app for replaying recording:

http://app.pytrace.com/

In case if you want to run UI locally, instead of using hosted version:
[Link for web app source code](https://github.com/gleb-sevruk/pycrunch-tracing-webui)

(Replays are not sent anywhere and processed entirely in-memory)
