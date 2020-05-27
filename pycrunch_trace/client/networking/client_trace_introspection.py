import collections
from collections import defaultdict
from typing import List, Dict

from pycrunch_trace.tracing.file_map import FileMap


class ClientTraceIntrospection:
    total_events: int

    def __init__(self):
        self.total_events = 0
        self.stats = defaultdict(int)
        # file id -> hit count
        self.top_files = defaultdict(int)

    def save_events(self, events: List):
        self.total_events += len(events)
        for e in events:
            self.stats[e.event_name] += 1
            self.top_files[e.cursor.file] += 1

    def print_to_console(self, files: Dict[str, int]):
        print('TraceIntrospection:')
        print('  stats:')
        for (each, hit_count) in self.stats.items():
            print(f' - {each}:{hit_count}')

        print('  files:')
        filemap = FileMap.from_reverse(files)
        sorted_x = sorted(self.top_files.items(), reverse=True, key=lambda kv: kv[1])
        sortir = collections.OrderedDict(sorted_x)


        for (each, hit_count) in sortir.items():
            print(f' - {hit_count} hits in {filemap.filename_by_id(each)}')


client_introspection = ClientTraceIntrospection()
