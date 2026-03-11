"""
Player class for managing individual player state.
"""

from typing import List, Optional
from dataclasses import dataclass, field
from .tiles import Tile, sort_tiles


@dataclass
class Meld:
    """Represents a called meld (pon, chi, kan)."""
    type: str  # "pon", "chi", "kan"
    tiles: List[Tile]
    from_player: Optional[int] = None  # Which player the tile was called from


@dataclass
class Player:
    """Represents a single player in the mahjong game."""
    position: int  # 0=East, 1=South, 2=West, 3=North
    hand: List[Tile] = field(default_factory=list)
    discards: List[Tile] = field(default_factory=list)
    melds: List[Meld] = field(default_factory=list)
    score: int = 25000  # Starting score
    is_riichi: bool = False
    riichi_turn: Optional[int] = None
    last_drawn_tile: Optional[Tile] = None  # Track the most recently drawn tile

    def draw_tile(self, tile: Tile) -> None:
        """
        Add a tile to the hand.

        Args:
            tile: The tile to draw
        """
        self.hand.append(tile)
        self.last_drawn_tile = tile

    def discard_tile(self, tile: Tile) -> bool:
        """
        Discard a tile from the hand.

        Args:
            tile: The tile to discard

        Returns:
            True if successful, False if tile not in hand
        """
        if tile in self.hand:
            self.hand.remove(tile)
            self.discards.append(tile)
            self.last_drawn_tile = None
            # Sort hand after discard
            self.sort_hand()
            return True
        return False

    def discard_by_index(self, index: int) -> Optional[Tile]:
        """
        Discard a tile from hand by index.

        Args:
            index: Index of the tile in hand

        Returns:
            The discarded tile, or None if index invalid
        """
        if 0 <= index < len(self.hand):
            tile = self.hand.pop(index)
            self.discards.append(tile)
            self.last_drawn_tile = None
            # Sort hand after discard
            self.sort_hand()
            return tile
        return None

    def sort_hand(self) -> None:
        """Sort the tiles in the hand."""
        self.hand = sort_tiles(self.hand)

    def can_declare_riichi(self) -> bool:
        """
        Check if player can declare riichi.
        Simplified check: must have 13 tiles and at least 1000 points.

        Returns:
            True if riichi can be declared
        """
        return (
            not self.is_riichi
            and len(self.hand) == 13
            and self.score >= 1000
            and len(self.melds) == 0  # No open melds
        )

    def declare_riichi(self, turn: int) -> bool:
        """
        Declare riichi.

        Args:
            turn: The turn number when riichi is declared

        Returns:
            True if successful
        """
        if self.can_declare_riichi():
            self.is_riichi = True
            self.riichi_turn = turn
            self.score -= 1000  # Pay riichi deposit
            return True
        return False

    def add_meld(self, meld: Meld) -> None:
        """
        Add a meld (pon/chi/kan) to the player.

        Args:
            meld: The meld to add
        """
        self.melds.append(meld)
        # Remove tiles from hand
        for tile in meld.tiles:
            if tile in self.hand:
                self.hand.remove(tile)
        self.last_drawn_tile = None

    @property
    def hand_size(self) -> int:
        """Get the current number of tiles in hand."""
        return len(self.hand)

    @property
    def total_tiles(self) -> int:
        """Get total tiles including melds."""
        return len(self.hand) + sum(len(m.tiles) for m in self.melds)

    @property
    def wind_name(self) -> str:
        """Get the wind name for this player's position."""
        winds = ["East", "South", "West", "North"]
        return winds[self.position]

    def __repr__(self) -> str:
        return (
            f"Player({self.wind_name}, "
            f"hand={len(self.hand)}, "
            f"discards={len(self.discards)}, "
            f"score={self.score})"
        )
