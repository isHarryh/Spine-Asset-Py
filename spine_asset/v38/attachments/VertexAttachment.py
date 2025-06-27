from typing import List, Optional

from .Attachment import Attachment


class VertexAttachment(Attachment):
    """Base class for attachments that have vertices and may be weighted."""

    def __init__(self, name: str):
        super().__init__(name)
        self.id: int = 0
        self.bones: Optional[List[int]] = None
        self.vertices: List[float] = []
        self.world_vertices_length: int = 0
        self.deform_attachment: Optional["VertexAttachment"] = None

    def set_world_vertices_length(self, length: int) -> None:
        self.world_vertices_length = length

    def set_vertices(self, vertices: List[float]) -> None:
        self.vertices = vertices

    def set_bones(self, bones: List[int]) -> None:
        self.bones = bones

    def set_deform_attachment(self, attachment: "VertexAttachment") -> None:
        self.deform_attachment = attachment
