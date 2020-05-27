from abc import ABC, abstractmethod


class Event(ABC):
    # timestamp of event
    event_name: str
    ts: float
