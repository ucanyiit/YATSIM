"""Includes the interfaces used in the library."""

from enum import Enum, auto


# ----  Interfaces  ----
class TrainStatus(Enum):
    """Enumeration representing the state of a train."""

    STOPPED = auto()
    MOVING = auto()
    REVERSE = auto()


# ----  Exceptions  ----
class OutOfGridException(Exception):
    """Thrown when boundary check fails."""
