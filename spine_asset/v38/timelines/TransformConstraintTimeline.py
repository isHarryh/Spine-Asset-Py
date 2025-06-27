from typing import List

from .CurveTimeline import CurveTimeline
from ..Enums import TimelineType


class TransformConstraintTimeline(CurveTimeline):
    """Changes a transform constraint's mix values."""

    ENTRIES = 5

    def __init__(self, frame_count: int):
        super().__init__(frame_count)
        self.transform_constraint_index: int = 0
        self.frames: List[float] = [0.0] * (frame_count * self.ENTRIES)

    def get_property_id(self) -> int:
        return (TimelineType.TRANSFORM_CONSTRAINT.value << 24) + self.transform_constraint_index

    def set_frame(
        self, frame_index: int, time: float, rotate_mix: float, translate_mix: float, scale_mix: float, shear_mix: float
    ) -> None:
        frame_index *= self.ENTRIES
        self.frames[frame_index] = time
        self.frames[frame_index + 1] = rotate_mix
        self.frames[frame_index + 2] = translate_mix
        self.frames[frame_index + 3] = scale_mix
        self.frames[frame_index + 4] = shear_mix
