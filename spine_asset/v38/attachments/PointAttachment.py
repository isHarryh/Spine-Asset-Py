from typing import List

from .Attachment import Attachment


class PointAttachment(Attachment):
    """An attachment which is a single point and a rotation."""

    def __init__(self, name: str):
        super().__init__(name)
        self.x: float = 0.0
        self.y: float = 0.0
        self.rotation: float = 0.0
        self.color: List[float] = [0.38, 0.94, 0.0, 1.0]  # Default color

    def set_x(self, x: float) -> None:
        self.x = x

    def set_y(self, y: float) -> None:
        self.y = y

    def set_rotation(self, rotation: float) -> None:
        self.rotation = rotation
