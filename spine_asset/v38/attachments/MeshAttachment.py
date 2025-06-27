from typing import List, Optional

from .VertexAttachment import VertexAttachment


class MeshAttachment(VertexAttachment):
    """An attachment that displays a textured mesh."""

    def __init__(self, name: str):
        super().__init__(name)
        self.path: str = ""
        self.color: List[float] = [1.0, 1.0, 1.0, 1.0]  # RGBA
        self.width: float = 0.0
        self.height: float = 0.0
        self.triangles: List[int] = []
        self.region_uvs: List[float] = []
        self.uvs: List[float] = []
        self.hull_length: int = 0
        self.edges: Optional[List[int]] = None
        self.parent_mesh: Optional["MeshAttachment"] = None
        self.deform_attachment: Optional[VertexAttachment] = None

    def set_path(self, path: str) -> None:
        self.path = path

    def set_width(self, width: float) -> None:
        self.width = width

    def set_height(self, height: float) -> None:
        self.height = height

    def set_triangles(self, triangles: List[int]) -> None:
        self.triangles = triangles

    def set_region_uvs(self, uvs: List[float]) -> None:
        self.region_uvs = uvs

    def update_uvs(self) -> None:
        self.uvs = self.region_uvs.copy()

    def set_hull_length(self, hull_length: int) -> None:
        self.hull_length = hull_length

    def set_edges(self, edges: List[int]) -> None:
        self.edges = edges

    def set_parent_mesh(self, parent_mesh: "MeshAttachment") -> None:
        self.parent_mesh = parent_mesh

    def set_deform_attachment(self, deform_attachment: VertexAttachment) -> None:
        self.deform_attachment = deform_attachment
