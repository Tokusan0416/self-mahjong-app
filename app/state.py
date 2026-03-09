"""
Reflex state management for the Mahjong application.
"""

import reflex as rx
from typing import List, Dict, Any
from .engine.game import MahjongGame


class MahjongState(rx.State):
    """State management for the Mahjong game."""

    # Game instance (not directly rendered)
    _game: MahjongGame = MahjongGame()

    # Rendered state (synced with game)
    current_player: int = 0
    turn_count: int = 0
    wall_remaining: int = 0
    is_game_over: bool = False
    winner: int = -1

    # Player data (4 players)
    player_hands: List[List[str]] = [[], [], [], []]
    player_discards: List[List[str]] = [[], [], [], []]
    player_scores: List[int] = [25000, 25000, 25000, 25000]
    player_riichi: List[bool] = [False, False, False, False]

    # Board info
    dora_indicators: List[str] = []

    # UI state
    info_message: str = ""
    waiting_tiles: List[str] = []

    def start_new_game(self):
        """Start a new game."""
        self._game = MahjongGame()
        self._game.start_new_round()
        self._sync_state()
        self.info_message = "New game started! East player's turn."
        self.waiting_tiles = []

    def discard_tile(self, player_idx: int, tile_str: str):
        """
        Discard a tile from specified player's hand.

        Args:
            player_idx: Index of the player (0-3)
            tile_str: String representation of tile (e.g. "1m")
        """
        if self.is_game_over:
            self.info_message = "Game is over. Start a new game."
            return

        # Check if it's this player's turn
        if player_idx != self._game.current_player:
            self.info_message = "Not your turn!"
            return

        # Find the index of this tile in the player's hand
        try:
            tile_index = self.player_hands[player_idx].index(tile_str)
        except ValueError:
            self.info_message = "Tile not in hand!"
            return

        tile = self._game.discard_tile(player_idx, tile_index)

        if tile:
            self._sync_state()
            next_player = self._game.current_player
            player_names = ["East", "South", "West", "North"]
            self.info_message = (
                f"{player_names[player_idx]} discarded {tile}. "
                f"Now {player_names[next_player]}'s turn."
            )

            # Check if game is over (wall empty)
            if self.wall_remaining == 0 and not self.is_game_over:
                self.info_message = "Wall is empty. Game ends in draw."
                self.is_game_over = True
        else:
            self.info_message = "Invalid tile selection."

    def check_current_tenpai(self):
        """Check what tiles the current player is waiting for."""
        if self.is_game_over:
            self.info_message = "Game is over."
            return

        current = self._game.current_player
        waiting = self._game.check_tenpai(current)

        if waiting:
            self.waiting_tiles = [str(t) for t in waiting]
            self.info_message = f"In tenpai! Waiting for {len(waiting)} tile(s)."
        else:
            self.waiting_tiles = []
            self.info_message = "Not in tenpai yet."

    def declare_riichi(self):
        """Declare riichi for the current player."""
        if self.is_game_over:
            self.info_message = "Game is over."
            return

        current = self._game.current_player
        player_names = ["East", "South", "West", "North"]

        # Check tenpai first
        waiting = self._game.check_tenpai(current)
        if not waiting:
            self.info_message = "Cannot declare riichi: not in tenpai."
            return

        # Try to declare
        if self._game.declare_riichi(current):
            self._sync_state()
            self.info_message = f"{player_names[current]} declared Riichi!"
        else:
            self.info_message = "Cannot declare riichi (need 13 tiles and 1000+ points)."

    def check_win(self):
        """Check if current player has won."""
        if self.is_game_over:
            return

        current = self._game.current_player
        if self._game.check_win(current):
            self._sync_state()
            player_names = ["East", "South", "West", "North"]
            self.info_message = f"{player_names[current]} wins! (Tsumo)"

    def export_log(self):
        """Export game log as JSON."""
        log_json = self._game.export_log_json()
        self.info_message = "Game log exported (check console/logs)"
        # In a real app, this would save to file or send to BigQuery
        print("=== GAME LOG ===")
        print(log_json)
        print("=== END LOG ===")

    def _sync_state(self):
        """Sync Reflex state with game engine state."""
        game_state = self._game.get_game_state()

        self.current_player = game_state["current_player"]
        self.turn_count = game_state["turn_count"]
        self.wall_remaining = game_state["wall_remaining"]
        self.is_game_over = game_state["is_game_over"]
        self.winner = game_state["winner"] if game_state["winner"] is not None else -1

        # Sync player data
        for i, player_data in enumerate(game_state["players"]):
            self.player_hands[i] = player_data["hand"]
            self.player_discards[i] = player_data["discards"]
            self.player_scores[i] = player_data["score"]
            self.player_riichi[i] = player_data["is_riichi"]

        self.dora_indicators = game_state["dora_indicators"]

    @rx.var
    def player_names(self) -> List[str]:
        """Get player names with wind positions."""
        names = ["East", "South", "West", "North"]
        return [
            f"{names[i]} ({self.player_scores[i]})" + (" [RIICHI]" if self.player_riichi[i] else "")
            for i in range(4)
        ]

    @rx.var
    def current_player_name(self) -> str:
        """Get the current player's name."""
        names = ["East", "South", "West", "North"]
        return names[self.current_player]
