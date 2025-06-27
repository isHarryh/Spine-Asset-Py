from typing import List, Any

from .Timeline import Timeline
from ..Enums import TimelineType


class EventTimeline(Timeline):
    """Fires events for key frames."""

    def __init__(self, frame_count: int):
        self.frames: List[float] = [0.0] * frame_count
        self.events: List[Any] = [None] * frame_count  # Event objects

    def get_property_id(self) -> int:
        return TimelineType.EVENT.value << 24

    def set_frame(self, frame_index: int, event: Any) -> None:
        self.frames[frame_index] = event.time
        self.events[frame_index] = event
