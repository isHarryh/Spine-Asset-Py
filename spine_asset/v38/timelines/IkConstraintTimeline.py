from typing import List

from .CurveTimeline import CurveTimeline
from ..Enums import TimelineType


class IkConstraintTimeline(CurveTimeline):
    """Changes an IK constraint's mix and bend direction."""

    ENTRIES = 6

    def __init__(self, frame_count: int):
        super().__init__(frame_count)
        self.ik_constraint_index: int = 0
        self.frames: List[float] = [0.0] * (frame_count * self.ENTRIES)

    def get_property_id(self) -> int:
        return (TimelineType.IK_CONSTRAINT.value << 24) + self.ik_constraint_index

    def set_frame(
        self,
        frame_index: int,
        time: float,
        mix: float,
        softness: float,
        bend_direction: int,
        compress: bool,
        stretch: bool,
    ) -> None:
        frame_index *= self.ENTRIES
        self.frames[frame_index] = time
        self.frames[frame_index + 1] = mix
        self.frames[frame_index + 2] = softness
        self.frames[frame_index + 3] = bend_direction
        self.frames[frame_index + 4] = 1.0 if compress else 0.0
        self.frames[frame_index + 5] = 1.0 if stretch else 0.0
