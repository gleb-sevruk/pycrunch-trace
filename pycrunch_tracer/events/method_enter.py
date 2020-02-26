from .base_event import Event
from ..filters import can_trace_type


class ExecutionCursor:
    file: str
    line: int

    def __init__(self, file: str, line: int):
        self.file = file
        self.line = line


class Variables:
    variables: dict

    def __init__(self):
        self.variables = dict()

    def push_variable(self, name, value):
        self.variables[name] = self.ensure_safe_for_serialization(value)

    def ensure_safe_for_serialization(self, value):
        if not can_trace_type(value):
            value = str(type(value))
        return value


class MethodEnterEvent(Event):
    cursor: ExecutionCursor
    input_variables: Variables
    stack: list

    def __init__(self, cursor: ExecutionCursor, stack: list):
        self.cursor = cursor
        self.input_variables = Variables()
        self.stack = stack
        self.event_name = 'method_enter'


class LineExecutionEvent(Event):
    cursor: ExecutionCursor
    locals: Variables
    stack: list

    def __init__(self, cursor, stack: list):
        self.cursor = cursor
        self.locals = Variables()
        self.event_name = 'line'
        self.stack = stack


class MethodExitEvent(Event):
    cursor: ExecutionCursor
    return_variables: Variables
    locals: Variables
    stack: list

    def __init__(self, cursor: ExecutionCursor, stack: list):
        self.cursor = cursor
        self.return_variables = Variables()
        self.locals = Variables()
        self.event_name = 'method_exit'
        self.stack = stack

