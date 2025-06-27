from .TranslateTimeline import TranslateTimeline
from ..Enums import TimelineType


class ShearTimeline(TranslateTimeline):
    """Changes a bone's local shear."""

    def get_property_id(self) -> int:
        return (TimelineType.SHEAR.value << 24) + self.bone_index
