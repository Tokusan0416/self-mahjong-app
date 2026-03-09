"""
Tile definitions and operations for Japanese Mahjong.
"""

from enum import Enum
from dataclasses import dataclass
from typing import List
import random


class TileType(Enum):
    """Types of mahjong tiles."""
    MANZU = "m"  # 萬子 (characters)
    PINZU = "p"  # 筒子 (dots)
    SOUZU = "s"  # 索子 (bamboo)
    JIHAI = "z"  # 字牌 (honors: winds and dragons)


@dataclass
class Tile:
    """Represents a single mahjong tile."""
    type: TileType
    number: int  # 1-9 for suits, 1-7 for honors (1-4: winds, 5-7: dragons)

    def __str__(self) -> str:
        """String representation like '1m', '5p', '7z'."""
        return f"{self.number}{self.type.value}"

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other) -> bool:
        if not isinstance(other, Tile):
            return False
        return self.type == other.type and self.number == other.number

    def __hash__(self) -> int:
        return hash((self.type, self.number))

    @property
    def is_honor(self) -> bool:
        """Check if this is an honor tile (wind or dragon)."""
        return self.type == TileType.JIHAI

    @property
    def is_terminal(self) -> bool:
        """Check if this is a terminal (1 or 9 of a suit)."""
        return not self.is_honor and self.number in [1, 9]

    @property
    def is_simple(self) -> bool:
        """Check if this is a simple tile (2-8 of a suit)."""
        return not self.is_honor and 2 <= self.number <= 8

    @classmethod
    def from_string(cls, s: str) -> "Tile":
        """Create a tile from string representation like '1m', '5p', '7z'."""
        if len(s) != 2:
            raise ValueError(f"Invalid tile string: {s}")

        number = int(s[0])
        type_char = s[1]

        type_map = {t.value: t for t in TileType}
        if type_char not in type_map:
            raise ValueError(f"Invalid tile type: {type_char}")

        return cls(type=type_map[type_char], number=number)


def create_tile_pool() -> List[Tile]:
    """
    Create a complete pool of mahjong tiles (136 tiles total).
    Each tile appears 4 times.

    Returns:
        List of 136 tiles, shuffled
    """
    tiles = []

    # Add number tiles (萬子, 筒子, 索子)
    for tile_type in [TileType.MANZU, TileType.PINZU, TileType.SOUZU]:
        for number in range(1, 10):
            for _ in range(4):  # 4 copies of each tile
                tiles.append(Tile(type=tile_type, number=number))

    # Add honor tiles (字牌)
    # 1-4: East, South, West, North (winds)
    # 5-7: White, Green, Red (dragons)
    for number in range(1, 8):
        for _ in range(4):  # 4 copies of each honor
            tiles.append(Tile(type=TileType.JIHAI, number=number))

    # Shuffle the pool
    random.shuffle(tiles)

    return tiles


def sort_tiles(tiles: List[Tile]) -> List[Tile]:
    """
    Sort tiles in standard order (manzu, pinzu, souzu, honors).

    Args:
        tiles: List of tiles to sort

    Returns:
        Sorted list of tiles
    """
    type_order = {
        TileType.MANZU: 0,
        TileType.PINZU: 1,
        TileType.SOUZU: 2,
        TileType.JIHAI: 3,
    }

    return sorted(tiles, key=lambda t: (type_order[t.type], t.number))


def tiles_to_string(tiles: List[Tile]) -> str:
    """
    Convert list of tiles to compact string representation.
    Example: [1m, 2m, 3m, 5p] -> "1m 2m 3m 5p"
    """
    return " ".join(str(t) for t in tiles)


def string_to_tiles(s: str) -> List[Tile]:
    """
    Parse string representation to list of tiles.
    Example: "1m 2m 3m 5p" -> [1m, 2m, 3m, 5p]
    """
    if not s.strip():
        return []
    return [Tile.from_string(tile_str) for tile_str in s.split()]
