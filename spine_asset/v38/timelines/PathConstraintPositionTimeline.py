from typing import List

from .CurveTimeline import CurveTimeline
from ..Enums import TimelineType


class PathConstraintPositionTimeline(CurveTimeline):
    """Changes a path constraint's position."""

    ENTRIES = 2

    def __init__(self, frame_count: int):
        super().__init__(frame_count)
        self.path_constraint_index: int = 0
        self.frames: List[float] = [0.0] * (frame_count * self.ENTRIES)

    def get_property_id(self) -> int:
        return (TimelineType.PATH_CONSTRAINT_POSITION.value << 24) + self.path_constraint_index

    def set_frame(self, frame_index: int, time: float, position: float) -> None:
        frame_index *= self.ENTRIES
        self.frames[frame_index] = time
        self.frames[frame_index + 1] = position
