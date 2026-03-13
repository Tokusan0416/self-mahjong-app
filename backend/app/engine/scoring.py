"""
Hand evaluation and scoring for Japanese Mahjong.

Uses the 'mahjong' library for complete yaku evaluation and scoring.
"""

from typing import List, Dict, Tuple, Optional
from collections import Counter

try:
    from mahjong.hand_calculating.hand import HandCalculator
    from mahjong.tile import TilesConverter
    from mahjong.hand_calculating.hand_config import HandConfig
    from mahjong.meld import Meld as MahjongMeld
    from mahjong.constants import EAST, SOUTH, WEST, NORTH
    MAHJONG_LIB_AVAILABLE = True
except ImportError:
    MAHJONG_LIB_AVAILABLE = False
    print("Warning: mahjong library not available. Using simplified scoring.")

from .tiles import Tile, TileType
from .player import Player, Meld


def tile_to_136_array(tiles: List[Tile]) -> List[int]:
    """
    Convert our Tile objects to mahjong library's 136 tile format.

    Args:
        tiles: List of Tile objects

    Returns:
        List of tile indices (0-135)
    """
    result = []
    for tile in tiles:
        # Convert to mahjong library string format
        tile_str = str(tile)  # e.g., "1m", "5p", "7z"

        # Map to mahjong library format
        # Man: 0-35 (1m-9m, 4 copies each)
        # Pin: 36-71 (1p-9p, 4 copies each)
        # Sou: 72-107 (1s-9s, 4 copies each)
        # Honor: 108-135 (1z-7z, 4 copies each)

        if tile.type == TileType.MANZU:
            base = (tile.number - 1) * 4
        elif tile.type == TileType.PINZU:
            base = 36 + (tile.number - 1) * 4
        elif tile.type == TileType.SOUZU:
            base = 72 + (tile.number - 1) * 4
        else:  # JIHAI
            base = 108 + (tile.number - 1) * 4

        # For simplicity, use the first copy (base + 0)
        # In a real game, you'd track which specific copy
        result.append(base)

    return result


def tiles_to_34_array(tiles: List[Tile]) -> List[int]:
    """
    Convert our Tile objects to mahjong library's 34 tile type format.

    Args:
        tiles: List of Tile objects

    Returns:
        Array of 34 integers representing tile counts
    """
    result = [0] * 34

    for tile in tiles:
        if tile.type == TileType.MANZU:
            idx = tile.number - 1
        elif tile.type == TileType.PINZU:
            idx = 9 + tile.number - 1
        elif tile.type == TileType.SOUZU:
            idx = 18 + tile.number - 1
        else:  # JIHAI
            idx = 27 + tile.number - 1

        result[idx] += 1

    return result


