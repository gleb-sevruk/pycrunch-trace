from typing import List

from . import base_event
from .method_enter import MethodEnterEvent, MethodExitEvent, LineExecutionEvent
from ..file_system.human_readable_size import HumanReadableByteSize
from ..file_system.session_store import SessionStore

import pickle


def count_every_element(self, cleanup_function= None):
    accum = 0
    for e in self.buffer:
        if cleanup_function:
            cleanup_function(e)
        bytes_ = pickle.dumps(e)
        accum += len(bytes_)
    return accum

class SizeWithoutStack:
    def __init__(self, buffer):
        self.buffer = buffer

    def size(self):
        return count_every_element(self, self.clean_up_stack)

    def clean_up_stack(self, e):
        e.stack = None


class SizeOriginal:
    def __init__(self, buffer):
        self.buffer = buffer

    def size(self):
        return count_every_element(self)

    def clean_up_stack(self, e):
        e.stack = None


class SizeWithoutVariables:
    def __init__(self, buffer):
        self.buffer = buffer

    def size(self):
       return count_every_element(self, self.clean_up_vars)

    def clean_up_vars(self, e):
        if isinstance(e, MethodEnterEvent):
            e.input_variables = None
        if isinstance(e, MethodExitEvent):
            e.return_variables = None
            e.locals = None
        if isinstance(e, LineExecutionEvent):
            e.locals = None


class SizeWithoutCursor:
    def __init__(self, buffer):
        self.buffer = buffer

    def size(self):
        return count_every_element(self, self.clean_up_cursor)

    def clean_up_cursor(self, e):
        e.cursor = None

class SizeBreakdown:
    event_buffer: List[base_event.Event]

    @staticmethod
    def load_from_session():
        sess = SessionStore().load_session('request_exce')
        sess.load_metadata()
        print(f'metadata thinks size is: {sess.metadata.file_size_on_disk}')
        print()

        orig = SizeOriginal(sess.load_buffer())
        real_size = orig.size()
        SizeBreakdown.print_size('real size', real_size)

        total_bytes_so_far = SizeWithoutStack(sess.load_buffer())
        without_stack = total_bytes_so_far.size()
        SizeBreakdown.print_size('without stack', without_stack)

        without_variables = SizeWithoutVariables(sess.load_buffer())
        without_variables_size = without_variables.size()
        SizeBreakdown.print_size('without variables', without_variables_size)

        without_cursor = SizeWithoutCursor(sess.load_buffer())
        without_cursor_size = without_cursor.size()
        SizeBreakdown.print_size('without cursor', without_cursor_size)

        cursor = SizeWithoutCursor(sess.load_buffer())
        cursor.size()
        without_cursor_and_vars = SizeWithoutVariables(cursor.buffer)
        without_cursor_and_vars_size = without_cursor_and_vars.size()
        SizeBreakdown.print_size('without_cursor and vars', without_cursor_and_vars_size)

        print('matan:')


        # for i in range(100):
        #     print(bugger[i].event_name)

    @staticmethod
    def print_size(prefix, real_size):
        print(f'{prefix}: {HumanReadableByteSize(real_size)} ({real_size})')