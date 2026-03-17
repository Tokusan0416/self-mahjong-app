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
                    'melds': [
                        {
                            'type': m.type,
                            'tiles': [str(t) for t in m.tiles],
                            'from_player': m.from_player,
                        }
                        for m in p.melds
                    ],
                    'score': p.score,
                    'is_riichi': p.is_riichi,
                    'last_drawn_tile': str(p.last_drawn_tile) if (p.last_drawn_tile and i == self.game.current_player) else '',
                    'riichi_turn': p.riichi_turn,
                }
                for i, p in enumerate(self.game.players)
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

        from app.engine.tiles import Tile

        # Convert string to Tile object
        tile_obj = Tile.from_string(tile)

        player = self.game.players[player_idx]

        # Discard the tile
        success = player.discard_tile(tile_obj)

        if not success:
            raise ValueError(f"Player {player_idx} cannot discard tile {tile} - tile not in hand")

        # Update game state for last discard tracking
        self.game.last_discard = tile_obj
        self.game.last_discard_player = player_idx

        # Log the action
        self.game.log_action(
            player=player_idx,
            action_type="discard",
            tile=str(tile_obj),
            metadata={"is_drawn": is_drawn, "hand_size": len(player.hand)},
        )

        # Check if any player can make a call (Ron, Pon, Chi, Kan)
        can_call = False
        for i in range(4):
            if i == player_idx:
                continue
            if (self._can_declare_ron(i) or self._can_declare_pon(i) or
                self._can_declare_chi(i) or self._can_declare_kan(i)):
                can_call = True
                break

        # If no one can make a call, automatically advance to next player
        if not can_call:
            self.game.advance_turn()

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

        from app.engine.scoring import HandEvaluator

        player = self.game.players[player_idx]
        winning_tile = player.hand[-1] if player.hand else None

        # Calculate score info before declaring (for response)
        score_info = HandEvaluator.calculate_basic_score(
            player,
            winning_tile,
            is_tsumo=True,
            player_wind=player.position,
            round_wind=self.game.round_wind,
        )

        success = self.game.declare_tsumo(player_idx)
        if not success:
            raise ValueError(f"Player {player_idx} cannot declare tsumo")

        state = self.get_game_state()
        state['win_info'] = {
            'winner': player_idx,
            'win_type': 'tsumo',
            'winning_tile': str(winning_tile) if winning_tile else None,
            'hand': [str(t) for t in player.hand],
            'score_info': score_info,
        }
        return state

    def declare_ron(self, player_idx: int) -> Dict[str, Any]:
        """Declare ron win."""
        if not self.game:
            raise ValueError("No active game")

        from app.engine.scoring import HandEvaluator

        player = self.game.players[player_idx]
        winning_tile = self.game.last_discard

        # Calculate score info before declaring (for response)
        score_info = HandEvaluator.calculate_basic_score(
            player,
            winning_tile,
            is_tsumo=False,
            player_wind=player.position,
            round_wind=self.game.round_wind,
        )

        success = self.game.declare_ron(player_idx)
        if not success:
            raise ValueError(f"Player {player_idx} cannot declare ron")

        state = self.get_game_state()
        state['win_info'] = {
            'winner': player_idx,
            'win_type': 'ron',
            'winning_tile': str(winning_tile) if winning_tile else None,
            'loser': self.game.last_discard_player,
            'hand': [str(t) for t in player.hand],
            'score_info': score_info,
        }
        return state

    def declare_pon(self, player_idx: int, tile: str) -> Dict[str, Any]:
        """Declare pon."""
        if not self.game:
            raise ValueError("No active game")

        # Engine's declare_pon only needs player_idx (uses last_discard implicitly)
        success = self.game.declare_pon(player_idx)
        if not success:
            raise ValueError(f"Player {player_idx} cannot declare pon")
        return self.get_game_state()

    def declare_chi(self, player_idx: int, tile: str, pattern: List[str]) -> Dict[str, Any]:
        """Declare chi."""
        if not self.game:
            raise ValueError("No active game")

        from app.engine.tiles import Tile

        # Convert pattern strings to Tile objects
        if pattern:
            tile_pattern = [Tile.from_string(t) for t in pattern]
        else:
            # If no pattern specified, get the first valid chi pattern
            possible_chis = self.game.check_chi(player_idx)
            if not possible_chis:
                raise ValueError(f"Player {player_idx} cannot declare chi")
            tile_pattern = possible_chis[0]

        success = self.game.declare_chi(player_idx, tile_pattern)
        if not success:
            raise ValueError(f"Player {player_idx} cannot declare chi with pattern {pattern}")
        return self.get_game_state()

    def declare_kan(self, player_idx: int, tile: str) -> Dict[str, Any]:
        """Declare kan."""
        if not self.game:
            raise ValueError("No active game")

        from app.engine.tiles import Tile

        # Convert tile string to Tile object
        tile_obj = Tile.from_string(tile)

        # Check what type of kan this is
        # For now, assume it's a daiminkan (adding to last discard)
        # In a full implementation, you'd need to check if it's ankan or shouminkan
        kan_type = "daiminkan"

        success = self.game.declare_kan(player_idx, kan_type, tile_obj)
        if not success:
            raise ValueError(f"Player {player_idx} cannot declare kan")
        return self.get_game_state()

    def pass_on_calls(self) -> Dict[str, Any]:
        """Pass on all call opportunities."""
        if not self.game:
            raise ValueError("No active game")

        # Clear last discard and advance to next player
        self.game.last_discard = None
        self.game.last_discard_player = None
        self.game.advance_turn()
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
        return self.game.check_ron(player_idx)

    def _can_declare_pon(self, player_idx: int) -> bool:
        """Check if player can declare pon."""
        if not self.game or not self.game.last_discard:
            return False
        return self.game.check_pon(player_idx)

    def _can_declare_chi(self, player_idx: int) -> bool:
        """Check if player can declare chi."""
        if not self.game or not self.game.last_discard:
            return False
        chi_patterns = self.game.check_chi(player_idx)
        return len(chi_patterns) > 0

    def _can_declare_kan(self, player_idx: int) -> bool:
        """Check if player can declare kan."""
        if not self.game:
            return False
        kan_options = self.game.check_kan(player_idx)
        # Check if any kan type is available
        return any(len(tiles) > 0 for tiles in kan_options.values())

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
