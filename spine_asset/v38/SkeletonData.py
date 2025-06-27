from typing import List, Optional

from .Animation import Animation
from .BoneData import BoneData
from .EventData import EventData
from .IkConstraintData import IkConstraintData
from .PathConstraintData import PathConstraintData
from .Skin import Skin
from .SlotData import SlotData
from .TransformConstraintData import TransformConstraintData


class SkeletonData:
    """Stores the setup pose and all of the stateless data for a skeleton."""

    def __init__(self):
        self.name: Optional[str] = None
        self.bones: List[BoneData] = []  # Ordered parents first
        self.slots: List[SlotData] = []  # Setup pose draw order
        self.skins: List[Skin] = []
        self.default_skin: Optional[Skin] = None
        self.events: List[EventData] = []
        self.animations: List[Animation] = []
        self.ik_constraints: List[IkConstraintData] = []
        self.transform_constraints: List[TransformConstraintData] = []
        self.path_constraints: List[PathConstraintData] = []
        self.x: float = 0.0
        self.y: float = 0.0
        self.width: float = 0.0
        self.height: float = 0.0
        self.version: Optional[str] = None
        self.hash: Optional[str] = None
        # Nonessential
        self.fps: float = 30.0
        self.images_path: Optional[str] = None
        self.audio_path: Optional[str] = None

    def find_bone(self, bone_name: str) -> Optional[BoneData]:
        if bone_name is None:
            raise ValueError("bone_name cannot be null.")
        for bone in self.bones:
            if bone.name == bone_name:
                return bone
        return None

    def find_slot(self, slot_name: str) -> Optional[SlotData]:
        if slot_name is None:
            raise ValueError("slot_name cannot be null.")
        for slot in self.slots:
            if slot.name == slot_name:
                return slot
        return None

    def find_skin(self, skin_name: str) -> Optional[Skin]:
        if skin_name is None:
            raise ValueError("skin_name cannot be null.")
        for skin in self.skins:
            if skin.name == skin_name:
                return skin
        return None

    def find_event(self, event_data_name: str) -> Optional[EventData]:
        if event_data_name is None:
            raise ValueError("event_data_name cannot be null.")
        for event_data in self.events:
            if event_data.name == event_data_name:
                return event_data
        return None

    def find_animation(self, animation_name: str) -> Optional[Animation]:
        if animation_name is None:
            raise ValueError("animation_name cannot be null.")
        for animation in self.animations:
            if animation.name == animation_name:
                return animation
        return None

    def find_ik_constraint(self, constraint_name: str) -> Optional[IkConstraintData]:
        if constraint_name is None:
            raise ValueError("constraint_name cannot be null.")
        for constraint in self.ik_constraints:
            if constraint.name == constraint_name:
                return constraint
        return None

    def find_transform_constraint(self, constraint_name: str) -> Optional[TransformConstraintData]:
        if constraint_name is None:
            raise ValueError("constraint_name cannot be null.")
        for constraint in self.transform_constraints:
            if constraint.name == constraint_name:
                return constraint
        return None

    def find_path_constraint(self, constraint_name: str) -> Optional[PathConstraintData]:
        if constraint_name is None:
            raise ValueError("constraint_name cannot be null.")
        for constraint in self.path_constraints:
            if constraint.name == constraint_name:
                return constraint
        return None

    def get_default_skin(self) -> Optional[Skin]:
        return self.default_skin

    def __repr__(self) -> str:
        return "<SkeletonData version={}, name={}, bones={}, slots={}, skins={}, animations={}>".format(
            self.version,
            self.name,
            len(self.bones),
            len(self.slots),
            len(self.skins),
            len(self.animations),
        )
