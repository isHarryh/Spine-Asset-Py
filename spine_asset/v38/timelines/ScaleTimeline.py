from .TranslateTimeline import TranslateTimeline
from ..Enums import TimelineType


class ScaleTimeline(TranslateTimeline):
    """Changes a bone's local scale."""

    def get_property_id(self) -> int:
        return (TimelineType.SCALE.value << 24) + self.bone_index
