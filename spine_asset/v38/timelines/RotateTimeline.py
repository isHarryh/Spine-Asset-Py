from typing import List

from .CurveTimeline import CurveTimeline
from .Timeline import BoneTimeline
from ..Enums import TimelineType


class RotateTimeline(CurveTimeline, BoneTimeline):
    """Changes a bone's local rotation."""

    ENTRIES = 2

    def __init__(self, frame_count: int):
        super().__init__(frame_count)
        BoneTimeline.__init__(self)
        self.frames: List[float] = [0.0] * (frame_count << 1)

    def get_property_id(self) -> int:
        return (TimelineType.ROTATE.value << 24) + self.bone_index

    def set_frame(self, frame_index: int, time: float, degrees: float) -> None:
        frame_index <<= 1
        self.frames[frame_index] = time
        self.frames[frame_index + 1] = degrees
