from typing import List, Set

from .timelines.Timeline import Timeline


class Animation:
    """A simple container for a list of timelines and a name."""

    def __init__(self, name: str, timelines: List[Timeline], duration: float):
        if name is None:
            raise ValueError("name cannot be null.")
        self.name = name
        self.duration = duration
        self.timeline_ids: Set[int] = set()
        self.set_timelines(timelines if timelines is not None else [])

    def set_timelines(self, timelines: List[Timeline]) -> None:
        if timelines is None:
            raise ValueError("timelines cannot be null.")
        self.timelines = timelines

        self.timeline_ids.clear()
        for timeline in timelines:
            self.timeline_ids.add(timeline.get_property_id())