class HandEvaluator:
    """Evaluates mahjong hands for winning conditions and scores."""

    @staticmethod
    def is_complete_hand(tiles: List[Tile]) -> bool:
        """
        Check if the hand is complete (ready to win).
        A complete hand has 14 tiles forming 4 melds + 1 pair.

        This is a simplified check. For full implementation,
        consider using the mahjong library.

        Args:
            tiles: List of tiles to check

        Returns:
            True if hand is complete
        """
        if len(tiles) != 14:
            return False

        # Try to find a valid hand structure
        return HandEvaluator._check_standard_form(tiles)

    @staticmethod
    def _check_standard_form(tiles: List[Tile]) -> bool:
        """
        Check if tiles form standard winning pattern (4 melds + 1 pair).
        This is a simplified implementation.

        Args:
            tiles: Sorted list of tiles

        Returns:
            True if valid winning hand
        """
        # Count tiles
        tile_counts = Counter(tiles)

        # Try each tile as the pair
        for pair_tile in tile_counts:
            if tile_counts[pair_tile] >= 2:
                # Remove pair
                remaining = tile_counts.copy()
                remaining[pair_tile] -= 2

                # Check if remaining tiles form 4 melds
                if HandEvaluator._check_melds(remaining, 4):
                    return True

        return False

    @staticmethod
    def _check_with_melds(tiles: List[Tile], num_remaining_melds: int) -> bool:
        """
        Check if tiles form a valid winning pattern with existing melds.

        Args:
            tiles: Remaining tiles in hand
            num_remaining_melds: Number of melds still needed (not including called melds)

        Returns:
            True if tiles can form required pattern
        """
        if len(tiles) != num_remaining_melds * 3 + 2:
            return False

        # Count tiles
        tile_counts = Counter(tiles)

        # Try each tile as the pair
        for pair_tile in tile_counts:
            if tile_counts[pair_tile] >= 2:
                # Remove pair
                remaining = tile_counts.copy()
                remaining[pair_tile] -= 2

                # Check if remaining tiles form required number of melds
                if HandEvaluator._check_melds(remaining, num_remaining_melds):
                    return True

        return False

    @staticmethod
    def _check_melds(tile_counts: Counter, num_melds: int) -> bool:
        """
        Recursively check if tiles can form required number of melds.

        Args:
            tile_counts: Counter of remaining tiles
            num_melds: Number of melds needed

        Returns:
            True if melds can be formed
        """
        if num_melds == 0:
            return all(count == 0 for count in tile_counts.values())

        # Get first tile
        for tile in sorted(tile_counts.keys(), key=lambda t: (t.type.value, t.number)):
            if tile_counts[tile] == 0:
                continue

            # Try as triplet (pon)
            if tile_counts[tile] >= 3:
                tile_counts[tile] -= 3
                if HandEvaluator._check_melds(tile_counts, num_melds - 1):
                    tile_counts[tile] += 3
                    return True
                tile_counts[tile] += 3

            # Try as sequence (chi) - only for number tiles
            if not tile.is_honor and tile.number <= 7:
                tile2 = Tile(tile.type, tile.number + 1)
                tile3 = Tile(tile.type, tile.number + 2)

                if tile_counts.get(tile2, 0) > 0 and tile_counts.get(tile3, 0) > 0:
                    tile_counts[tile] -= 1
                    tile_counts[tile2] -= 1
                    tile_counts[tile3] -= 1

                    if HandEvaluator._check_melds(tile_counts, num_melds - 1):
                        tile_counts[tile] += 1
                        tile_counts[tile2] += 1
                        tile_counts[tile3] += 1
                        return True

                    tile_counts[tile] += 1
                    tile_counts[tile2] += 1
                    tile_counts[tile3] += 1

            # If we can't form a meld with this tile, fail
            break

        return False

    @staticmethod
    def check_tenpai(tiles: List[Tile]) -> List[Tile]:
        """
        Check which tiles would complete the hand (tenpai check).

        Args:
            tiles: Current hand (should be 13 tiles)

        Returns:
            List of tiles that would complete the hand
        """
        if len(tiles) != 13:
            return []

        waiting_tiles = []

        # Try adding each possible tile
        all_possible_tiles = set()
        for tile_type in TileType:
            if tile_type == TileType.JIHAI:
                for num in range(1, 8):
                    all_possible_tiles.add(Tile(tile_type, num))
            else:
                for num in range(1, 10):
                    all_possible_tiles.add(Tile(tile_type, num))

        for test_tile in all_possible_tiles:
            test_hand = tiles + [test_tile]
            if HandEvaluator.is_complete_hand(test_hand):
                waiting_tiles.append(test_tile)

        return waiting_tiles

    @staticmethod
    def calculate_basic_score(
        player: Player, winning_tile: Tile, is_tsumo: bool = False, player_wind: int = 0, round_wind: int = 0
    ) -> Dict[str, any]:
        """
        Calculate score for a winning hand using mahjong library.

        Args:
            player: The winning player
            winning_tile: The tile that completed the hand
            is_tsumo: True if self-drawn win
            player_wind: Player's seat wind (0=East, 1=South, 2=West, 3=North)
            round_wind: Round wind (0=East, 1=South, etc.)

        Returns:
            Dictionary with score information
        """
        if not MAHJONG_LIB_AVAILABLE:
            # Fallback to simple scoring
            result = {
                "han": 1,
                "fu": 30,
                "points": 1000,
                "yaku": ["Simplified scoring (mahjong library not available)"],
                "is_tsumo": is_tsumo,
                "yaku_list": [],
            }
            if player.is_riichi:
                result["han"] += 1
                result["yaku"].append("Riichi")
                result["points"] += 1000
            return result

        try:
            # Convert tiles to mahjong library format
            hand_tiles = tiles_to_34_array(player.hand)

            # Find which tile is the winning tile
            win_tile_136 = tile_to_136_array([winning_tile])[0]

            # Configure hand calculation
            config = HandConfig(
                is_tsumo=is_tsumo,
                is_riichi=player.is_riichi,
                player_wind=player_wind,
                round_wind=round_wind,
                is_dealer=(player_wind == 0),
            )

            # Convert melds if any
            melds = []
            # TODO: Convert player.melds to mahjong library Meld format when implementing naki

            # Calculate hand value
            calculator = HandCalculator()
            result_calc = calculator.estimate_hand_value(
                hand_tiles,
                win_tile_136 // 4,  # Convert to 34 format
                melds=melds,
                config=config,
            )

            if result_calc.error:
                # No valid yaku
                return {
                    "han": 0,
                    "fu": 0,
                    "points": 0,
                    "yaku": ["No yaku (chombo)"],
                    "is_tsumo": is_tsumo,
                    "yaku_list": [],
                    "error": result_calc.error,
                }

            # Extract yaku names
            yaku_names = [yaku.name for yaku in result_calc.yaku] if result_calc.yaku else []

            return {
                "han": result_calc.han,
                "fu": result_calc.fu,
                "points": result_calc.cost.get("main", 0) if result_calc.cost else 0,
                "yaku": yaku_names,
                "is_tsumo": is_tsumo,
                "yaku_list": result_calc.yaku if result_calc.yaku else [],
                "cost": result_calc.cost,
            }

        except Exception as e:
            # Fallback on error
            print(f"Error calculating score: {e}")
            return {
                "han": 1,
                "fu": 30,
                "points": 1000,
                "yaku": ["Error in score calculation"],
                "is_tsumo": is_tsumo,
                "yaku_list": [],
                "error": str(e),
            }

    @staticmethod
    def get_yaku_name(hand: List[Tile], melds: List[Meld]) -> List[str]:
        """
        Get list of yaku (winning hands) names.
        This is a placeholder for full yaku detection.

        Args:
            hand: Player's concealed tiles
            melds: Player's open melds

        Returns:
            List of yaku names
        """
        # TODO: Implement full yaku detection
        # For now, return placeholder
        return ["TODO: Full yaku detection"]
