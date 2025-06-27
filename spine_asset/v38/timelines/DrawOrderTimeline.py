from typing import List, Optional

from .Timeline import Timeline
from ..Enums import TimelineType


class DrawOrderTimeline(Timeline):
    """Changes the skeleton's draw order."""

    def __init__(self, frame_count: int):
        self.frames: List[float] = [0.0] * frame_count
        self.draw_orders: List[Optional[List[int]]] = [None] * frame_count

    def get_property_id(self) -> int:
        return TimelineType.DRAW_ORDER.value << 24

    def set_frame(self, frame_index: int, time: float, draw_order: Optional[List[int]]) -> None:
        self.frames[frame_index] = time
        self.draw_orders[frame_index] = draw_order
