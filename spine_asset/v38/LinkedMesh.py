from typing import Optional

from .attachments import MeshAttachment


class LinkedMesh:
    """Stores information for linking meshes during parsing."""

    def __init__(self, mesh: MeshAttachment, skin: Optional[str], slot_index: int, parent: str, inherit_deform: bool):
        self.mesh = mesh
        self.skin = skin
        self.slot_index = slot_index
        self.parent = parent
        self.inherit_deform = inherit_deform
