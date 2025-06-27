from typing import List

from .CurveTimeline import CurveTimeline
from .Timeline import SlotTimeline
from ..Enums import TimelineType


class ColorTimeline(CurveTimeline, SlotTimeline):
    """Changes a slot's color."""

    ENTRIES = 5

    def __init__(self, frame_count: int):
        super().__init__(frame_count)
        SlotTimeline.__init__(self)
        self.frames: List[float] = [0.0] * (frame_count * self.ENTRIES)

    def get_property_id(self) -> int:
        return (TimelineType.COLOR.value << 24) + self.slot_index

    def set_frame(self, frame_index: int, time: float, r: float, g: float, b: float, a: float) -> None:
        frame_index *= self.ENTRIES
        self.frames[frame_index] = time
        self.frames[frame_index + 1] = r
        self.frames[frame_index + 2] = g
        self.frames[frame_index + 3] = b
        self.frames[frame_index + 4] = a
