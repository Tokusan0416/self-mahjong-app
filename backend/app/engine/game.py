"""
Main game logic for Mahjong.
"""

from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime
from collections import Counter
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

    def __init__(self, game_type: str = "hanchan"):
        """
        Initialize a new game.

        Args:
            game_type: "hanchan" (半荘, default) or "tonpuu" (東風戦)
        """
        self.players: List[Player] = [Player(position=i) for i in range(4)]
        self.wall: List[Tile] = []
        self.dead_wall: List[Tile] = []  # Last 14 tiles (for dora and replacement)
        self.dora_indicators: List[Tile] = []
        self.current_player: int = 0
        self.turn_count: int = 0
        self.round_wind: int = 0  # 0=East, 1=South (for hanchan), 2=West, 3=North
        self.round_number: int = 0  # 0-3 for rounds within a wind
        self.dealer: int = 0
        self.honba_sticks: int = 0  # 本場（連荘カウント）
        self.riichi_sticks: int = 0  # 立直棒の数
        self.game_type: str = game_type  # "hanchan" or "tonpuu"
        self.game_log: List[GameAction] = []
        self.is_game_over: bool = False
        self.winner: Optional[int] = None
        self.last_discard: Optional[Tile] = None  # Track last discarded tile for ron
        self.last_discard_player: Optional[int] = None  # Who discarded it
        self.pending_calls: List[Dict[str, Any]] = []  # Pending meld/ron calls

        # Exhaustive draw state
        self.is_exhaustive_draw: bool = False
        self.tenpai_players: List[int] = []  # Players in tenpai during exhaustive draw

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
            # Store last discard for ron/meld calls
            self.last_discard = tile
            self.last_discard_player = player_idx

            self.log_action(
                player=player_idx,
                action_type="discard",
                tile=str(tile),
                metadata={"hand_size": len(player.hand)},
            )

            # Don't auto-advance turn - wait for potential ron/meld calls
            # The caller should check for calls and then advance manually

        return tile

    def advance_turn(self) -> None:
        """Advance to the next player's turn."""
        self.current_player = (self.current_player + 1) % 4
        self.turn_count += 1

        # Check for exhaustive draw before drawing
        if len(self.wall) == 0:
            self.handle_exhaustive_draw()
            return

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

    def check_ron(self, player_idx: int) -> bool:
        """
        Check if the specified player can declare ron on the last discard.

        Args:
            player_idx: Player index to check

        Returns:
            True if ron is possible
        """
        if not self.last_discard or self.last_discard_player is None:
            return False

        # Can't ron your own discard
        if player_idx == self.last_discard_player:
            return False

        player = self.players[player_idx]

        # Check if hand would be complete with the last discard
        test_hand = player.hand + [self.last_discard]

        num_melds = len(player.melds)
        if num_melds == 0:
            # Standard 14-tile hand
            return HandEvaluator.is_complete_hand(test_hand)
        elif num_melds == 4:
            # Only need a pair (2 tiles)
            if len(test_hand) == 2:
                return test_hand[0] == test_hand[1]
            return False
        else:
            # Need to check remaining tiles form valid structure
            return HandEvaluator._check_with_melds(test_hand, 4 - num_melds)

    def check_all_ron(self) -> List[int]:
        """
        Check which players can declare ron on the last discard.

        Returns:
            List of player indices who can declare ron
        """
        if not self.last_discard or self.last_discard_player is None:
            return []

        ron_players = []
        for i in range(4):
            if self.check_ron(i):
                ron_players.append(i)

        return ron_players

    def declare_ron(self, player_idx: int) -> bool:
        """
        Player declares ron on the last discard.

        Args:
            player_idx: Player declaring ron

        Returns:
            True if successful
        """
        if not self.check_ron(player_idx):
            return False

        # Calculate score
        player = self.players[player_idx]
        score_info = HandEvaluator.calculate_basic_score(
            player,
            self.last_discard,
            is_tsumo=False,
            player_wind=player.position,
            round_wind=self.round_wind,
        )

        # Transfer points from discard player to winner
        loser_idx = self.last_discard_player
        points = score_info.get("points", 1000)

        # Handle cost structure from mahjong library
        if "cost" in score_info and score_info["cost"]:
            cost = score_info["cost"]
            if "main" in cost:
                points = cost["main"]

        self.players[loser_idx].score -= points
        player.score += points

        # Mark round as won
        self.winner = player_idx

        self.log_action(
            player=player_idx,
            action_type="ron",
            tile=str(self.last_discard),
            metadata={
                "loser": loser_idx,
                "hand": [str(t) for t in player.hand],
                "winning_tile": str(self.last_discard),
                "score_info": score_info,
            },
        )

        # Handle round end after win
        self.handle_round_end_after_win(player_idx)

        return True

    def check_tsumo(self, player_idx: int) -> bool:
        """
        Check if the player can declare tsumo (self-draw win).
        Player must have just drawn a tile.

        Args:
            player_idx: Player to check

        Returns:
            True if tsumo is possible
        """
        player = self.players[player_idx]

        # Calculate expected hand size: 14 - (number of melds * 3)
        expected_hand_size = 14 - (len(player.melds) * 3)
        if len(player.hand) != expected_hand_size:
            return False

        # For hands with melds, we need to check if remaining tiles form valid structure
        # Each meld reduces the requirement by 1 group (3 tiles)
        # So: 0 melds = need 4 groups + 1 pair (14 tiles)
        #     1 meld  = need 3 groups + 1 pair (11 tiles)
        #     2 melds = need 2 groups + 1 pair (8 tiles)
        #     3 melds = need 1 group + 1 pair (5 tiles)
        #     4 melds = need 0 groups + 1 pair (2 tiles)

        num_melds = len(player.melds)
        if num_melds == 0:
            # Standard 14-tile hand
            return HandEvaluator.is_complete_hand(player.hand)
        elif num_melds == 4:
            # Only need a pair (2 tiles)
            if len(player.hand) == 2:
                return player.hand[0] == player.hand[1]
            return False
        else:
            # Need to check remaining tiles form valid structure
            # For simplicity, we'll use a recursive check
            return HandEvaluator._check_with_melds(player.hand, 4 - num_melds)

    def declare_tsumo(self, player_idx: int) -> bool:
        """
        Player declares tsumo (self-draw win).

        Args:
            player_idx: Player declaring tsumo

        Returns:
            True if successful
        """
        if not self.check_tsumo(player_idx):
            return False

        player = self.players[player_idx]

        # The winning tile is the last tile drawn (last in hand)
        winning_tile = player.hand[-1] if player.hand else None

        # Calculate score
        score_info = HandEvaluator.calculate_basic_score(
            player,
            winning_tile,
            is_tsumo=True,
            player_wind=player.position,
            round_wind=self.round_wind,
        )

        # Handle cost structure from mahjong library
        if "cost" in score_info and score_info["cost"]:
            cost = score_info["cost"]
            # In tsumo, cost structure is different
            # "main" is what dealer pays or what winner gets from dealer
            # "additional" is what non-dealers pay
            if player.position == 0:  # Dealer wins
                # All players pay the same (main value)
                points_per_player = cost.get("main", 0)
                for i in range(4):
                    if i != player_idx:
                        self.players[i].score -= points_per_player
                        player.score += points_per_player
            else:  # Non-dealer wins
                # Dealer pays "main", others pay "additional"
                dealer_payment = cost.get("main", 0)
                other_payment = cost.get("additional", 0)

                for i in range(4):
                    if i != player_idx:
                        if i == self.dealer:
                            self.players[i].score -= dealer_payment
                            player.score += dealer_payment
                        else:
                            self.players[i].score -= other_payment
                            player.score += other_payment
        else:
            # Fallback: simple split
            points = score_info.get("points", 1000)
            points_per_player = points // 3
            for i in range(4):
                if i != player_idx:
                    self.players[i].score -= points_per_player
                    player.score += points_per_player

        # Mark round as won
        self.winner = player_idx

        self.log_action(
            player=player_idx,
            action_type="tsumo",
            tile=str(winning_tile) if winning_tile else None,
            metadata={
                "hand": [str(t) for t in player.hand],
                "winning_tile": str(winning_tile) if winning_tile else None,
                "score_info": score_info,
            },
        )

        # Handle round end after win
        self.handle_round_end_after_win(player_idx)

        return True

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

    def check_pon(self, player_idx: int) -> bool:
        """
        Check if the specified player can call pon on the last discard.

        Args:
            player_idx: Player index to check

        Returns:
            True if pon is possible
        """
        if not self.last_discard or self.last_discard_player is None:
            return False

        # Can't call your own discard
        if player_idx == self.last_discard_player:
            return False

        player = self.players[player_idx]

        # Can't call if already in riichi
        if player.is_riichi:
            return False

        # Need at least 2 matching tiles in hand
        matching_count = sum(1 for t in player.hand if t == self.last_discard)
        return matching_count >= 2

    def declare_pon(self, player_idx: int) -> bool:
        """
        Player declares pon on the last discard.

        Args:
            player_idx: Player declaring pon

        Returns:
            True if successful
        """
        if not self.check_pon(player_idx):
            return False

        player = self.players[player_idx]

        # Remove 2 matching tiles from hand
        tiles_for_meld = []
        removed_count = 0
        for i in range(len(player.hand) - 1, -1, -1):
            if player.hand[i] == self.last_discard and removed_count < 2:
                tiles_for_meld.append(player.hand.pop(i))
                removed_count += 1

        # Add the called tile
        tiles_for_meld.append(self.last_discard)

        # Create meld
        meld = Meld(
            type="pon",
            tiles=tiles_for_meld,
            from_player=self.last_discard_player,
        )
        player.melds.append(meld)

        # Remove last discard from discarder's pile
        if self.players[self.last_discard_player].discards:
            self.players[self.last_discard_player].discards.pop()

        self.log_action(
            player=player_idx,
            action_type="pon",
            tile=str(self.last_discard),
            metadata={
                "from_player": self.last_discard_player,
                "meld_tiles": [str(t) for t in tiles_for_meld],
            },
        )

        # Clear last discard
        self.last_discard = None
        self.last_discard_player = None

        # Player must discard immediately (no draw)
        self.current_player = player_idx

        return True

    def check_chi(self, player_idx: int) -> List[List[Tile]]:
        """
        Check if the specified player can call chi on the last discard.
        Chi can only be called from the previous player (kamicha).

        Args:
            player_idx: Player index to check

        Returns:
            List of possible chi combinations (each is a list of 3 tiles)
        """
        if not self.last_discard or self.last_discard_player is None:
            return []

        # Can only chi from previous player (kamicha)
        if (self.last_discard_player + 1) % 4 != player_idx:
            return []

        # Can't chi honors
        if self.last_discard.is_honor:
            return []

        player = self.players[player_idx]

        # Can't call if already in riichi
        if player.is_riichi:
            return []

        tile_type = self.last_discard.type
        tile_num = self.last_discard.number

        possible_chis = []

        # Pattern 1: called tile is the lowest (e.g., 1-2-3 with 1 called)
        if tile_num <= 7:
            tile2 = Tile(tile_type, tile_num + 1)
            tile3 = Tile(tile_type, tile_num + 2)
            if tile2 in player.hand and tile3 in player.hand:
                possible_chis.append([self.last_discard, tile2, tile3])

        # Pattern 2: called tile is in the middle (e.g., 1-2-3 with 2 called)
        if 2 <= tile_num <= 8:
            tile1 = Tile(tile_type, tile_num - 1)
            tile3 = Tile(tile_type, tile_num + 1)
            if tile1 in player.hand and tile3 in player.hand:
                possible_chis.append([tile1, self.last_discard, tile3])

        # Pattern 3: called tile is the highest (e.g., 1-2-3 with 3 called)
        if tile_num >= 3:
            tile1 = Tile(tile_type, tile_num - 2)
            tile2 = Tile(tile_type, tile_num - 1)
            if tile1 in player.hand and tile2 in player.hand:
                possible_chis.append([tile1, tile2, self.last_discard])

        return possible_chis

    def declare_chi(self, player_idx: int, chi_pattern: List[Tile]) -> bool:
        """
        Player declares chi on the last discard.

        Args:
            player_idx: Player declaring chi
            chi_pattern: The 3-tile pattern chosen (including the called tile)

        Returns:
            True if successful
        """
        possible_chis = self.check_chi(player_idx)
        if not possible_chis:
            return False

        # Verify the chosen pattern is valid
        pattern_valid = False
        for possible in possible_chis:
            if len(chi_pattern) == 3 and all(
                chi_pattern[i] == possible[i] for i in range(3)
            ):
                pattern_valid = True
                break

        if not pattern_valid:
            return False

        player = self.players[player_idx]

        # Remove the tiles from hand (except the called tile)
        tiles_for_meld = []
        for tile in chi_pattern:
            if tile == self.last_discard:
                tiles_for_meld.append(tile)
            else:
                if tile in player.hand:
                    player.hand.remove(tile)
                    tiles_for_meld.append(tile)

        # Create meld
        meld = Meld(
            type="chi",
            tiles=tiles_for_meld,
            from_player=self.last_discard_player,
        )
        player.melds.append(meld)

        # Remove last discard from discarder's pile
        if self.players[self.last_discard_player].discards:
            self.players[self.last_discard_player].discards.pop()

        self.log_action(
            player=player_idx,
            action_type="chi",
            tile=str(self.last_discard),
            metadata={
                "from_player": self.last_discard_player,
                "meld_tiles": [str(t) for t in tiles_for_meld],
            },
        )

        # Clear last discard
        self.last_discard = None
        self.last_discard_player = None

        # Player must discard immediately (no draw)
        self.current_player = player_idx

        return True

    def check_kan(self, player_idx: int) -> Dict[str, List[Tile]]:
        """
        Check if the player can call kan.

        Args:
            player_idx: Player to check

        Returns:
            Dictionary with possible kan types:
            - "daiminkan": List of tiles for open kan from discard
            - "ankan": List of 4-tile sets for concealed kan
            - "shouminkan": List of tiles that can be added to existing pon
        """
        player = self.players[player_idx]
        result = {"daiminkan": [], "ankan": [], "shouminkan": []}

        # Daiminkan: open kan from last discard
        if (
            self.last_discard
            and self.last_discard_player is not None
            and player_idx != self.last_discard_player
            and not player.is_riichi
        ):
            matching_count = sum(1 for t in player.hand if t == self.last_discard)
            if matching_count == 3:
                result["daiminkan"] = [self.last_discard]

        # Ankan: concealed kan from hand (only if it's player's turn)
        if player_idx == self.current_player and not player.is_riichi:
            tile_counts = Counter(player.hand)
            for tile, count in tile_counts.items():
                if count == 4:
                    result["ankan"].append(tile)

        # Shouminkan: add to existing pon (only if it's player's turn)
        if player_idx == self.current_player:
            for meld in player.melds:
                if meld.type == "pon" and len(meld.tiles) == 3:
                    # Check if we have the 4th tile in hand
                    meld_tile = meld.tiles[0]
                    if meld_tile in player.hand:
                        result["shouminkan"].append(meld_tile)

        return result

    def declare_kan(
        self, player_idx: int, kan_type: str, tile: Tile
    ) -> bool:
        """
        Player declares kan.

        Args:
            player_idx: Player declaring kan
            kan_type: Type of kan ("daiminkan", "ankan", "shouminkan")
            tile: The tile for the kan

        Returns:
            True if successful
        """
        kan_options = self.check_kan(player_idx)

        player = self.players[player_idx]

        if kan_type == "daiminkan":
            if not kan_options["daiminkan"] or tile != self.last_discard:
                return False

            # Remove 3 matching tiles from hand
            tiles_for_meld = []
            removed_count = 0
            for i in range(len(player.hand) - 1, -1, -1):
                if player.hand[i] == tile and removed_count < 3:
                    tiles_for_meld.append(player.hand.pop(i))
                    removed_count += 1

            # Add the called tile
            tiles_for_meld.append(tile)

            # Create kan meld
            meld = Meld(
                type="kan",
                tiles=tiles_for_meld,
                from_player=self.last_discard_player,
            )
            player.melds.append(meld)

            # Remove last discard
            if self.players[self.last_discard_player].discards:
                self.players[self.last_discard_player].discards.pop()

            self.last_discard = None
            self.last_discard_player = None

        elif kan_type == "ankan":
            if tile not in kan_options["ankan"]:
                return False

            # Remove all 4 tiles from hand
            tiles_for_meld = [t for t in player.hand if t == tile]
            player.hand = [t for t in player.hand if t != tile]

            # Create concealed kan meld
            meld = Meld(type="kan", tiles=tiles_for_meld, from_player=None)
            player.melds.append(meld)

        elif kan_type == "shouminkan":
            if tile not in kan_options["shouminkan"]:
                return False

            # Find the pon meld and upgrade it
            for meld in player.melds:
                if (
                    meld.type == "pon"
                    and len(meld.tiles) == 3
                    and meld.tiles[0] == tile
                ):
                    # Remove tile from hand
                    if tile in player.hand:
                        player.hand.remove(tile)
                        meld.tiles.append(tile)
                        meld.type = "kan"
                        break

        else:
            return False

        # Draw replacement tile from dead wall
        if self.dead_wall:
            replacement_tile = self.dead_wall.pop(0)
            player.draw_tile(replacement_tile)

            # Reveal new dora indicator
            if len(self.dead_wall) >= 5:
                new_dora = self.dead_wall[4]
                if new_dora not in self.dora_indicators:
                    self.dora_indicators.append(new_dora)

        self.log_action(
            player=player_idx,
            action_type="kan",
            tile=str(tile),
            metadata={
                "kan_type": kan_type,
                "from_player": self.last_discard_player if kan_type == "daiminkan" else None,
            },
        )

        # After kan, player continues their turn (must discard)
        self.current_player = player_idx

        return True

    def handle_round_end_after_win(self, winner_idx: int) -> None:
        """
        Handle round end after a win (ron or tsumo).

        Args:
            winner_idx: Index of the winning player
        """
        # Check if winner is dealer
        if winner_idx == self.dealer:
            # 連荘 (renchan): dealer continues, honba increases
            self.honba_sticks += 1
        else:
            # 輪荘 (rinshou): dealer rotates
            self.honba_sticks = 0
            self.advance_round()

        # Start next round if game is not over
        if not self.is_game_over:
            self.start_new_round()

    def handle_exhaustive_draw(self) -> None:
        """
        Handle exhaustive draw (流局) when wall is empty.
        Check tenpai status, distribute noten payments.
        Does NOT automatically start next round - UI should call continue_after_exhaustive_draw().
        """
        # Check tenpai status for each player
        self.tenpai_players = []
        for i, player in enumerate(self.players):
            waiting_tiles = HandEvaluator.check_tenpai(player.hand)
            if waiting_tiles:
                self.tenpai_players.append(i)

        num_tenpai = len(self.tenpai_players)
        num_noten = 4 - num_tenpai

        # Distribute noten payments (3000 points total)
        if 0 < num_tenpai < 4:
            payment_per_noten = 3000 // num_noten
            payment_per_tenpai = 3000 // num_tenpai

            for i in range(4):
                if i in self.tenpai_players:
                    self.players[i].score += payment_per_tenpai
                else:
                    self.players[i].score -= payment_per_noten

        # Log the draw
        self.log_action(
            player=-1,
            action_type="exhaustive_draw",
            metadata={
                "tenpai_players": self.tenpai_players,
                "num_tenpai": num_tenpai,
                "dealer_tenpai": self.dealer in self.tenpai_players,
            },
        )

        # Set exhaustive draw flag (UI will display and then call continue method)
        self.is_exhaustive_draw = True

    def continue_after_exhaustive_draw(self) -> None:
        """
        Continue to next round after exhaustive draw.
        Should be called by UI after displaying tenpai/noten status.
        """
        # Dealer rotation logic
        dealer_tenpai = self.dealer in self.tenpai_players
        if dealer_tenpai:
            # 連荘 (renchan): dealer continues, honba increases
            self.honba_sticks += 1
        else:
            # 輪荘 (rinshou): dealer rotates
            self.honba_sticks = 0
            self.advance_round()

        # Clear exhaustive draw state
        self.is_exhaustive_draw = False
        self.tenpai_players = []

        # Start next round
        if not self.is_game_over:
            self.start_new_round()

    def advance_round(self) -> None:
        """
        Advance to the next round.
        Handles round progression: East 1 -> East 2 -> ... -> South 1 -> ...
        """
        self.round_number += 1

        if self.round_number >= 4:
            # Move to next wind
            self.round_number = 0
            self.round_wind += 1

            # Check if game should end
            if self.game_type == "tonpuu" and self.round_wind >= 1:
                # 東風戦: game ends after East round
                self.is_game_over = True
                return
            elif self.game_type == "hanchan" and self.round_wind >= 2:
                # 半荘: game ends after South round
                self.is_game_over = True
                return

        # Rotate dealer
        self.dealer = (self.dealer + 1) % 4

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
            "round_number": self.round_number,
            "honba_sticks": self.honba_sticks,
            "riichi_sticks": self.riichi_sticks,
            "game_type": self.game_type,
            "wall_remaining": len(self.wall),
            "is_game_over": self.is_game_over,
            "winner": self.winner,
            "is_exhaustive_draw": self.is_exhaustive_draw,
            "tenpai_players": self.tenpai_players,
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
                    "last_drawn_tile": str(p.last_drawn_tile) if p.last_drawn_tile else "",
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
