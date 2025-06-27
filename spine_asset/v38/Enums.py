from enum import IntEnum


class BlendMode(IntEnum):
    """Determines how images are blended with existing pixels when drawn."""

    NORMAL = 0
    ADDITIVE = 1
    MULTIPLY = 2
    SCREEN = 3


class AttachmentType(IntEnum):
    """Attachment types for different kinds of attachments."""

    REGION = 0
    BOUNDINGBOX = 1
    MESH = 2
    LINKEDMESH = 3
    PATH = 4
    POINT = 5
    CLIPPING = 6


class BinaryAttachmentType(IntEnum):
    """Binary attachment type constants used in SkeletonBinary."""

    REGION = 0
    BOUNDINGBOX = 1
    MESH = 2
    LINKEDMESH = 3
    PATH = 4
    POINT = 5
    CLIPPING = 6


class BinaryTimelineType(IntEnum):
    """Binary timeline type constants used in SkeletonBinary."""

    # Bone timeline types
    BONE_ROTATE = 0
    BONE_TRANSLATE = 1
    BONE_SCALE = 2
    BONE_SHEAR = 3

    # Slot timeline types
    SLOT_ATTACHMENT = 0
    SLOT_COLOR = 1
    SLOT_TWO_COLOR = 2

    # Path constraint timeline types
    PATH_POSITION = 0
    PATH_SPACING = 1
    PATH_MIX = 2


class BinaryCurveType(IntEnum):
    """Binary curve type constants used in SkeletonBinary."""

    CURVE_LINEAR = 0
    CURVE_STEPPED = 1
    CURVE_BEZIER = 2


class PositionMode(IntEnum):
    """Position mode for path constraints."""

    FIXED = 0
    PERCENT = 1


class SpacingMode(IntEnum):
    """Spacing mode for path constraints."""

    LENGTH = 0
    FIXED = 1
    PERCENT = 2


class RotateMode(IntEnum):
    """Rotate mode for path constraints."""

    TANGENT = 0
    CHAIN = 1
    CHAIN_SCALE = 2


class TransformMode(IntEnum):
    """Transform mode for bones."""

    NORMAL = 0
    ONLY_TRANSLATION = 1
    NO_ROTATION_OR_REFLECTION = 2
    NO_SCALE = 3
    NO_SCALE_OR_REFLECTION = 4


class MixBlend(IntEnum):
    """Controls how a timeline value is mixed with the setup pose value or current pose value."""

    SETUP = 0
    FIRST = 1
    REPLACE = 2
    ADD = 3


class MixDirection(IntEnum):
    """Indicates whether a timeline's alpha is mixing out over time toward 0 or mixing in toward 1."""

    IN = 0
    OUT = 1


class TimelineType(IntEnum):
    """Internal enum for timeline types with ordinal values matching Java."""

    ROTATE = 0
    TRANSLATE = 1
    SCALE = 2
    SHEAR = 3
    ATTACHMENT = 4
    COLOR = 5
    DEFORM = 6
    EVENT = 7
    DRAW_ORDER = 8
    IK_CONSTRAINT = 9
    TRANSFORM_CONSTRAINT = 10
    PATH_CONSTRAINT_POSITION = 11
    PATH_CONSTRAINT_SPACING = 12
    PATH_CONSTRAINT_MIX = 13
    TWO_COLOR = 14
