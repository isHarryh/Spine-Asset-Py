from typing import List

from .VertexAttachment import VertexAttachment


class BoundingBoxAttachment(VertexAttachment):
    """An attachment that consists of a polygon for collision detection."""

    def __init__(self, name: str):
        super().__init__(name)
        self.color: List[float] = [1.0, 1.0, 1.0, 1.0]  # RGBA
