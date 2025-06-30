from typing import Any, List, Optional, Union

import json

from .AtlasFile import AtlasFile
from .SkeletonData import SkeletonData
from .BoneData import BoneData
from .SlotData import SlotData
from .Event import Event
from .EventData import EventData
from .IkConstraintData import IkConstraintData
from .TransformConstraintData import TransformConstraintData
from .PathConstraintData import PathConstraintData
from .Skin import Skin
from .Animation import Animation
from .LinkedMesh import LinkedMesh
from .Enums import TransformMode, BlendMode, PositionMode, SpacingMode, RotateMode, AttachmentType
from .attachments import (
    RegionAttachment,
    MeshAttachment,
    BoundingBoxAttachment,
    PathAttachment,
    PointAttachment,
    ClippingAttachment,
    VertexAttachment,
)
from .timelines import (
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
    CurveTimeline,
)
from ..utils.SkeletonJsonReader import SkeletonJsonReader


class SkeletonJson:
    """Loads skeleton data in the Spine JSON format."""

    def __init__(self, atlas: Optional[AtlasFile] = None, scale: float = 1.0):
        if scale == 0:
            raise ValueError("scale cannot be 0")
        self.atlas = atlas
        self.scale = scale
        self.linked_meshes: List[LinkedMesh] = []

    def read_skeleton_data(self, content: Union[bytes, str]) -> SkeletonData:
        """Read skeleton data from JSON string or bytes."""
        reader = SkeletonJsonReader(json.loads(content))

        scale = self.scale
        skeleton_data = SkeletonData()

        # Skeleton header
        if "skeleton" in reader:
            header_reader = reader.get_child("skeleton")
            skeleton_data.hash = header_reader.get_string("hash", None)
            skeleton_data.version = header_reader.get_string("spine", None)
            if skeleton_data.version == "3.8.75":
                raise RuntimeError("Unsupported skeleton data, please export with a newer version of Spine.")
            skeleton_data.x = header_reader.get_float("x")
            skeleton_data.y = header_reader.get_float("y")
            skeleton_data.width = header_reader.get_float("width")
            skeleton_data.height = header_reader.get_float("height")
            skeleton_data.fps = header_reader.get_float("fps", 30.0)
            skeleton_data.images_path = header_reader.get_string("images", None)
            skeleton_data.audio_path = header_reader.get_string("audio", None)

        # Bones
        for bone_reader in reader.iter_child_list("bones"):
            parent = None
            parent_name = bone_reader.get_string("parent", None)
            if parent_name:
                parent = skeleton_data.find_bone(parent_name)
            bone = BoneData(len(skeleton_data.bones), bone_reader.get_string_required("name"), parent)
            bone.length = bone_reader.get_float("length") * scale
            bone.x = bone_reader.get_float("x") * scale
            bone.y = bone_reader.get_float("y") * scale
            bone.rotation = bone_reader.get_float("rotation")
            bone.scale_x = bone_reader.get_float("scaleX", 1.0)
            bone.scale_y = bone_reader.get_float("scaleY", 1.0)
            bone.shear_x = bone_reader.get_float("shearX")
            bone.shear_y = bone_reader.get_float("shearY")
            bone.transform_mode = bone_reader.get_enum("transform", TransformMode, TransformMode.NORMAL)
            bone.skin_required = bone_reader.get_bool("skin")
            color = bone_reader.get_color("color")
            if color:
                bone.color = color
            skeleton_data.bones.append(bone)

        # Slots
        for slot_reader in reader.iter_child_list("slots"):
            bone = skeleton_data.find_bone(slot_reader.get_string_required("bone"))
            slot = SlotData(len(skeleton_data.slots), slot_reader.get_string_required("name"), bone)
            color = slot_reader.get_color("color")
            if color:
                slot.color = color
            dark_color = slot_reader.get_color("dark")
            if dark_color:
                slot.dark_color = dark_color
            slot.attachment_name = slot_reader.get_string("attachment", None)
            slot.blend_mode = slot_reader.get_enum("blend", BlendMode, BlendMode.NORMAL)
            skeleton_data.slots.append(slot)

        # IK Constraints
        for ik_reader in reader.iter_child_list("ik"):
            ik = IkConstraintData(ik_reader.get_string_required("name"))
            ik.order = ik_reader.get_int("order")
            ik.skin_required = ik_reader.get_bool("skin")
            for bone_name in ik_reader.get_list("bones"):
                ik.bones.append(skeleton_data.find_bone(bone_name))
            target_name = ik_reader.get_string_required("target")
            ik.target = skeleton_data.find_bone(target_name)
            ik.mix = ik_reader.get_float("mix", 1.0)
            ik.softness = ik_reader.get_float("softness") * scale
            ik.bend_direction = 1 if ik_reader.get_bool("bendPositive", True) else -1
            ik.compress = ik_reader.get_bool("compress")
            ik.stretch = ik_reader.get_bool("stretch")
            ik.uniform = ik_reader.get_bool("uniform")
            skeleton_data.ik_constraints.append(ik)

        # Transform Constraints
        for tc_reader in reader.iter_child_list("transform"):
            tcd = TransformConstraintData(tc_reader.get_string_required("name"))
            tcd.order = tc_reader.get_int("order")
            tcd.skin_required = tc_reader.get_bool("skin")
            for bone_name in tc_reader.get_list("bones"):
                tcd.bones.append(skeleton_data.find_bone(bone_name))
            tcd.target = skeleton_data.find_bone(tc_reader.get_string_required("target"))
            tcd.local = tc_reader.get_bool("local")
            tcd.relative = tc_reader.get_bool("relative")
            tcd.offset_rotation = tc_reader.get_float("rotation")
            tcd.offset_x = tc_reader.get_float("x") * scale
            tcd.offset_y = tc_reader.get_float("y") * scale
            tcd.offset_scale_x = tc_reader.get_float("scaleX")
            tcd.offset_scale_y = tc_reader.get_float("scaleY")
            tcd.offset_shear_y = tc_reader.get_float("shearY")
            tcd.rotate_mix = tc_reader.get_float("rotateMix", 1.0)
            tcd.translate_mix = tc_reader.get_float("translateMix", 1.0)
            tcd.scale_mix = tc_reader.get_float("scaleMix", 1.0)
            tcd.shear_mix = tc_reader.get_float("shearMix", 1.0)
            skeleton_data.transform_constraints.append(tcd)

        # Path Constraints
        for path_reader in reader.iter_child_list("path"):
            pcd = PathConstraintData(path_reader.get_string_required("name"))
            pcd.order = path_reader.get_int("order")
            pcd.skin_required = path_reader.get_bool("skin")
            for bone_name in path_reader.get_list("bones"):
                pcd.bones.append(skeleton_data.find_bone(bone_name))
            pcd.target = skeleton_data.find_slot(path_reader.get_string_required("target"))
            pcd.position_mode = path_reader.get_enum("positionMode", PositionMode, PositionMode.PERCENT)
            pcd.spacing_mode = path_reader.get_enum("spacingMode", SpacingMode, SpacingMode.LENGTH)
            pcd.rotate_mode = path_reader.get_enum("rotateMode", RotateMode, RotateMode.TANGENT)
            pcd.offset_rotation = path_reader.get_float("rotation")
            pcd.position = path_reader.get_float("position")
            if pcd.position_mode == PositionMode.FIXED:
                pcd.position *= scale
            pcd.spacing = path_reader.get_float("spacing")
            if pcd.spacing_mode in (SpacingMode.LENGTH, SpacingMode.FIXED):
                pcd.spacing *= scale
            pcd.rotate_mix = path_reader.get_float("rotateMix", 1.0)
            pcd.translate_mix = path_reader.get_float("translateMix", 1.0)
            skeleton_data.path_constraints.append(pcd)

        # Skins
        for skin_reader in reader.iter_child_list("skins"):
            skin = self._read_skin(skin_reader, skeleton_data)
            skeleton_data.skins.append(skin)
            if skin.name == "default":
                skeleton_data.default_skin = skin

        # Linked meshes
        for linked_mesh in self.linked_meshes:
            if linked_mesh.skin:
                skin = skeleton_data.find_skin(linked_mesh.skin, fallback_default_skin=True)
            parent = skin.get_attachment(linked_mesh.slot_index, linked_mesh.parent)
            if not parent:
                raise Exception(f"Parent mesh not found: {linked_mesh.parent}")

            if isinstance(parent, MeshAttachment):
                if hasattr(linked_mesh.mesh, "set_deform_attachment") and hasattr(linked_mesh.mesh, "set_parent_mesh"):
                    deform_attachment = parent if linked_mesh.inherit_deform else linked_mesh.mesh
                    if isinstance(deform_attachment, VertexAttachment):
                        linked_mesh.mesh.set_deform_attachment(deform_attachment)
                    else:
                        raise Exception(
                            f"Deform attachment must be a VertexAttachment, but got {type(deform_attachment)}"
                        )
                    linked_mesh.mesh.set_parent_mesh(parent)
                    linked_mesh.mesh.update_uvs()
            else:
                raise Exception(f"Parent mesh not a MeshAttachment: {linked_mesh.parent}")
        self.linked_meshes.clear()

        # Events
        for event_name, event_map in reader.iter_child_dict("events"):
            event_data = EventData(event_name)
            event_data.int_value = event_map.get_int("int")
            event_data.float_value = event_map.get_float("float")
            event_data.string_value = event_map.get_string("string", "")
            event_data.audio_path = event_map.get_string("audio", None)
            if event_data.audio_path:
                event_data.volume = event_map.get_float("volume", 1.0)
                event_data.balance = event_map.get_float("balance")
            skeleton_data.events.append(event_data)

        # Animations
        for anim_name, anim_map in reader.iter_child_dict("animations"):
            animation = self._read_animation(anim_name, anim_map, skeleton_data)
            skeleton_data.animations.append(animation)

        return skeleton_data

    def _read_skin(self, skin_reader: SkeletonJsonReader, skeleton_data: SkeletonData) -> Skin:
        skin = Skin(skin_reader.get_string_required("name"))

        for bone_name in skin_reader.get_list("bones"):
            skin.bones.append(skeleton_data.find_bone(bone_name))

        for constraint_name in skin_reader.get_list("ik"):
            skin.constraints.append(skeleton_data.find_ik_constraint(constraint_name))

        for constraint_name in skin_reader.get_list("transform"):
            skin.constraints.append(skeleton_data.find_transform_constraint(constraint_name))

        for constraint_name in skin_reader.get_list("path"):
            skin.constraints.append(skeleton_data.find_path_constraint(constraint_name))

        for slot_name, slot_attachments_map in skin_reader.iter_child_dict("attachments"):
            slot = skeleton_data.find_slot(slot_name)
            for attachment_name in slot_attachments_map.keys():
                attachment = self._read_attachment(
                    attachment_name, slot_attachments_map.get_child(attachment_name), slot.index, skeleton_data
                )
                if attachment:
                    skin.set_attachment(slot.index, attachment_name, attachment)

        return skin

    def _read_attachment(
        self, attachment_name: str, reader: SkeletonJsonReader, slot_index: Any, skeleton_data: SkeletonData
    ):
        attachment_type = reader.get_enum("type", AttachmentType, AttachmentType.REGION)

        if attachment_type == AttachmentType.REGION:
            path = reader.get_string("path", attachment_name)
            region = RegionAttachment(attachment_name)
            region.set_path(path)
            region.set_x(reader.get_float("x") * self.scale)
            region.set_y(reader.get_float("y") * self.scale)
            region.set_scale_x(reader.get_float("scaleX", 1.0))
            region.set_scale_y(reader.get_float("scaleY", 1.0))
            region.set_rotation(reader.get_float("rotation"))
            if "width" not in reader:
                raise KeyError("width")
            if "height" not in reader:
                raise KeyError("height")
            region.set_width(reader.get_float("width") * self.scale)
            region.set_height(reader.get_float("height") * self.scale)
            color = reader.get_color("color")
            if color:
                region.color = list(color)
            region.update_offset()
            return region

        elif attachment_type == AttachmentType.BOUNDINGBOX:
            box = BoundingBoxAttachment(attachment_name)
            self._read_vertices(reader, box, reader.get_int("vertexCount") * 2)
            color = reader.get_color("color")
            if color:
                box.color = list(color)
            return box

        elif attachment_type in (AttachmentType.MESH, AttachmentType.LINKEDMESH):
            path = reader.get_string("path", attachment_name)
            mesh = MeshAttachment(attachment_name)
            mesh.set_path(path)
            color = reader.get_color("color")
            if color:
                mesh.color = list(color)  # Convert tuple to list for MeshAttachment
            mesh.set_width(reader.get_float("width") * self.scale)
            mesh.set_height(reader.get_float("height") * self.scale)
            parent = reader.get_string("parent", None)
            if parent:
                self.linked_meshes.append(
                    LinkedMesh(
                        mesh, reader.get_string("skin", None), slot_index, parent, reader.get_bool("deform", True)
                    )
                )
                return mesh
            uvs = reader.get_list("uvs", required=True)
            mesh.set_region_uvs(uvs)
            mesh.set_triangles(reader.get_list("triangles", required=True))
            self._read_vertices(reader, mesh, len(uvs))
            hull = reader.get_raw("hull")
            if hull is not None:
                mesh.set_hull_length(hull * 2)
            edges = reader.get_raw("edges")
            if edges is not None:
                mesh.set_edges(edges)
            mesh.update_uvs()
            return mesh

        elif attachment_type == AttachmentType.PATH:
            path_att = PathAttachment(attachment_name)
            path_att.set_closed(reader.get_bool("closed"))
            path_att.set_constant_speed(reader.get_bool("constantSpeed", True))
            count = reader.get_int("vertexCount")
            self._read_vertices(reader, path_att, count * 2)
            lengths = reader.get_list("lengths", required=True)
            path_att.set_lengths([l * self.scale for l in lengths])
            color = reader.get_color("color")
            if color:
                path_att.color = list(color)  # Convert tuple to list for PathAttachment
            return path_att

        elif attachment_type == AttachmentType.POINT:
            point = PointAttachment(attachment_name)
            point.x = reader.get_float("x") * self.scale
            point.y = reader.get_float("y") * self.scale
            point.rotation = reader.get_float("rotation")
            color = reader.get_color("color")
            if color:
                point.color = list(color)  # Convert tuple to list for PointAttachment
            return point

        elif attachment_type == AttachmentType.CLIPPING:
            clip = ClippingAttachment(attachment_name)
            end = reader.get_string("end", None)
            if end:
                end_slot = skeleton_data.find_slot(end)
                clip.end_slot = end_slot
            self._read_vertices(reader, clip, reader.get_int("vertexCount") * 2)
            color = reader.get_color("color")
            if color:
                clip.color = list(color)  # Convert tuple to list for ClippingAttachment
            return clip

        else:
            raise ValueError(f"Unknown attachment type: {attachment_type}")

    def _read_vertices(
        self, vertices_map: SkeletonJsonReader, vertices_attachment: VertexAttachment, vertices_length: int
    ):
        vertices_attachment.set_world_vertices_length(vertices_length)
        vertices = vertices_map.get_list("vertices", required=True)
        if len(vertices) == vertices_length:
            if self.scale != 1:
                vertices = [v * self.scale for v in vertices]
            vertices_attachment.set_vertices(vertices)
            return
        bones = []
        weights = []
        i = 0
        while i < len(vertices):
            bone_count = int(vertices[i])
            bones.append(bone_count)
            i += 1
            for _ in range(bone_count):
                bones.append(int(vertices[i]))
                weights.append(vertices[i + 1] * self.scale)
                weights.append(vertices[i + 2] * self.scale)
                weights.append(vertices[i + 3])
                i += 4
        vertices_attachment.set_bones(bones)
        vertices_attachment.set_vertices(weights)

    def _read_curve(self, curve_map: SkeletonJsonReader, timeline: CurveTimeline, frame_index: int):
        curve = curve_map.get_raw("curve")
        if curve is None:
            return
        if isinstance(curve, str):
            timeline.set_stepped(frame_index)
        elif isinstance(curve, float):
            c2, c3, c4 = curve_map.get_float("c2"), curve_map.get_float("c3", 1.0), curve_map.get_float("c4", 1.0)
            timeline.set_curve(frame_index, curve, c2, c3, c4)

    def _read_animation(self, anim_name: str, anim_map: SkeletonJsonReader, skeleton_data: SkeletonData) -> Animation:
        scale = self.scale
        timelines = []
        duration = 0

        # Slot timelines
        for slot_name, slot_map in anim_map.iter_child_dict("slots"):
            slot = skeleton_data.find_slot(slot_name)
            slot_index = slot.index
            for timeline_name in slot_map.keys():
                values = list(slot_map.iter_child_list(timeline_name))
                if timeline_name == "attachment":
                    timeline = AttachmentTimeline(len(values))
                    timeline.slot_index = slot_index
                    for i, value_map in enumerate(values):
                        timeline.set_frame(i, value_map.get_float("time"), value_map.get_string("name", None))
                    timelines.append(timeline)
                    if values:
                        duration = max(duration, timeline.frames[-1])
                elif timeline_name == "color":
                    timeline = ColorTimeline(len(values))
                    timeline.slot_index = slot_index
                    for i, value_map in enumerate(values):
                        time = value_map.get_float("time")
                        color = value_map.get_color("color", required=True)
                        assert color is not None
                        timeline.set_frame(i, time, *color)
                        self._read_curve(value_map, timeline, i)
                    timelines.append(timeline)
                    if values:
                        duration = max(duration, timeline.frames[(len(values) - 1) * ColorTimeline.ENTRIES])
                elif timeline_name == "twoColor":
                    timeline = TwoColorTimeline(len(values))
                    timeline.slot_index = slot_index
                    for i, value_map in enumerate(values):
                        time = value_map.get_float("time")
                        light = value_map.get_color("light", required=True)
                        dark = value_map.get_color("dark", required=True)
                        assert light is not None and dark is not None
                        timeline.set_frame(i, time, *light, *dark[0:3])
                        self._read_curve(value_map, timeline, i)
                    timelines.append(timeline)
                    if values:
                        duration = max(duration, timeline.frames[(len(values) - 1) * TwoColorTimeline.ENTRIES])
                else:
                    raise ValueError(f"Invalid timeline type for a slot: {timeline_name}")

        # Bone timelines
        for bone_name, bone_map in anim_map.iter_child_dict("bones"):
            bone = skeleton_data.find_bone(bone_name)
            bone_index = bone.index
            for timeline_name in bone_map.keys():
                values = list(bone_map.iter_child_list(timeline_name))
                timeline = None
                if timeline_name == "rotate":
                    timeline = RotateTimeline(len(values))
                    timeline.bone_index = bone_index
                    for i, value_map in enumerate(values):
                        timeline.set_frame(i, value_map.get_float("time"), value_map.get_float("angle"))
                        self._read_curve(value_map, timeline, i)
                elif timeline_name in ("translate", "scale", "shear"):
                    if timeline_name == "translate":
                        timeline = TranslateTimeline(len(values))
                    elif timeline_name == "scale":
                        timeline = ScaleTimeline(len(values))
                    else:
                        timeline = ShearTimeline(len(values))
                    timeline.bone_index = bone_index
                    for i, value_map in enumerate(values):
                        if timeline_name == "scale":
                            x = value_map.get_float("x", 1.0)
                            y = value_map.get_float("y", 1.0)
                        elif timeline == "translate":
                            x = value_map.get_float("x") * scale
                            y = value_map.get_float("y") * scale
                        else:
                            x = value_map.get_float("x")
                            y = value_map.get_float("y")
                        timeline.set_frame(i, value_map.get_float("time"), x, y)
                        self._read_curve(value_map, timeline, i)
                else:
                    raise ValueError(f"Invalid timeline type for a bone: {timeline_name}")
                timelines.append(timeline)
                if values:
                    duration = max(duration, timeline.frames[(len(values) - 1) * timeline.ENTRIES])

        # IK constraint timelines
        for ik_name in anim_map.iter_child_keys("ik"):
            ik = skeleton_data.find_ik_constraint(ik_name)
            values = list(anim_map.get_child("ik").iter_child_list(ik_name))
            timeline = IkConstraintTimeline(len(values))
            timeline.ik_constraint_index = ik.order
            for i, value_map in enumerate(values):
                timeline.set_frame(
                    i,
                    value_map.get_float("time"),
                    value_map.get_float("mix", 1.0),
                    value_map.get_float("softness") * scale,
                    1 if value_map.get_bool("bendPositive", True) else -1,
                    value_map.get_bool("compress", False),
                    value_map.get_bool("stretch", False),
                )
                self._read_curve(value_map, timeline, i)
            timelines.append(timeline)
            if values:
                duration = max(duration, timeline.frames[(len(values) - 1) * IkConstraintTimeline.ENTRIES])

        # Transform constraint timelines
        for tc_name in anim_map.iter_child_keys("transform"):
            tc = skeleton_data.find_transform_constraint(tc_name)
            values = list(anim_map.get_child("transform").iter_child_list(tc_name))
            timeline = TransformConstraintTimeline(len(values))
            timeline.transform_constraint_index = tc.order
            for i, value_map in enumerate(values):
                timeline.set_frame(
                    i,
                    value_map.get_float("time"),
                    value_map.get_float("rotateMix", 1.0),
                    value_map.get_float("translateMix", 1.0),
                    value_map.get_float("scaleMix", 1.0),
                    value_map.get_float("shearMix", 1.0),
                )
                self._read_curve(value_map, timeline, i)
            timelines.append(timeline)
            if values:
                duration = max(duration, timeline.frames[(len(values) - 1) * TransformConstraintTimeline.ENTRIES])

        # Path constraint timelines
        for path_name in anim_map.iter_child_keys("paths"):
            path = skeleton_data.find_path_constraint(path_name)
            path_index = path.order
            path_map = anim_map.get_child("paths").get_child(path_name)
            for timeline_name in path_map.keys():
                values = list(path_map.iter_child_list(timeline_name))
                timeline = None
                if timeline_name in ("position", "spacing"):
                    value_scale = 1
                    if timeline_name == "position":
                        timeline = PathConstraintPositionTimeline(len(values))
                        if path.position_mode == PositionMode.FIXED:
                            value_scale = scale
                    else:
                        timeline = PathConstraintSpacingTimeline(len(values))
                        if path.spacing_mode in (SpacingMode.LENGTH, SpacingMode.FIXED):
                            value_scale = scale
                    timeline.path_constraint_index = path_index
                    for i, value_map in enumerate(values):
                        timeline.set_frame(
                            i, value_map.get_float("time"), value_map.get_float(timeline_name) * value_scale
                        )
                        self._read_curve(value_map, timeline, i)
                elif timeline_name == "mix":
                    timeline = PathConstraintMixTimeline(len(values))
                    timeline.path_constraint_index = path_index
                    for i, value_map in enumerate(values):
                        timeline.set_frame(
                            i,
                            value_map.get_float("time"),
                            value_map.get_float("rotateMix", 1.0),
                            value_map.get_float("translateMix", 1.0),
                        )
                        self._read_curve(value_map, timeline, i)
                if timeline:
                    timelines.append(timeline)
                    if values:
                        duration = max(duration, timeline.frames[(len(values) - 1) * timeline.ENTRIES])

        # Deform timelines
        for skin_name in anim_map.iter_child_keys("deform"):
            skin = skeleton_data.find_skin(skin_name)
            skin_deform_map = anim_map.get_child("deform").get_child(skin_name)
            for slot_name in skin_deform_map.keys():
                slot = skeleton_data.find_slot(slot_name)
                slot_deform_map = skin_deform_map.get_child(slot_name)
                for mesh_name in slot_deform_map.keys():
                    attachment = skin.get_attachment(slot.index, mesh_name)
                    if not isinstance(attachment, VertexAttachment):
                        raise ValueError(f"Deform attachment not found or not a VertexAttachment: {mesh_name}")

                    is_weighted = attachment.bones is not None
                    base_vertices = attachment.vertices
                    deform_length = len(base_vertices) if not is_weighted else len(base_vertices) // 3 * 2

                    values = list(slot_deform_map.iter_child_list(mesh_name))
                    timeline = DeformTimeline(len(values))
                    timeline.slot_index = slot.index
                    timeline.attachment = attachment
                    for i, value_map in enumerate(values):
                        if "vertices" not in value_map:
                            deform = base_vertices if is_weighted else [0.0] * deform_length
                        else:
                            frame_vertices = value_map.get_list("vertices")
                            frame_vertices = [v * scale for v in frame_vertices]

                            deform = [0.0] * deform_length
                            start = value_map.get_int("offset")
                            deform[start : start + len(frame_vertices)] = frame_vertices

                            if not is_weighted:
                                for j in range(len(deform)):
                                    deform[j] += base_vertices[j]

                        timeline.set_frame(i, value_map.get_float("time"), deform)
                        self._read_curve(value_map, timeline, i)
                    timelines.append(timeline)
                    if values:
                        duration = max(duration, timeline.frames[len(values) - 1])

        # Draw order timeline
        if "drawOrder" in anim_map or "draworder" in anim_map:
            if "drawOrder" in anim_map:
                values = list(anim_map.iter_child_list("drawOrder"))
            else:
                values = list(anim_map.iter_child_list("draworder"))
            timeline = DrawOrderTimeline(len(values))
            for i, value_map in enumerate(values):
                draw_order = None
                offsets = value_map.get_list("offsets")
                if offsets:
                    draw_order = list(range(len(skeleton_data.slots)))
                    slots = skeleton_data.slots

                    original_draw_order = list(range(len(slots)))
                    for offset in offsets:
                        slot = skeleton_data.find_slot(offset["slot"])
                        slot_index = slot.index
                        original_draw_order.pop(original_draw_order.index(slot_index))
                        original_draw_order.insert(slot_index + offset["offset"], slot_index)
                    draw_order = original_draw_order

                timeline.set_frame(i, value_map.get_float("time"), draw_order)
            timelines.append(timeline)
            if values:
                duration = max(duration, timeline.frames[len(values) - 1])

        # Event timeline
        if "events" in anim_map:
            values = list(anim_map.iter_child_list("events"))
            timeline = EventTimeline(len(values))
            for i, value_map in enumerate(values):
                event_data = skeleton_data.find_event(value_map.get_string_required("name"))
                event = Event(value_map.get_float("time"), event_data)
                event.int_value = value_map.get_int("int", event_data.int_value)
                event.float_value = value_map.get_float("float", event_data.float_value)
                event.string_value = value_map.get_string("string", event_data.string_value)
                if event_data.audio_path:
                    event.volume = value_map.get_float("volume", 1.0)
                    event.balance = value_map.get_float("balance")
                timeline.set_frame(i, event)
            timelines.append(timeline)
            if values:
                duration = max(duration, timeline.frames[len(values) - 1])

        return Animation(anim_name, timelines, duration)
