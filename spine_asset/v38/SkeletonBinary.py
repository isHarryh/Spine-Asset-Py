from typing import List, Optional

from .SkeletonData import SkeletonData
from .BoneData import BoneData
from .SlotData import SlotData
from .EventData import EventData
from .Event import Event
from .IkConstraintData import IkConstraintData
from .TransformConstraintData import TransformConstraintData
from .PathConstraintData import PathConstraintData
from .Skin import Skin
from .Animation import Animation
from .LinkedMesh import LinkedMesh
from .Enums import (
    TransformMode,
    BlendMode,
    PositionMode,
    SpacingMode,
    RotateMode,
    BinaryAttachmentType,
    BinaryTimelineType,
    BinaryCurveType,
)
from .attachments import (
    Attachment,
    RegionAttachment,
    MeshAttachment,
    PathAttachment,
    BoundingBoxAttachment,
    PointAttachment,
    ClippingAttachment,
    VertexAttachment,
)
from .timelines import (
    CurveTimeline,
    AttachmentTimeline,
    ColorTimeline,
    TwoColorTimeline,
    RotateTimeline,
    TranslateTimeline,
    ScaleTimeline,
    ShearTimeline,
    IkConstraintTimeline,
    TransformConstraintTimeline,
    PathConstraintPositionTimeline,
    PathConstraintSpacingTimeline,
    PathConstraintMixTimeline,
    DeformTimeline,
    DrawOrderTimeline,
    EventTimeline,
)
from ..utils import SkeletonBinaryReader


