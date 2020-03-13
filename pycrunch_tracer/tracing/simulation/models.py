from typing import Any


class EventKeys:
    call = 'call'
    line = 'line'
    event_return = 'return'
    exception = 'exception'


class Code:
    co_filename: str

    """ function name """
    co_name: str

    """ Number of arguments (excluding keyword, *, and **) """
    co_argcount: int

    """ machine bytecode """
    co_code: bytearray

class Frame:
    f_locals: dict
    f_back: Any
    f_builtins: Any
    f_code: Code
    f_lineno: int
