from typing import List

from .Attachment import Attachment


class RegionAttachment(Attachment):
    """An attachment that displays a textured quadrilateral."""

    def __init__(self, name: str):
        super().__init__(name)
        self.path: str = ""
        self.x: float = 0.0
        self.y: float = 0.0
        self.scale_x: float = 1.0
        self.scale_y: float = 1.0
        self.rotation: float = 0.0
        self.width: float = 0.0
        self.height: float = 0.0
        self.color: List[float] = [1.0, 1.0, 1.0, 1.0]  # RGBA

    def set_path(self, path: str) -> None:
        self.path = path

    def set_x(self, x: float) -> None:
        self.x = x

    def set_y(self, y: float) -> None:
        self.y = y

    def set_scale_x(self, scale_x: float) -> None:
        self.scale_x = scale_x

    def set_scale_y(self, scale_y: float) -> None:
        self.scale_y = scale_y

    def set_rotation(self, rotation: float) -> None:
        self.rotation = rotation

    def set_width(self, width: float) -> None:
        self.width = width

    def set_height(self, height: float) -> None:
        self.height = height

    def update_offset(self) -> None:
        pass
