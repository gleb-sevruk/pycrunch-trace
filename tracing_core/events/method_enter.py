from .base_event import Event


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
        self.variables[name] = value


class MethodEnterEvent(Event):
    cursor: ExecutionCursor
    input_variables: Variables

    def __init__(self, cursor: ExecutionCursor):
        self.cursor = cursor
        self.input_variables = Variables()
        self.event_name = 'method_enter'


class LineExecutionEvent(Event):
    cursor: ExecutionCursor
    locals: Variables

    def __init__(self, cursor):
        self.cursor = cursor
        self.locals = Variables()
        self.event_name = 'line'


class MethodExitEvent(Event):
    cursor: ExecutionCursor
    return_variables: Variables
    locals: Variables

    def __init__(self, cursor: ExecutionCursor):
        self.cursor = cursor
        self.return_variables = Variables()
        self.locals = Variables()
        self.event_name = 'method_exit'

