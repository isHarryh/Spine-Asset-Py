from typing import List

from .VertexAttachment import VertexAttachment


class PathAttachment(VertexAttachment):
    """An attachment whose vertices make up a composite Bezier curve."""

    def __init__(self, name: str):
        super().__init__(name)
        self.closed: bool = False
        self.constant_speed: bool = True
        self.lengths: List[float] = []
        self.color: List[float] = [1.0, 1.0, 1.0, 1.0]  # RGBA

    def set_closed(self, closed: bool) -> None:
        self.closed = closed

    def set_constant_speed(self, constant_speed: bool) -> None:
        self.constant_speed = constant_speed

    def set_lengths(self, lengths: List[float]) -> None:
        self.lengths = lengths
