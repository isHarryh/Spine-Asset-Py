from typing import List, Optional

from .BoneData import BoneData
from .ConstraintData import ConstraintData


class IkConstraintData(ConstraintData):
    """Stores the setup pose for an IkConstraint."""

    def __init__(self, name: str):
        super().__init__(name)
        self.bones: List[BoneData] = []
        self.target: Optional[BoneData] = None
        self.bend_direction: int = 1
        self.compress: bool = False
        self.stretch: bool = False
        self.uniform: bool = False
        self.mix: float = 1.0
        self.softness: float = 0.0
