https://opensource.com/article/19/8/debug-python

settrace registers a trace function for the interpreter, which may be called in any of the following cases:

- Function call
- Line execution
- Function return
- Exception raised

 
 or:
 
 - 'call' 
 - 'line' 
 - 'return'  
 - 'exception'

When looking at this function, the first things that come to mind are its arguments and return values. The trace function arguments are:

frame object, which is the full state of the interpreter at the point of the function's execution
event string, which can be call, line, return, or exception
arg object, which is optional and depends on the event type


The local trace function should return a reference to itself (or to another function for further tracing in that scope), or None to turn off tracing in that scope.

https://docs.python.org/3/library/inspect.html

