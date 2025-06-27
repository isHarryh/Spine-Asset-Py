from typing import Optional, Tuple

from .Enums import TransformMode


class BoneData:
    """Stores the setup pose for a Bone."""

    def __init__(self, index: int, name: str, parent: Optional["BoneData"] = None):
        if index < 0:
            raise ValueError("index must be >= 0.")
        if name is None:
            raise ValueError("name cannot be null.")

        self.index = index
        self.name = name
        self.parent = parent
        self.length: float = 0.0
        self.x: float = 0.0
        self.y: float = 0.0
        self.rotation: float = 0.0
        self.scale_x: float = 1.0
        self.scale_y: float = 1.0
        self.shear_x: float = 0.0
        self.shear_y: float = 0.0
        self.transform_mode: TransformMode = TransformMode.NORMAL
        self.skin_required: bool = False
        # Nonessential - color as RGBA tuple (0.61, 0.61, 0.61, 1.0) equivalent to 9b9b9bff
        self.color: Tuple[float, float, float, float] = (0.61, 0.61, 0.61, 1.0)
