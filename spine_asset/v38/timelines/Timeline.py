from abc import ABC, abstractmethod


class Timeline(ABC):
    """Base interface for all timelines."""

    @abstractmethod
    def get_property_id(self) -> int:
        """Uniquely encodes both the type of this timeline and the skeleton property that it affects."""
        pass


class BoneTimeline(Timeline):
    """An interface for timelines which change the property of a bone."""

    def __init__(self):
        self.bone_index: int = 0


class SlotTimeline(Timeline):
    """An interface for timelines which change the property of a slot."""

    def __init__(self):
        self.slot_index: int = 0
