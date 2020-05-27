import pycrunch_trace.events.method_enter as events
import collections


class CallStack:
    def __init__(self):
        self.stack = collections.deque()

    def enter_frame(self, execution_cursor: events.ExecutionCursor):
        parent_frame = self.get_parent_frame()
        # print(f"{execution_cursor.file}:{execution_cursor.line} -> {parent_frame} ")
        frame = events.StackFrame.new(parent_frame, execution_cursor)
        self.stack.append(frame)

    def get_parent_frame(self):
        if len(self.stack) > 0:
            return self.stack[-1]
        return None

    def new_cursor_in_current_frame(self, new_cursor: events.ExecutionCursor):
        stack_frame: events.StackFrame = self.top_level_frame_as_clone()
        stack_frame.line = new_cursor.line
        stack_frame.file = new_cursor.file
        stack_frame.function_name = new_cursor.function_name
        # todo this is probably dirty hack?
        # or just replacing last-known stack frame
        #  todo what about performance ?
        if len(self.stack) > 0:
            self.stack.pop()
            self.stack.append(stack_frame)
            # self.stack[-1] = stack_frame
        else:
            # session just begin, not yet in any stack
            self.stack.append(stack_frame)


    def exit_frame(self):
        self.stack.pop()

    def top_level_frame_as_clone(self):
        current: events.StackFrame = self.current_frame()
        # print('top_level_frame_as_clone ->' + str(current))
        return events.StackFrame.clone(current)
        # ???
        # return current

    def current_frame(self):
        frame = self.get_parent_frame()
        return frame
