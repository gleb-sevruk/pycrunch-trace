from typing import TypeVar

from .base_event import Event
from ..filters import can_trace_type


class ExecutionCursor:
    function_name: str
    file: int
    line: int

    def __init__(self, file: int, line: int, function_name: str):
        self.function_name = function_name
        self.file = file
        self.line = line

class StackFrameIds:
    last_id: int
    def __init__(self):
        self.last_id = 1

    def new_id(self):
        ret = self.last_id
        self.last_id += 1
        return ret

stack_ids = StackFrameIds()

class StackFrame:
    # parent: StackFrame
    def __init__(self, parent, file: id, line: int, function_name: str):
        self.parent = parent
        self.file = file
        self.line = line
        self.id = stack_ids.new_id()
        self.function_name = function_name

    def as_id(self):
        return self.id


    @classmethod
    def new(cls, parent, execution_cursor: ExecutionCursor):
        return StackFrame(parent, execution_cursor.file, execution_cursor.line, execution_cursor.function_name)

    @classmethod
    def clone(cls, origin):
        if not origin:
            return StackFrame.empty()
        return StackFrame(origin.parent, origin.file, origin.line, origin.function_name)

    @classmethod
    def empty(cls):
        return StackFrame(None, None, None, None)

    def __str__(self):
        return f'{self.file}:{self.function_name}:{self.line} -> \n\t {self.parent}'




class Variables:
    variables: dict

    def __init__(self):
        # self.variables = None
        # return
        self.variables = dict()

    def push_variable(self, name, value):
        self.variables[name] = self.ensure_safe_for_serialization(value)

    def ensure_safe_for_serialization(self, value):
        # return 'a'
        # todo is this slowdown?
        if not can_trace_type(value):
            value = str(type(value))
        if type(value) == dict:
            return value.copy()
        return value


class MethodEnterEvent(Event):
    cursor: ExecutionCursor
    input_variables: Variables
    stack: StackFrame

    def __init__(self, cursor: ExecutionCursor, stack: StackFrame, ts: float):
        self.cursor = cursor
        self.input_variables = Variables()
        self.stack = stack
        self.event_name = 'method_enter'
        self.ts = ts


class LineExecutionEvent(Event):
    cursor: ExecutionCursor
    locals: Variables
    stack: StackFrame

    def __init__(self, cursor, stack: StackFrame, ts: float):
        self.cursor = cursor
        self.locals = Variables()
        self.event_name = 'line'
        self.stack = stack
        self.ts = ts





class MethodExitEvent(Event):
    cursor: ExecutionCursor
    return_variables: Variables
    locals: Variables
    stack: StackFrame

    def __init__(self, cursor: ExecutionCursor, stack: StackFrame, ts: float):
        self.cursor = cursor
        self.return_variables = Variables()
        self.locals = Variables()
        self.event_name = 'method_exit'
        self.stack = stack
        self.ts = ts

