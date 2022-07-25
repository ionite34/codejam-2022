# Player Model for text game
from dataclasses import dataclass


@dataclass
class Player:
    """Player Model for text game."""

    uid: int
    name: str
    inventory: dict
