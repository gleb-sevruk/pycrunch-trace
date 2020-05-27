from collections import deque, OrderedDict
from typing import Dict, Any

from pycrunch_trace.oop import Clock


class InlineProfiler:
    timings: Dict[str, float]

    def __init__(self):
        # method scope-> total time
        self.timings = OrderedDict()
        self.execution_stack = deque()

    def enter_scope(self, scope):
        self.execution_stack.append(scope)

    def get_full_stack(self):
        return '.'.join(self.execution_stack)

    def exit_scope(self):
        self.execution_stack.pop()

    def append_timing(self, scope: str, time_spent: float):
        stack___key = self.get_full_stack() + '.' + scope
        if not self.timings.get(stack___key):
            self.timings[stack___key] = time_spent
        else:
            self.timings[stack___key] += time_spent

    def print_timings(self):
        print(f'----print_timings----')
        for (key, val) in self.timings.items():
            print(f'{key}\t{val}')


inline_profiler_instance: InlineProfiler = InlineProfiler()
clock = Clock()

class ProfilingScope():
    def __init__(self, scope):
        self.scope = scope
        self.ts_begin = None
        self.ts_end = None

    def __enter__(self):
        self.ts_begin = clock.now()
        inline_profiler_instance.enter_scope(self.scope)
        return None

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.ts_end = clock.now()
        inline_profiler_instance.exit_scope()

        inline_profiler_instance.append_timing(self.scope, self.ts_end - self.ts_begin)