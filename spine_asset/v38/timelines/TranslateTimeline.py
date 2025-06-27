from typing import List

from .CurveTimeline import CurveTimeline
from .Timeline import BoneTimeline
from ..Enums import TimelineType


class TranslateTimeline(CurveTimeline, BoneTimeline):
    """Changes a bone's local translation."""

    ENTRIES = 3

    def __init__(self, frame_count: int):
        super().__init__(frame_count)
        BoneTimeline.__init__(self)
        self.frames: List[float] = [0.0] * (frame_count * self.ENTRIES)

    def get_property_id(self) -> int:
        return (TimelineType.TRANSLATE.value << 24) + self.bone_index

    def set_frame(self, frame_index: int, time: float, x: float, y: float) -> None:
        frame_index *= self.ENTRIES
        self.frames[frame_index] = time
        self.frames[frame_index + 1] = x
        self.frames[frame_index + 2] = y
