from typing import List, Optional

from .BoneData import BoneData
from .ConstraintData import ConstraintData


class TransformConstraintData(ConstraintData):
    """Stores the setup pose for a TransformConstraint."""

    def __init__(self, name: str):
        super().__init__(name)
        self.bones: List[BoneData] = []
        self.target: Optional[BoneData] = None
        self.rotate_mix: float = 0.0
        self.translate_mix: float = 0.0
        self.scale_mix: float = 0.0
        self.shear_mix: float = 0.0
        self.offset_rotation: float = 0.0
        self.offset_x: float = 0.0
        self.offset_y: float = 0.0
        self.offset_scale_x: float = 0.0
        self.offset_scale_y: float = 0.0
        self.offset_shear_y: float = 0.0
        self.relative: bool = False
        self.local: bool = False
