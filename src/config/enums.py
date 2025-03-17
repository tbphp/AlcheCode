"""Management of enumerations used in the application."""

from enum import Enum, auto


class StatusEnum(Enum):
    """Execution status enumeration."""

    SUCCESS = auto()
    ERROR = auto()
    DIRECT = auto()
