# Player Model for text game
from dataclasses import dataclass, field


@dataclass
class Player:
    """Player Model for text game."""

    uid: int
    name: str
    # Inventory of item_name: quantity
    inventory: dict = field(default_factory=dict)
    # State flags
    states: dict = field(default_factory=dict)
