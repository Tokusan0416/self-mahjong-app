"""
Hand evaluation and scoring for Japanese Mahjong.

Note: This is a simplified implementation. For production use,
consider using the 'mahjong' library for complete yaku evaluation.
"""

from typing import List, Dict, Tuple, Optional
from collections import Counter
from .tiles import Tile, TileType
from .player import Player, Meld


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
        player: Player, winning_tile: Tile, is_tsumo: bool = False
    ) -> Dict[str, any]:
        """
        Calculate basic score for a winning hand.
        This is a simplified implementation.

        Args:
            player: The winning player
            winning_tile: The tile that completed the hand
            is_tsumo: True if self-drawn win

        Returns:
            Dictionary with score information
        """
        # This is a placeholder for basic scoring
        # Full implementation would check for all yaku and calculate han/fu

        result = {
            "han": 1,  # Basic 1 han for now
            "fu": 30,  # Basic fu
            "points": 1000,  # Simplified point calculation
            "yaku": ["Simplified scoring - TODO: Implement full yaku"],
            "is_tsumo": is_tsumo,
        }

        # Add riichi bonus
        if player.is_riichi:
            result["han"] += 1
            result["yaku"].append("Riichi")
            result["points"] += 1000

        return result

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
