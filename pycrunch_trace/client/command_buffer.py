from collections import deque
from typing import List

from pycrunch_trace.events.base_event import Event


class ArrayCommandBuffer:
    def __init__(self):
        # todo swap implementation to linked list?
        self._command_buffer = []

    def add_event(self, evt):
        self._command_buffer.append(evt)

    def finish_chunk(self) -> List[Event]:
        old_buffer = self._command_buffer
        self._command_buffer = []
        return old_buffer

    def how_many_events(self):
        return len(self._command_buffer)

class DequeCommandBuffer:
    def __init__(self):
        self._command_buffer = deque()

    def add_event(self, evt):
        self._command_buffer.append(evt)

    def finish_chunk(self) -> List[Event]:
        old_buffer = self._command_buffer.copy()
        self._command_buffer.clear()
        return list(old_buffer)

    def how_many_events(self):
        return len(self._command_buffer)