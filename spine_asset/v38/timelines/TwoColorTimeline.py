from typing import List

from .CurveTimeline import CurveTimeline
from .Timeline import SlotTimeline
from ..Enums import TimelineType


class TwoColorTimeline(CurveTimeline, SlotTimeline):
    """Changes a slot's color and dark color for two color tinting."""

    ENTRIES = 8

    def __init__(self, frame_count: int):
        super().__init__(frame_count)
        SlotTimeline.__init__(self)
        self.frames: List[float] = [0.0] * (frame_count * self.ENTRIES)

    def get_property_id(self) -> int:
        return (TimelineType.TWO_COLOR.value << 24) + self.slot_index

    def set_frame(
        self, frame_index: int, time: float, r: float, g: float, b: float, a: float, r2: float, g2: float, b2: float
    ) -> None:
        frame_index *= self.ENTRIES
        self.frames[frame_index] = time
        self.frames[frame_index + 1] = r  # R
        self.frames[frame_index + 2] = g  # G
        self.frames[frame_index + 3] = b  # B
        self.frames[frame_index + 4] = a  # A
        self.frames[frame_index + 5] = r2  # R2
        self.frames[frame_index + 6] = g2  # G2
        self.frames[frame_index + 7] = b2  # B2
