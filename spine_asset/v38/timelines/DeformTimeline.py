from typing import List, Optional

from .CurveTimeline import CurveTimeline
from .Timeline import SlotTimeline
from ..attachments import VertexAttachment
from ..Enums import TimelineType


class DeformTimeline(CurveTimeline, SlotTimeline):
    """Changes a slot's deform to deform a VertexAttachment."""

    def __init__(self, frame_count: int):
        super().__init__(frame_count)
        SlotTimeline.__init__(self)
        self.attachment: Optional[VertexAttachment] = None
        self.frames: List[float] = [0.0] * frame_count
        self.frame_vertices: List[List[float]] = [[] for _ in range(frame_count)]

    def get_property_id(self) -> int:
        # Deform timelines use a complex ID based on attachment and slot
        attachment_id = self.attachment.id if self.attachment else 0
        return (TimelineType.DEFORM.value << 27) + attachment_id + self.slot_index

    def set_frame(self, frame_index: int, time: float, vertices: List[float]) -> None:
        self.frames[frame_index] = time
        self.frame_vertices[frame_index] = vertices.copy()
