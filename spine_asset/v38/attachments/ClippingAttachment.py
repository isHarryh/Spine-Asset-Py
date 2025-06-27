from typing import List

from .VertexAttachment import VertexAttachment


class ClippingAttachment(VertexAttachment):
    """An attachment that clips rendering of other attachments."""

    def __init__(self, name: str):
        super().__init__(name)
        self.end_slot = None  # SlotData
        self.color: List[float] = [0.2, 0.2, 0.2, 1.0]  # Default color

    def set_end_slot(self, end_slot) -> None:
        self.end_slot = end_slot
