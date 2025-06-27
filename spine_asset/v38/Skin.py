from typing import Dict, List, Optional

from .attachments import Attachment
from .BoneData import BoneData
from .ConstraintData import ConstraintData


class SkinEntry:
    """Stores an entry in the skin consisting of the slot index, name, and attachment."""

    def __init__(self, slot_index: int = 0, name: str = "", attachment: Optional[Attachment] = None):
        self.set(slot_index, name)
        self.attachment = attachment

    def set(self, slot_index: int, name: str) -> None:
        if name is None:
            raise ValueError("name cannot be null.")
        self.slot_index = slot_index
        self.name = name
        self._hash_code = hash(name) + slot_index * 37

    def __hash__(self) -> int:
        return self._hash_code

    def __eq__(self, other) -> bool:
        if other is None:
            return False
        if not isinstance(other, SkinEntry):
            return False
        if self.slot_index != other.slot_index:
            return False
        if self.name != other.name:
            return False
        return True


class Skin:
    """Stores attachments by slot index and attachment name."""

    def __init__(self, name: str):
        if name is None:
            raise ValueError("name cannot be null.")
        self.name = name
        self.attachments: Dict[SkinEntry, SkinEntry] = {}
        self.bones: List[BoneData] = []
        self.constraints: List[ConstraintData] = []
        self._lookup = SkinEntry()

    def set_attachment(self, slot_index: int, name: str, attachment: Attachment) -> None:
        if slot_index < 0:
            raise ValueError("slot_index must be >= 0.")
        if attachment is None:
            raise ValueError("attachment cannot be null.")

        new_entry = SkinEntry(slot_index, name, attachment)
        old_entry = self.attachments.get(new_entry)
        if old_entry is not None:
            old_entry.attachment = attachment
        else:
            self.attachments[new_entry] = new_entry

    def get_attachment(self, slot_index: int, name: str) -> Optional[Attachment]:
        if slot_index < 0:
            raise ValueError("slot_index must be >= 0.")
        self._lookup.set(slot_index, name)
        entry = self.attachments.get(self._lookup)
        return entry.attachment if entry is not None else None
