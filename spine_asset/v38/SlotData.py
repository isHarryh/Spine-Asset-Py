from typing import Optional, Tuple

from .Enums import BlendMode
from .BoneData import BoneData


class SlotData:
    """Stores the setup pose for a Slot."""

    def __init__(self, index: int, name: str, bone_data: BoneData):
        if index < 0:
            raise ValueError("index must be >= 0.")
        if name is None:
            raise ValueError("name cannot be null.")
        if bone_data is None:
            raise ValueError("bone_data cannot be null.")

        self.index = index
        self.name = name
        self.bone_data = bone_data
        self.color: Tuple[float, float, float, float] = (1.0, 1.0, 1.0, 1.0)
        self.dark_color: Optional[Tuple[float, float, float, float]] = None
        self.attachment_name: Optional[str] = None
        self.blend_mode: Optional[BlendMode] = None

    def set_color(self, r: float, g: float, b: float, a: float):
        self.color = (r, g, b, a)

    def set_dark_color(self, r: float, g: float, b: float, a: float):
        self.dark_color = (r, g, b, a)
