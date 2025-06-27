from abc import ABC


class ConstraintData(ABC):
    """The base class for all constraint data."""

    def __init__(self, name: str):
        if name is None:
            raise ValueError("name cannot be null.")
        self.name = name
        self.order: int = 0
        self.skin_required: bool = False
