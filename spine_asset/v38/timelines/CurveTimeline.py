from abc import ABC
from typing import List

from .Timeline import Timeline


class CurveTimeline(Timeline, ABC):
    """The base class for timelines that use interpolation between key frame values."""

    LINEAR = 0.0
    STEPPED = 1.0
    BEZIER = 2.0
    BEZIER_SIZE = 10 * 2 - 1

    def __init__(self, frame_count: int):
        if frame_count <= 0:
            raise ValueError(f"frame_count must be > 0: {frame_count}")
        self.curves: List[float] = [0.0] * ((frame_count - 1) * self.BEZIER_SIZE)

    def get_frame_count(self) -> int:
        return len(self.curves) // self.BEZIER_SIZE + 1

    def set_linear(self, frame_index: int) -> None:
        self.curves[frame_index * self.BEZIER_SIZE] = self.LINEAR

    def set_stepped(self, frame_index: int) -> None:
        self.curves[frame_index * self.BEZIER_SIZE] = self.STEPPED

    def get_curve_type(self, frame_index: int) -> float:
        index = frame_index * self.BEZIER_SIZE
        if index == len(self.curves):
            return self.LINEAR
        curve_type = self.curves[index]
        if curve_type == self.LINEAR:
            return self.LINEAR
        if curve_type == self.STEPPED:
            return self.STEPPED
        return self.BEZIER

    def set_curve(self, frame_index: int, cx1: float, cy1: float, cx2: float, cy2: float) -> None:
        tmpx = (-cx1 * 2 + cx2) * 0.03
        tmpy = (-cy1 * 2 + cy2) * 0.03
        dddfx = ((cx1 - cx2) * 3 + 1) * 0.006
        dddfy = ((cy1 - cy2) * 3 + 1) * 0.006
        ddfx = tmpx * 2 + dddfx
        ddfy = tmpy * 2 + dddfy
        dfx = cx1 * 0.3 + tmpx + dddfx * 0.16666667
        dfy = cy1 * 0.3 + tmpy + dddfy * 0.16666667

        i = frame_index * self.BEZIER_SIZE
        curves = self.curves
        curves[i] = self.BEZIER
        i += 1

        x = dfx
        y = dfy
        n = i + self.BEZIER_SIZE - 1
        while i < n:
            curves[i] = x
            curves[i + 1] = y
            dfx += ddfx
            dfy += ddfy
            ddfx += dddfx
            ddfy += dddfy
            x += dfx
            y += dfy
            i += 2

    def get_curve_percent(self, frame_index: int, percent: float) -> float:
        percent = max(0.0, min(1.0, percent))  # Clamp between 0 and 1
        curves = self.curves
        i = frame_index * self.BEZIER_SIZE
        curve_type = curves[i]

        if curve_type == self.LINEAR:
            return percent
        if curve_type == self.STEPPED:
            return 0.0

        i += 1
        x = 0.0
        start = i
        n = i + self.BEZIER_SIZE - 1

        while i < n:
            x = curves[i]
            if x >= percent:
                if i == start:
                    return curves[i + 1] * percent / x  # First point is 0,0
                prev_x = curves[i - 2]
                prev_y = curves[i - 1]
                return prev_y + (curves[i + 1] - prev_y) * (percent - prev_x) / (x - prev_x)
            i += 2

        y = curves[i - 1]
        return y + (1 - y) * (percent - x) / (1 - x)  # Last point is 1,1
