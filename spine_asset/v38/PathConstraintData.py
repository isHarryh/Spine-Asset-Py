from typing import List, Optional

from .BoneData import BoneData
from .ConstraintData import ConstraintData
from .Enums import PositionMode, SpacingMode, RotateMode
from .SlotData import SlotData


class PathConstraintData(ConstraintData):
    """Stores the setup pose for a PathConstraint."""

    def __init__(self, name: str):
        super().__init__(name)
        self.bones: List[BoneData] = []
        self.target: Optional[SlotData] = None
        self.position_mode: Optional[PositionMode] = None
        self.spacing_mode: Optional[SpacingMode] = None
        self.rotate_mode: Optional[RotateMode] = None
        self.offset_rotation: float = 0.0
        self.position: float = 0.0
        self.spacing: float = 0.0
        self.rotate_mix: float = 0.0
        self.translate_mix: float = 0.0
