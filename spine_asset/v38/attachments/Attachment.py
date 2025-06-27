from abc import ABC


class Attachment(ABC):
    """The base class for all attachments."""

    def __init__(self, name: str):
        if name is None:
            raise ValueError("name cannot be null.")
        self.name = name
