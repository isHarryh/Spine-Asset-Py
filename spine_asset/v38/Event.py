from typing import Optional

from .EventData import EventData


class Event:
    """Stores the current pose values for an Event."""

    def __init__(self, time: float, data: EventData):
        if data is None:
            raise ValueError("data cannot be null.")
        self.time = time
        self.data = data
        self.int_value: int = 0
        self.float_value: float = 0.0
        self.string_value: Optional[str] = None
        self.volume: float = 0.0
        self.balance: float = 0.0

    def set_int(self, int_value: int) -> None:
        self.int_value = int_value

    def set_float(self, float_value: float) -> None:
        self.float_value = float_value

    def set_string(self, string_value: str) -> None:
        if string_value is None:
            raise ValueError("stringValue cannot be null.")
        self.string_value = string_value

    def set_volume(self, volume: float) -> None:
        self.volume = volume

    def set_balance(self, balance: float) -> None:
        self.balance = balance
