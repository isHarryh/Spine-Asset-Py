from .PathConstraintPositionTimeline import PathConstraintPositionTimeline
from ..Enums import TimelineType


class PathConstraintSpacingTimeline(PathConstraintPositionTimeline):
    """Changes a path constraint's spacing."""

    def __init__(self, frame_count: int):
        super().__init__(frame_count)

    def get_property_id(self) -> int:
        return (TimelineType.PATH_CONSTRAINT_SPACING.value << 24) + self.path_constraint_index
