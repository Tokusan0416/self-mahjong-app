"""
Main game logic for Mahjong.
"""

from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime
import json

from .tiles import Tile, create_tile_pool, sort_tiles
from .player import Player, Meld
from .scoring import HandEvaluator


@dataclass
class GameAction:
    """Represents a single game action for logging."""
    turn: int
    player: int
    action_type: str  # "draw", "discard", "pon", "chi", "kan", "riichi", "tsumo", "ron"
    tile: Optional[str] = None
    tiles: Optional[List[str]] = None
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    metadata: Dict[str, Any] = field(default_factory=dict)


class MahjongGame:
    """Main game class managing the mahjong game state and flow."""

    def __init__(self):
        """Initialize a new game."""
        self.players: List[Player] = [Player(position=i) for i in range(4)]
        self.wall: List[Tile] = []
        self.dead_wall: List[Tile] = []  # Last 14 tiles (for dora and replacement)
        self.dora_indicators: List[Tile] = []
        self.current_player: int = 0
        self.turn_count: int = 0
        self.round_wind: int = 0  # 0=East, 1=South, 2=West, 3=North
        self.dealer: int = 0
        self.game_log: List[GameAction] = []
        self.is_game_over: bool = False
        self.winner: Optional[int] = None

    def start_new_round(self) -> None:
        """Start a new round of mahjong."""
        # Create and shuffle tile pool
        all_tiles = create_tile_pool()

        # Separate dead wall (last 14 tiles)
        self.wall = all_tiles[:-14]
        self.dead_wall = all_tiles[-14:]

        # Set dora indicator (5th tile from end of dead wall)
        self.dora_indicators = [self.dead_wall[4]]

        # Reset players
        for player in self.players:
            player.hand = []
            player.discards = []
            player.melds = []
            player.is_riichi = False
            player.riichi_turn = None

        # Deal initial tiles (13 tiles to each player)
        for _ in range(13):
            for player in self.players:
                if self.wall:
                    player.draw_tile(self.wall.pop(0))

        # Sort all hands
        for player in self.players:
            player.sort_hand()

        # Dealer (East) draws first tile
        if self.wall:
            self.players[self.dealer].draw_tile(self.wall.pop(0))

        self.current_player = self.dealer
        self.turn_count = 0
        self.is_game_over = False
        self.winner = None

        # Log game start
        self.log_action(
            player=-1,
            action_type="game_start",
            metadata={
                "dealer": self.dealer,
                "round_wind": self.round_wind,
            },
        )

    def draw_tile(self, player_idx: int) -> Optional[Tile]:
        """
        Draw a tile from the wall for the specified player.

        Args:
            player_idx: Index of the player drawing

        Returns:
            The drawn tile, or None if wall is empty
        """
        if not self.wall:
            return None

        tile = self.wall.pop(0)
        self.players[player_idx].draw_tile(tile)

        self.log_action(
            player=player_idx,
            action_type="draw",
            tile=str(tile),
        )

        return tile

    def discard_tile(self, player_idx: int, tile_idx: int) -> Optional[Tile]:
        """
        Player discards a tile by index.

        Args:
            player_idx: Index of the player
            tile_idx: Index of the tile in player's hand

        Returns:
            The discarded tile, or None if invalid
        """
        player = self.players[player_idx]
        tile = player.discard_by_index(tile_idx)

        if tile:
            self.log_action(
                player=player_idx,
                action_type="discard",
                tile=str(tile),
                metadata={"hand_size": len(player.hand)},
            )

            # Check for win (ron)
            for i, p in enumerate(self.players):
                if i != player_idx:
                    test_hand = p.hand + [tile]
                    if HandEvaluator.is_complete_hand(test_hand):
                        # Ron is possible
                        pass  # In actual game, would prompt for ron

            # Move to next player
            self.advance_turn()

        return tile

    def advance_turn(self) -> None:
        """Advance to the next player's turn."""
        self.current_player = (self.current_player + 1) % 4
        self.turn_count += 1

        # Draw tile for next player
        if self.wall:
            self.draw_tile(self.current_player)

    def check_win(self, player_idx: int, tile: Optional[Tile] = None) -> bool:
        """
        Check if player has won.

        Args:
            player_idx: Player to check
            tile: Optional winning tile (for ron)

        Returns:
            True if player has won
        """
        player = self.players[player_idx]
        hand = player.hand if tile is None else player.hand + [tile]

        if HandEvaluator.is_complete_hand(hand):
            self.winner = player_idx
            self.is_game_over = True

            self.log_action(
                player=player_idx,
                action_type="win",
                tile=str(tile) if tile else None,
                metadata={
                    "hand": [str(t) for t in player.hand],
                    "melds": [
                        {"type": m.type, "tiles": [str(t) for t in m.tiles]}
                        for m in player.melds
                    ],
                },
            )
            return True

        return False

    def check_tenpai(self, player_idx: int) -> List[Tile]:
        """
        Check which tiles the player is waiting for.

        Args:
            player_idx: Player to check

        Returns:
            List of waiting tiles
        """
        player = self.players[player_idx]
        return HandEvaluator.check_tenpai(player.hand)

    def declare_riichi(self, player_idx: int) -> bool:
        """
        Player declares riichi.

        Args:
            player_idx: Player declaring riichi

        Returns:
            True if successful
        """
        player = self.players[player_idx]

        if player.declare_riichi(self.turn_count):
            self.log_action(
                player=player_idx,
                action_type="riichi",
                metadata={"turn": self.turn_count},
            )
            return True

        return False

    def log_action(
        self,
        player: int,
        action_type: str,
        tile: Optional[str] = None,
        tiles: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Log a game action.

        Args:
            player: Player index (-1 for system actions)
            action_type: Type of action
            tile: Optional tile involved
            tiles: Optional list of tiles involved
            metadata: Optional additional data
        """
        action = GameAction(
            turn=self.turn_count,
            player=player,
            action_type=action_type,
            tile=tile,
            tiles=tiles,
            metadata=metadata or {},
        )
        self.game_log.append(action)

    def get_game_state(self) -> Dict[str, Any]:
        """
        Get current game state as dictionary.

        Returns:
            Dictionary containing complete game state
        """
        return {
            "current_player": self.current_player,
            "turn_count": self.turn_count,
            "dealer": self.dealer,
            "round_wind": self.round_wind,
            "wall_remaining": len(self.wall),
            "is_game_over": self.is_game_over,
            "winner": self.winner,
            "players": [
                {
                    "position": p.position,
                    "wind": p.wind_name,
                    "hand": [str(t) for t in p.hand],
                    "hand_size": len(p.hand),
                    "discards": [str(t) for t in p.discards],
                    "melds": [
                        {"type": m.type, "tiles": [str(t) for t in m.tiles]}
                        for m in p.melds
                    ],
                    "score": p.score,
                    "is_riichi": p.is_riichi,
                }
                for p in self.players
            ],
            "dora_indicators": [str(t) for t in self.dora_indicators],
        }

    def export_log_json(self) -> str:
        """
        Export game log as JSON string.

        Returns:
            JSON string of game log
        """
        log_data = {
            "game_state": self.get_game_state(),
            "actions": [
                {
                    "turn": a.turn,
                    "player": a.player,
                    "action_type": a.action_type,
                    "tile": a.tile,
                    "tiles": a.tiles,
                    "timestamp": a.timestamp,
                    "metadata": a.metadata,
                }
                for a in self.game_log
            ],
        }
        return json.dumps(log_data, indent=2, ensure_ascii=False)
