import pycrunch_trace.events.method_enter as e
from pycrunch_trace.config import config
from pycrunch_trace.serialization import to_string


def test_simple():
    command_stack = build_testing_events()
    # print(command_stack)
    print(to_string(command_stack))





def build_testing_events():
    command_stack = []
    stack = ['a:11', 'b:12']
    method_enter_event = e.MethodEnterEvent(e.ExecutionCursor(config.absolute_path, 2), stack)
    method_enter_event.input_variables.push_variable('some_number', 1)
    command_stack.append(method_enter_event)
    line_1 = e.LineExecutionEvent(e.ExecutionCursor(config.absolute_path, 3), stack)
    line_1.locals.push_variable('a', 2)
    command_stack.append(line_1)
    line_2 = e.LineExecutionEvent(e.ExecutionCursor(config.absolute_path, 4), stack)
    line_2.locals.push_variable('a', 2)
    line_2.locals.push_variable('b', 3)
    command_stack.append(line_2)
    line_3 = e.LineExecutionEvent(e.ExecutionCursor(config.absolute_path, 5), stack)
    line_3.locals.push_variable('a', 2)
    line_3.locals.push_variable('b', 3)
    line_3.locals.push_variable('result', 6)
    command_stack.append(line_3)
    line_return = e.MethodExitEvent(e.ExecutionCursor(config.absolute_path, 6), stack)
    line_return.return_variables.push_variable('return_value', 6)
    command_stack.append(line_return)
    return command_stack
