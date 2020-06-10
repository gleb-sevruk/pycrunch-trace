import six

if six.PY3:
    from typing import List

from pycrunch_trace.client.networking.commands import EventsSlice, FileContentSlice


class AbstractRecordingStrategy:
    def prepare(self):
        pass

    def recording_start(self, session_id):
        # type: (str) -> ()
        pass

    def recording_stop(self, session_id, files_include, files_excluded):
        # type: (str, List[str], List[str]) -> ()
        pass

    def recording_slice(self, x):
        # type: (EventsSlice) -> ()
        pass

    def files_slice(self, x):
        # type: (FileContentSlice) -> ()
        pass

    def clean(self):
        pass