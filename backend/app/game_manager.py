"""Game state manager - bridges Flask routes and game engine."""
from app.engine.game import MahjongGame
from typing import Optional, Dict, List, Any


class GameManager:
    """Manages game instance and provides serializable state."""

    def __init__(self):
        """Initialize game manager."""
        self.game: Optional[MahjongGame] = None
        self.player_names = ["East", "South", "West", "North"]

    def start_new_game(self, game_type: str = 'hanchan') -> Dict[str, Any]:
        """
        Start new game and return initial state.

        Args:
            game_type: Type of game ('hanchan' or 'tonpuu')

        Returns:
            Initial game state dictionary
        """
        # MahjongGame constructor already initializes the game
        self.game = MahjongGame(game_type=game_type)
        # Start the first round
        self.game.start_new_round()
        return self.get_game_state()

    def get_game_state(self) -> Optional[Dict[str, Any]]:
        """
        Get serializable game state.

        Returns:
            Current game state or None if no game active
        """
        if not self.game:
            return None

        return {
            'players': [
                {
                    'hand': [str(t) for t in p.hand],
                    'discards': [str(t) for t in p.discards],
                    'melds': p.melds,  # Already strings
                    'score': p.score,
                    'is_riichi': p.is_riichi,
                    'last_drawn_tile': str(p.last_drawn_tile) if p.last_drawn_tile else '',
                    'riichi_turn': p.riichi_turn,
                }
                for p in self.game.players
            ],
            'player_names': self.player_names,
            'current_player': self.game.current_player,
            'wall_remaining': len(self.game.wall),
            'dora_indicators': [str(d) for d in self.game.dora_indicators],
            'round_wind': self.game.round_wind,
            'round_number': self.game.round_number,
            'honba_sticks': self.game.honba_sticks,
            'riichi_sticks': self.game.riichi_sticks,
            'game_type': self.game.game_type,
            'dealer': self.game.dealer,
            'turn_count': self.game.turn_count,
            'is_game_over': self.game.is_game_over,
            'is_exhaustive_draw': getattr(self.game, 'is_exhaustive_draw', False),
            'last_discard': str(self.game.last_discard) if self.game.last_discard else None,
            'last_discard_player': self.game.last_discard_player,
            # Call availability
            'can_ron': [self._can_declare_ron(i) for i in range(4)],
            'can_pon': [self._can_declare_pon(i) for i in range(4)],
            'can_chi': [self._can_declare_chi(i) for i in range(4)],
            'can_kan': [self._can_declare_kan(i) for i in range(4)],
            'can_tsumo': self._can_declare_tsumo(self.game.current_player) if self.game.players[self.game.current_player].last_drawn_tile else False,
        }

    def discard_tile(self, player_idx: int, tile: str, is_drawn: bool) -> Dict[str, Any]:
        """
        Discard a tile.

        Args:
            player_idx: Index of player discarding
            tile: Tile code to discard
            is_drawn: Whether discarding the drawn tile

        Returns:
            Updated game state
        """
        if not self.game:
            raise ValueError("No active game")

        # MahjongGame.discard_tile takes (tile, is_drawn) - player_idx is implicitly current_player
        self.game.discard_tile(tile, is_drawn)
        return self.get_game_state()

    def declare_riichi(self, player_idx: int) -> Dict[str, Any]:
        """Declare riichi for player."""
        if not self.game:
            raise ValueError("No active game")

        self.game.declare_riichi(player_idx)
        return self.get_game_state()

    def declare_tsumo(self, player_idx: int) -> Dict[str, Any]:
        """Declare tsumo win."""
        if not self.game:
            raise ValueError("No active game")

        win_info = self.game.declare_tsumo(player_idx)
        state = self.get_game_state()
        state['win_info'] = win_info
        return state

    def declare_ron(self, player_idx: int) -> Dict[str, Any]:
        """Declare ron win."""
        if not self.game:
            raise ValueError("No active game")

        win_info = self.game.declare_ron(player_idx)
        state = self.get_game_state()
        state['win_info'] = win_info
        return state

    def declare_pon(self, player_idx: int, tile: str) -> Dict[str, Any]:
        """Declare pon."""
        if not self.game:
            raise ValueError("No active game")

        self.game.declare_pon(player_idx, tile)
        return self.get_game_state()

    def declare_chi(self, player_idx: int, tile: str, pattern: List[str]) -> Dict[str, Any]:
        """Declare chi."""
        if not self.game:
            raise ValueError("No active game")

        self.game.declare_chi(player_idx, tile, pattern)
        return self.get_game_state()

    def declare_kan(self, player_idx: int, tile: str) -> Dict[str, Any]:
        """Declare kan."""
        if not self.game:
            raise ValueError("No active game")

        self.game.declare_kan(player_idx, tile)
        return self.get_game_state()

    def pass_on_calls(self) -> Dict[str, Any]:
        """Pass on all call opportunities."""
        if not self.game:
            raise ValueError("No active game")

        self.game.pass_on_ron()
        return self.get_game_state()

    def check_tenpai(self, player_idx: int) -> Dict[str, Any]:
        """
        Check tenpai status for player.

        Returns:
            Dict with is_tenpai and waiting_tiles
        """
        if not self.game:
            raise ValueError("No active game")

        player = self.game.players[player_idx]
        is_tenpai, waiting_tiles = self.game.check_tenpai(player.hand, player.melds)

        return {
            'is_tenpai': is_tenpai,
            'waiting_tiles': waiting_tiles
        }

    def continue_after_exhaustive_draw(self) -> Dict[str, Any]:
        """Continue to next round after exhaustive draw."""
        if not self.game:
            raise ValueError("No active game")

        self.game.continue_after_exhaustive_draw()
        return self.get_game_state()

    # Helper methods for call availability
    def _can_declare_ron(self, player_idx: int) -> bool:
        """Check if player can declare ron."""
        if not self.game or not self.game.last_discard:
            return False
        return self.game.check_ron(player_idx, self.game.last_discard)

    def _can_declare_pon(self, player_idx: int) -> bool:
        """Check if player can declare pon."""
        if not self.game or not self.game.last_discard or player_idx == self.game.last_discard_player:
            return False
        player = self.game.players[player_idx]
        return player.hand.count(self.game.last_discard) >= 2

    def _can_declare_chi(self, player_idx: int) -> bool:
        """Check if player can declare chi."""
        if not self.game or not self.game.last_discard:
            return False
        # Chi only from previous player
        if (self.game.last_discard_player + 1) % 4 != player_idx:
            return False
        return len(self.game.get_chi_patterns(player_idx, self.game.last_discard)) > 0

    def _can_declare_kan(self, player_idx: int) -> bool:
        """Check if player can declare kan."""
        if not self.game or not self.game.last_discard or player_idx == self.game.last_discard_player:
            return False
        player = self.game.players[player_idx]
        return player.hand.count(self.game.last_discard) >= 3

    def _can_declare_tsumo(self, player_idx: int) -> bool:
        """Check if player can declare tsumo."""
        if not self.game or player_idx != self.game.current_player:
            return False
        player = self.game.players[player_idx]
        if not player.last_drawn_tile:
            return False
        return self.game.check_tsumo(player_idx)


# Global game manager instance
game_manager = GameManager()
