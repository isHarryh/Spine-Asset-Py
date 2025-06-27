from typing import List, Optional

from .Timeline import SlotTimeline
from ..Enums import TimelineType


class AttachmentTimeline(SlotTimeline):
    """Changes a slot's attachment."""

    def __init__(self, frame_count: int):
        super().__init__()
        self.frames: List[float] = [0.0] * frame_count
        self.attachment_names: List[Optional[str]] = [None] * frame_count

    def get_property_id(self) -> int:
        return (TimelineType.ATTACHMENT.value << 24) + self.slot_index

    def set_frame(self, frame_index: int, time: float, attachment_name: Optional[str]) -> None:
        self.frames[frame_index] = time
        self.attachment_names[frame_index] = attachment_name
