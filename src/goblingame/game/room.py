from __future__ import annotations

import typing as t
from abc import ABC, abstractmethod
from enum import Enum

if t.TYPE_CHECKING:
    from player import Player


class Direction(Enum):
    """Directions for movement."""

    NORTH = 1
    EAST = 2
    SOUTH = 3
    WEST = 4
    UP = 5
    DOWN = 6
    IN = 7
    OUT = 8
    NONE = 9


class Room(ABC):
    """Abstract Base Class for Rooms."""

    def __init__(self, player: Player):
        """Initialize the Room."""
        self.player = player

    @abstractmethod
    @property
    def name(self) -> str:
        """Return the name of the Room."""
        raise NotImplementedError

    @abstractmethod
    @property
    def description(self) -> str:
        """Return the description of the Room."""
        raise NotImplementedError

    @abstractmethod
    def connections(self) -> dict[Direction, Room]:
        """Return the connections to other Rooms."""
        raise NotImplementedError
