from typing import Tuple

import io
import struct


class SkeletonBinaryReader:
    """Reader for basic data types in Spine binary format skeleton."""

    def __init__(self, data: bytes):
        self._stream = io.BytesIO(data)

    def read_byte(self) -> int:
        b = self._stream.read(1)
        if not b:
            raise EOFError("Unexpected end of stream")
        return b[0]

    def read_boolean(self) -> bool:
        return self.read_byte() != 0

    def read_float32(self) -> float:
        return struct.unpack("<f", self._stream.read(4))[0]

    def read_int16(self) -> int:
        return struct.unpack("<h", self._stream.read(2))[0]

    def read_int32(self) -> int:
        return struct.unpack("<i", self._stream.read(4))[0]

    def read_uint32(self) -> int:
        return struct.unpack("<I", self._stream.read(4))[0]

    def read_varint(self, optimize_positive: bool = True) -> int:
        result = 0
        # Read up to 5 bytes
        for i in range(5):
            b = self.read_byte()
            result |= (b & 0x7F) << (i * 7)
            if (b & 0x80) == 0:
                # MSB not set, no more bytes to read
                break
        if not optimize_positive:
            # Convert unsigned to signed
            result = (result >> 1) ^ -(result & 1)
        return result

    def read_string(self) -> str:
        length = self.read_varint()
        if length <= 1:
            return ""
        b = self._stream.read(length - 1)
        return b.decode("utf-8")

    def read_color(self, read_alpha: bool = True) -> Tuple[float, float, float, float]:
        if read_alpha:
            rgba = self.read_uint32()
            r = ((rgba >> 24) & 0xFF) / 255.0
            g = ((rgba >> 16) & 0xFF) / 255.0
            b = ((rgba >> 8) & 0xFF) / 255.0
            a = (rgba & 0xFF) / 255.0
            return (r, g, b, a)
        else:
            rgb = self.read_int32()
            r = ((rgb >> 16) & 0xFF) / 255.0
            g = ((rgb >> 8) & 0xFF) / 255.0
            b = (rgb & 0xFF) / 255.0
            return (r, g, b, 1.0)
