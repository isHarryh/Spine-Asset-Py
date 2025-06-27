from typing import Optional


class EventData:
    """Stores the setup pose values for an Event."""

    def __init__(self, name: str):
        if name is None:
            raise ValueError("name cannot be null.")
        self.name = name
        self.int_value: int = 0
        self.float_value: float = 0.0
        self.string_value: Optional[str] = None
        self.audio_path: Optional[str] = None
        self.volume: float = 0.0
        self.balance: float = 0.0