class SkeletonBinary:
    """Handler for Spine binary format skeleton."""

    def __init__(self, scale: float = 1.0):
        if scale == 0:
            raise ValueError("scale cannot be 0.")
        self.scale = scale
        self.linked_meshes: List[LinkedMesh] = []

    def read_skeleton_data(self, data: bytes) -> SkeletonData:
        """Read skeleton data from binary format."""
        self._reader = SkeletonBinaryReader(data)
        self.linked_meshes.clear()

        skeleton_data = SkeletonData()

        # Read header
        skeleton_data.hash = self._reader.read_string()
        if not skeleton_data.hash:
            skeleton_data.hash = None

        skeleton_data.version = self._reader.read_string()
        if not skeleton_data.version:
            skeleton_data.version = None

        if skeleton_data.version == "3.8.75":
            raise RuntimeError("Unsupported skeleton data, please export with a newer version of Spine.")

        skeleton_data.x = self._reader.read_float32()
        skeleton_data.y = self._reader.read_float32()
        skeleton_data.width = self._reader.read_float32()
        skeleton_data.height = self._reader.read_float32()

        nonessential = self._reader.read_boolean()
        if nonessential:
            skeleton_data.fps = self._reader.read_float32()
            skeleton_data.images_path = self._reader.read_string()
            if not skeleton_data.images_path:
                skeleton_data.images_path = None
            skeleton_data.audio_path = self._reader.read_string()
            if not skeleton_data.audio_path:
                skeleton_data.audio_path = None

        # Read strings
        self._strings = []
        string_count = self._reader.read_varint()
        for _ in range(string_count):
            self._strings.append(self._reader.read_string())

        # Read bones
        bone_count = self._reader.read_varint()
        for i in range(bone_count):
            name = self._reader.read_string()
            parent = None if i == 0 else skeleton_data.bones[self._reader.read_varint()]
            bone_data = BoneData(i, name, parent)
            bone_data.rotation = self._reader.read_float32()
            bone_data.x = self._reader.read_float32() * self.scale
            bone_data.y = self._reader.read_float32() * self.scale
            bone_data.scale_x = self._reader.read_float32()
            bone_data.scale_y = self._reader.read_float32()
            bone_data.shear_x = self._reader.read_float32()
            bone_data.shear_y = self._reader.read_float32()
            bone_data.length = self._reader.read_float32() * self.scale
            bone_data.transform_mode = self._get_transform_mode(self._reader.read_varint())
            bone_data.skin_required = self._reader.read_boolean()
            if nonessential:
                bone_data.color = self._reader.read_color()
            skeleton_data.bones.append(bone_data)

        # Read slots
        slot_count = self._reader.read_varint()
        for i in range(slot_count):
            slot_name = self._reader.read_string()
            bone_data = skeleton_data.bones[self._reader.read_varint()]
            slot_data = SlotData(i, slot_name, bone_data)
            slot_data.color = self._reader.read_color()

            dark_color = self._reader.read_int32()
            if dark_color != -1:
                # Convert the already-read dark_color value
                r = ((dark_color >> 16) & 0xFF) / 255.0
                g = ((dark_color >> 8) & 0xFF) / 255.0
                b = (dark_color & 0xFF) / 255.0
                slot_data.dark_color = (r, g, b, 1.0)

            slot_data.attachment_name = self._read_string_ref()
            slot_data.blend_mode = self._get_blend_mode(self._reader.read_varint())
            skeleton_data.slots.append(slot_data)

        # Read IK constraints
        ik_count = self._reader.read_varint()
        for i in range(ik_count):
            ik_data = IkConstraintData(self._reader.read_string())
            ik_data.order = self._reader.read_varint()
            ik_data.skin_required = self._reader.read_boolean()

            bone_count = self._reader.read_varint()
            for _ in range(bone_count):
                ik_data.bones.append(skeleton_data.bones[self._reader.read_varint()])

            ik_data.target = skeleton_data.bones[self._reader.read_varint()]
            ik_data.mix = self._reader.read_float32()
            ik_data.softness = self._reader.read_float32() * self.scale
            ik_data.bend_direction = self._reader.read_byte()
            ik_data.compress = self._reader.read_boolean()
            ik_data.stretch = self._reader.read_boolean()
            ik_data.uniform = self._reader.read_boolean()
            skeleton_data.ik_constraints.append(ik_data)

        # Read transform constraints
        transform_count = self._reader.read_varint()
        for i in range(transform_count):
            transform_data = TransformConstraintData(self._reader.read_string())
            transform_data.order = self._reader.read_varint()
            transform_data.skin_required = self._reader.read_boolean()

            bone_count = self._reader.read_varint()
            for _ in range(bone_count):
                transform_data.bones.append(skeleton_data.bones[self._reader.read_varint()])

            transform_data.target = skeleton_data.bones[self._reader.read_varint()]
            transform_data.local = self._reader.read_boolean()
            transform_data.relative = self._reader.read_boolean()
            transform_data.offset_rotation = self._reader.read_float32()
            transform_data.offset_x = self._reader.read_float32() * self.scale
            transform_data.offset_y = self._reader.read_float32() * self.scale
            transform_data.offset_scale_x = self._reader.read_float32()
            transform_data.offset_scale_y = self._reader.read_float32()
            transform_data.offset_shear_y = self._reader.read_float32()
            transform_data.rotate_mix = self._reader.read_float32()
            transform_data.translate_mix = self._reader.read_float32()
            transform_data.scale_mix = self._reader.read_float32()
            transform_data.shear_mix = self._reader.read_float32()
            skeleton_data.transform_constraints.append(transform_data)

        # Read path constraints
        path_count = self._reader.read_varint()
        for i in range(path_count):
            path_data = PathConstraintData(self._reader.read_string())
            path_data.order = self._reader.read_varint()
            path_data.skin_required = self._reader.read_boolean()

            bone_count = self._reader.read_varint()
            for _ in range(bone_count):
                path_data.bones.append(skeleton_data.bones[self._reader.read_varint()])

            path_data.target = skeleton_data.slots[self._reader.read_varint()]
            path_data.position_mode = self._get_position_mode(self._reader.read_varint())
            path_data.spacing_mode = self._get_spacing_mode(self._reader.read_varint())
            path_data.rotate_mode = self._get_rotate_mode(self._reader.read_varint())
            path_data.offset_rotation = self._reader.read_float32()

            position = self._reader.read_float32()
            if path_data.position_mode == PositionMode.FIXED:
                position *= self.scale
            path_data.position = position

            spacing = self._reader.read_float32()
            if path_data.spacing_mode in [SpacingMode.LENGTH, SpacingMode.FIXED]:
                spacing *= self.scale
            path_data.spacing = spacing

            path_data.rotate_mix = self._reader.read_float32()
            path_data.translate_mix = self._reader.read_float32()
            skeleton_data.path_constraints.append(path_data)

        # Read default skin
        default_skin = self._read_skin(True, nonessential, skeleton_data)
        if default_skin:
            skeleton_data.default_skin = default_skin
            skeleton_data.skins.append(default_skin)

        # Read skins
        skin_count = self._reader.read_varint()
        for _ in range(skin_count):
            skin = self._read_skin(False, nonessential, skeleton_data)
            if skin:
                skeleton_data.skins.append(skin)

        # Read events
        event_count = self._reader.read_varint()
        for _ in range(event_count):
            event_name = self._read_string_ref()
            event_data = EventData(event_name or "")  # Always create EventData even if name is None
            event_data.int_value = self._reader.read_varint(False)  # signed
            event_data.float_value = self._reader.read_float32()
            event_data.string_value = self._reader.read_string()
            event_data.audio_path = self._reader.read_string()
            if event_data.audio_path:
                event_data.volume = self._reader.read_float32()
                event_data.balance = self._reader.read_float32()
            skeleton_data.events.append(event_data)

        # Read animations
        animation_count = self._reader.read_varint()
        for _ in range(animation_count):
            animation_name = self._reader.read_string()
            animation = self._read_animation(animation_name, skeleton_data)
            skeleton_data.animations.append(animation)

        # Resolve linked meshes
        for linked_mesh in self.linked_meshes:
            skin = skeleton_data.default_skin if linked_mesh.skin is None else skeleton_data.find_skin(linked_mesh.skin)
            if skin is None:
                raise RuntimeError(f"Skin not found: {linked_mesh.skin}")
            parent = skin.get_attachment(linked_mesh.slot_index, linked_mesh.parent)
            if parent is None:
                raise RuntimeError(f"Parent mesh not found: {linked_mesh.parent}")
            if linked_mesh.inherit_deform and isinstance(parent, VertexAttachment):
                linked_mesh.mesh.deform_attachment = parent
            else:
                linked_mesh.mesh.deform_attachment = linked_mesh.mesh
            if isinstance(parent, MeshAttachment):
                linked_mesh.mesh.set_parent_mesh(parent)
                linked_mesh.mesh.update_uvs()

        self.linked_meshes.clear()

        return skeleton_data

    def _read_string_ref(self) -> Optional[str]:
        index = self._reader.read_varint()
        if index == 0:
            return None
        return self._strings[index - 1]

    def _read_skin(self, is_default_skin: bool, nonessential: bool, skeleton_data: SkeletonData) -> Optional[Skin]:
        if is_default_skin:
            slot_count = self._reader.read_varint()
            if slot_count == 0:
                return None
            skin = Skin("default")
        else:
            skin_name = self._read_string_ref()
            if skin_name is None:
                return None
            skin = Skin(skin_name)

            # Read bones
            bone_count = self._reader.read_varint()
            for _ in range(bone_count):
                bone_index = self._reader.read_varint()
                skin.bones.append(skeleton_data.bones[bone_index])

            # Read IK constraints
            ik_count = self._reader.read_varint()
            for _ in range(ik_count):
                ik_index = self._reader.read_varint()
                skin.constraints.append(skeleton_data.ik_constraints[ik_index])

            # Read transform constraints
            transform_count = self._reader.read_varint()
            for _ in range(transform_count):
                transform_index = self._reader.read_varint()
                skin.constraints.append(skeleton_data.transform_constraints[transform_index])

            # Read path constraints
            path_count = self._reader.read_varint()
            for _ in range(path_count):
                path_index = self._reader.read_varint()
                skin.constraints.append(skeleton_data.path_constraints[path_index])

            slot_count = self._reader.read_varint()

        # Read slot attachments
        for _ in range(slot_count):
            slot_index = self._reader.read_varint()
            attachment_count = self._reader.read_varint()

            for _ in range(attachment_count):
                attachment_name = self._read_string_ref()
                if attachment_name:
                    attachment = self._read_attachment(skin, slot_index, attachment_name, nonessential, skeleton_data)
                    if attachment:
                        skin.set_attachment(slot_index, attachment_name, attachment)

        return skin

    def _read_attachment(
        self,
        skin: Skin,
        slot_index: int,
        attachment_name: Optional[str],
        nonessential: bool,
        skeleton_data: SkeletonData,
    ) -> Optional[Attachment]:
        """Read attachment data."""
        if attachment_name is None:
            return None

        # First read the name (might be different from attachment_name)
        name = self._read_string_ref()
        if name is None:
            name = attachment_name

        attachment_type = self._get_attachment_type(self._reader.read_byte())

        if attachment_type == BinaryAttachmentType.REGION:  # Region
            path = self._read_string_ref()
            if path is None:
                path = name
            attachment = RegionAttachment(name)
            attachment.set_path(path)
            attachment.set_rotation(self._reader.read_float32())
            attachment.set_x(self._reader.read_float32() * self.scale)
            attachment.set_y(self._reader.read_float32() * self.scale)
            attachment.set_scale_x(self._reader.read_float32())
            attachment.set_scale_y(self._reader.read_float32())
            attachment.set_width(self._reader.read_float32() * self.scale)
            attachment.set_height(self._reader.read_float32() * self.scale)
            color = self._reader.read_color()
            attachment.color = [color[0], color[1], color[2], color[3]]
            attachment.update_offset()

        elif attachment_type == BinaryAttachmentType.MESH:  # Mesh
            path = self._read_string_ref()
            if path is None:
                path = name
            attachment = MeshAttachment(name)
            attachment.set_path(path)

            # Read color
            color = self._reader.read_color()
            attachment.color = [color[0], color[1], color[2], color[3]]

            # Read vertex count and UVs
            vertex_count = self._reader.read_varint()
            uvs = []
            for _ in range(vertex_count * 2):
                uvs.append(self._reader.read_float32())
            attachment.set_region_uvs(uvs)

            # Read triangles
            triangle_count = self._reader.read_varint()
            triangles = []
            for _ in range(triangle_count):
                triangles.append(self._reader.read_int16())
            attachment.set_triangles(triangles)

            # Read vertices
            vertices, bones = self._read_vertices(vertex_count)
            attachment.vertices = vertices
            if bones is not None:
                attachment.bones = bones
            attachment.set_hull_length(self._reader.read_varint() * 2)  # hullLength << 1

            if nonessential:
                # Read edges
                edge_count = self._reader.read_varint()
                edges = []
                for _ in range(edge_count):
                    edges.append(self._reader.read_int16())
                attachment.set_edges(edges)
                attachment.set_width(self._reader.read_float32() * self.scale)
                attachment.set_height(self._reader.read_float32() * self.scale)

            attachment.update_uvs()

        elif attachment_type == BinaryAttachmentType.LINKEDMESH:  # LinkedMesh
            path = self._read_string_ref()
            if path is None:
                path = name

            # Read color
            color = self._reader.read_color()

            skin_name = self._read_string_ref()
            parent_name = self._read_string_ref()
            inherit_deform = self._reader.read_boolean()

            width = 0.0
            height = 0.0
            if nonessential:
                width = self._reader.read_float32()
                height = self._reader.read_float32()

            attachment = MeshAttachment(name)
            attachment.set_path(path)
            attachment.color = [color[0], color[1], color[2], color[3]]

            if nonessential:
                attachment.set_width(width * self.scale)
                attachment.set_height(height * self.scale)

            # Store for later resolution
            if parent_name:
                linked_mesh = LinkedMesh(attachment, skin_name, slot_index, parent_name, inherit_deform)
                self.linked_meshes.append(linked_mesh)

        elif attachment_type == BinaryAttachmentType.PATH:  # Path
            closed = self._reader.read_boolean()
            constant_speed = self._reader.read_boolean()
            vertex_count = self._reader.read_varint()
            vertices, bones = self._read_vertices(vertex_count)

            # Read lengths
            lengths = []
            for _ in range(vertex_count // 3):
                lengths.append(self._reader.read_float32() * self.scale)

            attachment = PathAttachment(name)
            attachment.set_closed(closed)
            attachment.set_constant_speed(constant_speed)
            attachment.vertices = vertices
            if bones is not None:
                attachment.bones = bones
            attachment.set_lengths(lengths)

            if nonessential:
                color = self._reader.read_color()
                attachment.color = [color[0], color[1], color[2], color[3]]

        elif attachment_type == BinaryAttachmentType.BOUNDINGBOX:  # BoundingBox
            vertex_count = self._reader.read_varint()
            vertices, bones = self._read_vertices(vertex_count)

            attachment = BoundingBoxAttachment(name)
            attachment.vertices = vertices
            if bones is not None:
                attachment.bones = bones

            if nonessential:
                color = self._reader.read_color()
                attachment.color = [color[0], color[1], color[2], color[3]]

        elif attachment_type == BinaryAttachmentType.POINT:  # Point
            rotation = self._reader.read_float32()
            x = self._reader.read_float32()
            y = self._reader.read_float32()

            attachment = PointAttachment(name)
            attachment.x = x * self.scale
            attachment.y = y * self.scale
            attachment.rotation = rotation

            if nonessential:
                color = self._reader.read_color()
                attachment.color = [color[0], color[1], color[2], color[3]]

        elif attachment_type == BinaryAttachmentType.CLIPPING:  # Clipping
            end_slot_index = self._reader.read_varint()
            vertex_count = self._reader.read_varint()
            vertices, bones = self._read_vertices(vertex_count)

            attachment = ClippingAttachment(name)
            # Set end slot from skeleton data
            if end_slot_index < len(skeleton_data.slots):
                attachment.end_slot = skeleton_data.slots[end_slot_index]
            attachment.vertices = vertices
            if bones is not None:
                attachment.bones = bones

            if nonessential:
                color = self._reader.read_color()
                attachment.color = [color[0], color[1], color[2], color[3]]
        else:
            # Unknown attachment type, skip
            return None

        return attachment

    def _read_vertices(self, vertex_count: int) -> tuple:
        vertices_length = vertex_count * 2
        weighted = self._reader.read_boolean()

        if not weighted:
            # Simple vertex array
            vertices = []
            for _ in range(vertices_length):
                vertices.append(self._reader.read_float32() * self.scale)
            return vertices, None
        else:
            # Weighted vertices - store as flat arrays like Java
            weights = []
            bones_array = []

            for _ in range(vertex_count):
                bone_count = self._reader.read_varint()
                bones_array.append(bone_count)

                for _ in range(bone_count):
                    bones_array.append(self._reader.read_varint())  # bone index
                    weights.append(self._reader.read_float32() * self.scale)  # x
                    weights.append(self._reader.read_float32() * self.scale)  # y
                    weights.append(self._reader.read_float32())  # weight

            return weights, bones_array

    def _get_transform_mode(self, value: int) -> TransformMode:
        transform_modes = [
            TransformMode.NORMAL,
            TransformMode.ONLY_TRANSLATION,
            TransformMode.NO_ROTATION_OR_REFLECTION,
            TransformMode.NO_SCALE,
            TransformMode.NO_SCALE_OR_REFLECTION,
        ]
        if 0 <= value < len(transform_modes):
            return transform_modes[value]
        return TransformMode.NORMAL

    def _get_blend_mode(self, value: int) -> BlendMode:
        blend_modes = [BlendMode.NORMAL, BlendMode.ADDITIVE, BlendMode.MULTIPLY, BlendMode.SCREEN]
        if 0 <= value < len(blend_modes):
            return blend_modes[value]
        return BlendMode.NORMAL

    def _get_position_mode(self, value: int) -> PositionMode:
        if value == 0:
            return PositionMode.FIXED
        return PositionMode.PERCENT

    def _get_spacing_mode(self, value: int) -> SpacingMode:
        spacing_modes = [SpacingMode.LENGTH, SpacingMode.FIXED, SpacingMode.PERCENT]
        if 0 <= value < len(spacing_modes):
            return spacing_modes[value]
        return SpacingMode.LENGTH

    def _get_rotate_mode(self, value: int) -> RotateMode:
        rotate_modes = [RotateMode.TANGENT, RotateMode.CHAIN, RotateMode.CHAIN_SCALE]
        if 0 <= value < len(rotate_modes):
            return rotate_modes[value]
        return RotateMode.TANGENT

    def _get_attachment_type(self, value: int) -> BinaryAttachmentType:
        """Convert byte value to attachment type enum."""
        attachment_types = [
            BinaryAttachmentType.REGION,
            BinaryAttachmentType.BOUNDINGBOX,
            BinaryAttachmentType.MESH,
            BinaryAttachmentType.LINKEDMESH,
            BinaryAttachmentType.PATH,
            BinaryAttachmentType.POINT,
            BinaryAttachmentType.CLIPPING,
        ]
        if 0 <= value < len(attachment_types):
            return attachment_types[value]
        raise ValueError(f"Invalid attachment type: {value}")

    def _read_animation(self, name: str, skeleton_data: SkeletonData) -> Animation:
        timelines = []
        duration = 0.0

        # Slot timelines
        slot_count = self._reader.read_varint()
        for _ in range(slot_count):
            slot_index = self._reader.read_varint()
            timeline_count = self._reader.read_varint()

            for _ in range(timeline_count):
                timeline_type = self._reader.read_byte()
                frame_count = self._reader.read_varint()

                if timeline_type == BinaryTimelineType.SLOT_ATTACHMENT:
                    timeline = AttachmentTimeline(frame_count)
                    timeline.slot_index = slot_index
                    for frame_index in range(frame_count):
                        time = self._reader.read_float32()
                        attachment_name = self._read_string_ref()
                        timeline.set_frame(frame_index, time, attachment_name)
                    timelines.append(timeline)
                    duration = max(duration, timeline.frames[frame_count - 1])

                elif timeline_type == BinaryTimelineType.SLOT_COLOR:
                    timeline = ColorTimeline(frame_count)
                    timeline.slot_index = slot_index
                    for frame_index in range(frame_count):
                        time = self._reader.read_float32()
                        color = self._reader.read_color()
                        timeline.set_frame(frame_index, time, color[0], color[1], color[2], color[3])
                        if frame_index < frame_count - 1:
                            self._read_curve(timeline, frame_index)
                    timelines.append(timeline)
                    duration = max(duration, timeline.frames[(frame_count - 1) * 5])  # ColorTimeline.ENTRIES = 5

                elif timeline_type == BinaryTimelineType.SLOT_TWO_COLOR:
                    timeline = TwoColorTimeline(frame_count)
                    timeline.slot_index = slot_index
                    for frame_index in range(frame_count):
                        time = self._reader.read_float32()
                        light_color = self._reader.read_color()
                        dark_color = self._reader.read_color(read_alpha=False)
                        timeline.set_frame(
                            frame_index,
                            time,
                            light_color[0],
                            light_color[1],
                            light_color[2],
                            light_color[3],
                            dark_color[0],
                            dark_color[1],
                            dark_color[2],
                        )
                        if frame_index < frame_count - 1:
                            self._read_curve(timeline, frame_index)
                    timelines.append(timeline)
                    duration = max(duration, timeline.frames[(frame_count - 1) * 8])  # TwoColorTimeline.ENTRIES = 8

        # Bone timelines
        bone_count = self._reader.read_varint()
        for _ in range(bone_count):
            bone_index = self._reader.read_varint()
            timeline_count = self._reader.read_varint()

            for _ in range(timeline_count):
                timeline_type = self._reader.read_byte()
                frame_count = self._reader.read_varint()

                if timeline_type == BinaryTimelineType.BONE_ROTATE:
                    timeline = RotateTimeline(frame_count)
                    timeline.bone_index = bone_index
                    for frame_index in range(frame_count):
                        time = self._reader.read_float32()
                        angle = self._reader.read_float32()
                        timeline.set_frame(frame_index, time, angle)
                        if frame_index < frame_count - 1:
                            self._read_curve(timeline, frame_index)
                    timelines.append(timeline)
                    duration = max(duration, timeline.frames[(frame_count - 1) * 2])  # RotateTimeline.ENTRIES = 2

                elif timeline_type in [
                    BinaryTimelineType.BONE_TRANSLATE,
                    BinaryTimelineType.BONE_SCALE,
                    BinaryTimelineType.BONE_SHEAR,
                ]:
                    timeline_scale = 1.0
                    if timeline_type == BinaryTimelineType.BONE_SCALE:
                        timeline = ScaleTimeline(frame_count)
                    elif timeline_type == BinaryTimelineType.BONE_SHEAR:
                        timeline = ShearTimeline(frame_count)
                    else:  # BONE_TRANSLATE
                        timeline = TranslateTimeline(frame_count)
                        timeline_scale = self.scale

                    timeline.bone_index = bone_index
                    for frame_index in range(frame_count):
                        time = self._reader.read_float32()
                        x = self._reader.read_float32() * timeline_scale
                        y = self._reader.read_float32() * timeline_scale
                        timeline.set_frame(frame_index, time, x, y)
                        if frame_index < frame_count - 1:
                            self._read_curve(timeline, frame_index)
                    timelines.append(timeline)
                    duration = max(duration, timeline.frames[(frame_count - 1) * 3])  # TranslateTimeline.ENTRIES = 3

        # IK constraint timelines
        ik_count = self._reader.read_varint()
        for _ in range(ik_count):
            index = self._reader.read_varint()
            frame_count = self._reader.read_varint()
            timeline = IkConstraintTimeline(frame_count)
            timeline.ik_constraint_index = index

            for frame_index in range(frame_count):
                time = self._reader.read_float32()
                mix = self._reader.read_float32()
                softness = self._reader.read_float32() * self.scale
                bend_direction = self._reader.read_byte()
                compress = self._reader.read_boolean()
                stretch = self._reader.read_boolean()
                timeline.set_frame(frame_index, time, mix, softness, bend_direction, compress, stretch)
                if frame_index < frame_count - 1:
                    self._read_curve(timeline, frame_index)
            timelines.append(timeline)
            duration = max(duration, timeline.frames[(frame_count - 1) * 6])  # IkConstraintTimeline.ENTRIES = 6

        # Transform constraint timelines
        transform_count = self._reader.read_varint()
        for _ in range(transform_count):
            index = self._reader.read_varint()
            frame_count = self._reader.read_varint()
            timeline = TransformConstraintTimeline(frame_count)
            timeline.transform_constraint_index = index

            for frame_index in range(frame_count):
                time = self._reader.read_float32()
                rotate_mix = self._reader.read_float32()
                translate_mix = self._reader.read_float32()
                scale_mix = self._reader.read_float32()
                shear_mix = self._reader.read_float32()
                timeline.set_frame(frame_index, time, rotate_mix, translate_mix, scale_mix, shear_mix)
                if frame_index < frame_count - 1:
                    self._read_curve(timeline, frame_index)
            timelines.append(timeline)
            duration = max(duration, timeline.frames[(frame_count - 1) * 5])  # TransformConstraintTimeline.ENTRIES = 5

        # Path constraint timelines
        path_count = self._reader.read_varint()
        for _ in range(path_count):
            index = self._reader.read_varint()
            path_data = skeleton_data.path_constraints[index]
            timeline_count = self._reader.read_varint()

            for _ in range(timeline_count):
                timeline_type = self._reader.read_byte()
                frame_count = self._reader.read_varint()

                if timeline_type in [BinaryTimelineType.PATH_POSITION, BinaryTimelineType.PATH_SPACING]:
                    timeline_scale = 1.0
                    if timeline_type == BinaryTimelineType.PATH_SPACING:
                        timeline = PathConstraintSpacingTimeline(frame_count)
                        if path_data.spacing_mode in [SpacingMode.LENGTH, SpacingMode.FIXED]:
                            timeline_scale = self.scale
                    else:  # PATH_POSITION
                        timeline = PathConstraintPositionTimeline(frame_count)
                        if path_data.position_mode == PositionMode.FIXED:
                            timeline_scale = self.scale

                    timeline.path_constraint_index = index
                    for frame_index in range(frame_count):
                        time = self._reader.read_float32()
                        value = self._reader.read_float32() * timeline_scale
                        timeline.set_frame(frame_index, time, value)
                        if frame_index < frame_count - 1:
                            self._read_curve(timeline, frame_index)
                    timelines.append(timeline)
                    duration = max(
                        duration, timeline.frames[(frame_count - 1) * 2]
                    )  # PathConstraintPositionTimeline.ENTRIES = 2

                elif timeline_type == BinaryTimelineType.PATH_MIX:
                    timeline = PathConstraintMixTimeline(frame_count)
                    timeline.path_constraint_index = index
                    for frame_index in range(frame_count):
                        time = self._reader.read_float32()
                        rotate_mix = self._reader.read_float32()
                        translate_mix = self._reader.read_float32()
                        timeline.set_frame(frame_index, time, rotate_mix, translate_mix)
                        if frame_index < frame_count - 1:
                            self._read_curve(timeline, frame_index)
                    timelines.append(timeline)
                    duration = max(
                        duration, timeline.frames[(frame_count - 1) * 3]
                    )  # PathConstraintMixTimeline.ENTRIES = 3

        # Deform timelines
        deform_count = self._reader.read_varint()
        for _ in range(deform_count):
            skin_index = self._reader.read_varint()
            skin = skeleton_data.skins[skin_index]
            slot_count = self._reader.read_varint()

            for _ in range(slot_count):
                slot_index = self._reader.read_varint()
                attachment_count = self._reader.read_varint()

                for _ in range(attachment_count):
                    attachment_name = self._read_string_ref()
                    if not attachment_name:
                        continue
                    attachment = skin.get_attachment(slot_index, attachment_name)
                    if not isinstance(attachment, VertexAttachment):
                        continue

                    weighted = attachment.bones is not None
                    vertices = attachment.vertices
                    deform_length = len(vertices) // 3 * 2 if weighted else len(vertices)

                    frame_count = self._reader.read_varint()
                    timeline = DeformTimeline(frame_count)
                    timeline.slot_index = slot_index
                    timeline.attachment = attachment

                    for frame_index in range(frame_count):
                        time = self._reader.read_float32()
                        end = self._reader.read_varint()

                        if end == 0:
                            deform = [0.0] * deform_length if weighted else vertices[:]
                        else:
                            deform = [0.0] * deform_length
                            start = self._reader.read_varint()
                            end += start

                            if self.scale == 1.0:
                                for v in range(start, end):
                                    deform[v] = self._reader.read_float32()
                            else:
                                for v in range(start, end):
                                    deform[v] = self._reader.read_float32() * self.scale

                            if not weighted:
                                for v in range(len(deform)):
                                    deform[v] += vertices[v]

                        timeline.set_frame(frame_index, time, deform)
                        if frame_index < frame_count - 1:
                            self._read_curve(timeline, frame_index)

                    timelines.append(timeline)
                    duration = max(duration, timeline.frames[frame_count - 1])

        # Draw order timeline
        draw_order_count = self._reader.read_varint()
        if draw_order_count > 0:
            timeline = DrawOrderTimeline(draw_order_count)
            slot_count = len(skeleton_data.slots)

            for i in range(draw_order_count):
                time = self._reader.read_float32()
                offset_count = self._reader.read_varint()
                draw_order = [-1] * slot_count
                unchanged = [0] * (slot_count - offset_count)
                original_index = 0
                unchanged_index = 0

                for _ in range(offset_count):
                    slot_index = self._reader.read_varint()
                    # Collect unchanged items
                    while original_index != slot_index:
                        unchanged[unchanged_index] = original_index
                        unchanged_index += 1
                        original_index += 1
                    # Set changed items
                    offset = self._reader.read_varint()
                    new_index = original_index + offset
                    if 0 <= new_index < slot_count:  # Bounds check
                        draw_order[new_index] = original_index
                    original_index += 1

                # Collect remaining unchanged items
                while original_index < slot_count:
                    unchanged[unchanged_index] = original_index
                    unchanged_index += 1
                    original_index += 1

                # Fill in unchanged items
                for ii in range(slot_count - 1, -1, -1):
                    if draw_order[ii] == -1:
                        unchanged_index -= 1
                        draw_order[ii] = unchanged[unchanged_index]

                timeline.set_frame(i, time, draw_order)

            timelines.append(timeline)
            duration = max(duration, timeline.frames[draw_order_count - 1])

        # Event timeline
        event_count = self._reader.read_varint()
        if event_count > 0:
            timeline = EventTimeline(event_count)

            for i in range(event_count):
                time = self._reader.read_float32()
                event_data_index = self._reader.read_varint()
                event_data = skeleton_data.events[event_data_index]

                # Create event with override values
                int_value = self._reader.read_varint(False)  # signed
                float_value = self._reader.read_float32()
                string_value = self._reader.read_string() if self._reader.read_boolean() else event_data.string_value

                # Create event object
                event = Event(time, event_data)
                event.int_value = int_value
                event.float_value = float_value
                event.string_value = string_value

                if event_data.audio_path:
                    event.volume = self._reader.read_float32()
                    event.balance = self._reader.read_float32()

                timeline.set_frame(i, event)

            timelines.append(timeline)
            duration = max(duration, timeline.frames[event_count - 1])

        return Animation(name, timelines, duration)

    def _read_curve(self, timeline: CurveTimeline, frame_index: int):
        curve_type = self._reader.read_byte()

        if curve_type == BinaryCurveType.CURVE_STEPPED:
            timeline.set_stepped(frame_index)
        elif curve_type == BinaryCurveType.CURVE_BEZIER:
            cx1 = self._reader.read_float32()
            cy1 = self._reader.read_float32()
            cx2 = self._reader.read_float32()
            cy2 = self._reader.read_float32()
            timeline.set_curve(frame_index, cx1, cy1, cx2, cy2)
