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
    player_melds: List[List[str]] = [[], [], [], []]  # Melds as strings for each player

    # Board info
    dora_indicators: List[str] = []

    # UI state
    info_message: str = ""
    waiting_tiles: List[str] = []

    # Call availability (for showing buttons)
    can_ron: List[bool] = [False, False, False, False]  # Which players can ron
    can_tsumo: bool = False  # Current player can tsumo
    can_pon: List[bool] = [False, False, False, False]  # Which players can pon
    can_chi: List[bool] = [False, False, False, False]  # Which players can chi
    can_kan: List[bool] = [False, False, False, False]  # Which players can kan (daiminkan)

    # Win information (for display)
    last_win_info: Dict[str, Any] = {}

    def start_new_game(self):
        """Start a new game."""
        self._game = MahjongGame()
        self._game.start_new_round()
        self._sync_state()
        self.info_message = "New game started! East player's turn."
        self.waiting_tiles = []
        self.can_ron = [False, False, False, False]
        # Check if dealer can immediately tsumo (rare but possible)
        self.can_tsumo = self._game.check_tsumo(self._game.current_player)

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
            player_names = ["East", "South", "West", "North"]

            # Priority: Ron > Kan > Pon > Chi

            # Check for ron possibilities
            ron_players = self._game.check_all_ron()

            # Check for kan possibilities (daiminkan)
            kan_players = []
            for i in range(4):
                if i != player_idx:
                    kan_options = self._game.check_kan(i)
                    if kan_options.get("daiminkan"):
                        kan_players.append(i)

            # Check for pon possibilities
            pon_players = []
            for i in range(4):
                if i != player_idx and self._game.check_pon(i):
                    pon_players.append(i)

            # Check for chi possibilities (only next player)
            chi_players = []
            next_player = (player_idx + 1) % 4
            chi_patterns = self._game.check_chi(next_player)
            if chi_patterns:
                chi_players.append(next_player)

            # Update call availability flags
            for i in range(4):
                self.can_ron[i] = i in ron_players
                self.can_pon[i] = i in pon_players
                self.can_chi[i] = i in chi_players
                self.can_kan[i] = i in kan_players

            # If any calls are available, don't advance turn yet
            if ron_players or kan_players or pon_players or chi_players:
                call_names = []
                if ron_players:
                    call_names.append(f"Ron: {', '.join([player_names[i] for i in ron_players])}")
                if kan_players:
                    call_names.append(f"Kan: {', '.join([player_names[i] for i in kan_players])}")
                if pon_players:
                    call_names.append(f"Pon: {', '.join([player_names[i] for i in pon_players])}")
                if chi_players:
                    call_names.append(f"Chi: {', '.join([player_names[i] for i in chi_players])}")

                self.info_message = (
                    f"{player_names[player_idx]} discarded {tile}. "
                    f"Calls available: {' | '.join(call_names)}"
                )
            else:
                # No calls, advance turn normally
                self.can_ron = [False, False, False, False]
                self.can_pon = [False, False, False, False]
                self.can_chi = [False, False, False, False]
                self.can_kan = [False, False, False, False]

                self._game.advance_turn()
                self._sync_state()

                # Check if current player can tsumo
                self.can_tsumo = self._game.check_tsumo(self._game.current_player)

                next_player = self._game.current_player
                self.info_message = (
                    f"{player_names[player_idx]} discarded {tile}. "
                    f"Now {player_names[next_player]}'s turn."
                )

                # Check if game is over (wall empty)
                if self.wall_remaining == 0 and not self.is_game_over:
                    self.info_message = "Wall is empty. Game ends in draw."
                    self.is_game_over = True

            self._sync_state()
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

    def declare_ron(self, player_idx: int):
        """
        Declare ron for the specified player.

        Args:
            player_idx: Player declaring ron (0-3)
        """
        if self.is_game_over:
            self.info_message = "Game is over."
            return

        if not self.can_ron[player_idx]:
            self.info_message = "Ron not available for this player."
            return

        player_names = ["East", "South", "West", "North"]

        if self._game.declare_ron(player_idx):
            # Get score info from game log
            last_action = self._game.game_log[-1] if self._game.game_log else None
            if last_action and "score_info" in last_action.metadata:
                self.last_win_info = last_action.metadata["score_info"]
            else:
                self.last_win_info = {}

            self._sync_state()
            self.can_ron = [False, False, False, False]
            self.can_tsumo = False

            # Create detailed win message
            score_info = self.last_win_info
            han = score_info.get("han", 0)
            fu = score_info.get("fu", 0)
            points = score_info.get("points", 0)
            yaku = score_info.get("yaku", [])

            yaku_str = ", ".join(yaku) if yaku else "No yaku"
            self.info_message = (
                f"🎉 {player_names[player_idx]} wins by Ron! "
                f"{han} han, {fu} fu = {points} points. Yaku: {yaku_str}"
            )
        else:
            self.info_message = "Ron declaration failed."

    def pass_on_ron(self):
        """Pass on all call opportunities and advance the turn."""
        if self.is_game_over:
            return

        # Clear all call flags and advance turn
        self.can_ron = [False, False, False, False]
        self.can_pon = [False, False, False, False]
        self.can_chi = [False, False, False, False]
        self.can_kan = [False, False, False, False]

        self._game.advance_turn()
        self._sync_state()

        # Check if current player can tsumo
        self.can_tsumo = self._game.check_tsumo(self._game.current_player)

        player_names = ["East", "South", "West", "North"]
        self.info_message = f"All calls passed. Now {player_names[self._game.current_player]}'s turn."

    def declare_pon(self, player_idx: int):
        """
        Declare pon for the specified player.

        Args:
            player_idx: Player declaring pon (0-3)
        """
        if self.is_game_over:
            self.info_message = "Game is over."
            return

        if not self.can_pon[player_idx]:
            self.info_message = "Pon not available for this player."
            return

        player_names = ["East", "South", "West", "North"]

        if self._game.declare_pon(player_idx):
            self._sync_state()
            # Clear all call flags
            self.can_ron = [False, False, False, False]
            self.can_pon = [False, False, False, False]
            self.can_chi = [False, False, False, False]
            self.can_kan = [False, False, False, False]
            self.can_tsumo = False

            self.info_message = f"{player_names[player_idx]} called Pon! Now discard a tile."
        else:
            self.info_message = "Pon declaration failed."

    def declare_chi(self, player_idx: int, pattern_index: int = 0):
        """
        Declare chi for the specified player.

        Args:
            player_idx: Player declaring chi (0-3)
            pattern_index: Index of the chi pattern to use (if multiple options)
        """
        if self.is_game_over:
            self.info_message = "Game is over."
            return

        if not self.can_chi[player_idx]:
            self.info_message = "Chi not available for this player."
            return

        player_names = ["East", "South", "West", "North"]

        # Get possible patterns
        chi_patterns = self._game.check_chi(player_idx)
        if not chi_patterns or pattern_index >= len(chi_patterns):
            self.info_message = "Invalid chi pattern."
            return

        # Use first pattern for now (TODO: Allow user to select pattern)
        selected_pattern = chi_patterns[pattern_index]

        if self._game.declare_chi(player_idx, selected_pattern):
            self._sync_state()
            # Clear all call flags
            self.can_ron = [False, False, False, False]
            self.can_pon = [False, False, False, False]
            self.can_chi = [False, False, False, False]
            self.can_kan = [False, False, False, False]
            self.can_tsumo = False

            self.info_message = f"{player_names[player_idx]} called Chi! Now discard a tile."
        else:
            self.info_message = "Chi declaration failed."

    def declare_tsumo(self):
        """Declare tsumo for the current player."""
        if self.is_game_over:
            self.info_message = "Game is over."
            return

        current = self._game.current_player
        player_names = ["East", "South", "West", "North"]

        if self._game.declare_tsumo(current):
            # Get score info from game log
            last_action = self._game.game_log[-1] if self._game.game_log else None
            if last_action and "score_info" in last_action.metadata:
                self.last_win_info = last_action.metadata["score_info"]
            else:
                self.last_win_info = {}

            self._sync_state()
            self.can_tsumo = False
            self.can_ron = [False, False, False, False]

            # Create detailed win message
            score_info = self.last_win_info
            han = score_info.get("han", 0)
            fu = score_info.get("fu", 0)
            points = score_info.get("points", 0)
            yaku = score_info.get("yaku", [])

            yaku_str = ", ".join(yaku) if yaku else "No yaku"
            self.info_message = (
                f"🎉 {player_names[current]} wins by Tsumo! "
                f"{han} han, {fu} fu = {points} points. Yaku: {yaku_str}"
            )
        else:
            self.info_message = "Tsumo not available."

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

            # Convert melds to displayable strings
            meld_strings = []
            for meld in player_data["melds"]:
                meld_type = meld["type"].upper()
                tiles_str = " ".join(meld["tiles"])
                meld_strings.append(f"{meld_type}: {tiles_str}")
            self.player_melds[i] = meld_strings

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
