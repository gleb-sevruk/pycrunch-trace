from abc import ABCMeta


class Event:
    __metaclass__ = ABCMeta
    # timestamp of event
    event_name = None  # type: str
    ts = None  # type: float
