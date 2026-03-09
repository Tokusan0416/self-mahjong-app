# API Documentation

Complete API reference for the Mahjong game engine.

## Table of Contents

- [Tile System](#tile-system)
- [Player Management](#player-management)
- [Game Engine](#game-engine)
- [Hand Evaluation](#hand-evaluation)
- [State Management](#state-management)

---

## Tile System

### TileType

Enum representing the four tile types in Mahjong.

```python
from app.engine.tiles import TileType

class TileType(Enum):
    MANZU = "m"  # 萬子 (characters)
    PINZU = "p"  # 筒子 (dots)
    SOUZU = "s"  # 索子 (bamboo)
    JIHAI = "z"  # 字牌 (honors: winds and dragons)
```

### Tile

Represents a single mahjong tile.

```python
from app.engine.tiles import Tile, TileType

@dataclass
class Tile:
    type: TileType
    number: int  # 1-9 for suits, 1-7 for honors
```

**Properties**:

- `is_honor: bool` - True if this is an honor tile (wind or dragon)
- `is_terminal: bool` - True if this is a terminal (1 or 9 of a suit)
- `is_simple: bool` - True if this is a simple tile (2-8 of a suit)

**Methods**:

#### `__str__() -> str`

Returns string representation like '1m', '5p', '7z'.

```python
tile = Tile(TileType.MANZU, 1)
print(tile)  # "1m"
```

#### `from_string(s: str) -> Tile` (classmethod)

Creates a tile from string representation.

```python
tile = Tile.from_string("5p")
# Tile(type=TileType.PINZU, number=5)
```

**Parameters**:
- `s` (str): String like "1m", "5p", "7z"

**Returns**: Tile object

**Raises**: ValueError if string is invalid

### Tile Utility Functions

#### `create_tile_pool() -> List[Tile]`

Creates a complete, shuffled pool of 136 tiles.

```python
from app.engine.tiles import create_tile_pool

tiles = create_tile_pool()
# Returns 136 tiles (34 types × 4 copies), shuffled
```

**Returns**: List of 136 Tile objects

#### `sort_tiles(tiles: List[Tile]) -> List[Tile]`

Sorts tiles in standard order (manzu, pinzu, souzu, honors).

```python
from app.engine.tiles import sort_tiles

unsorted = [Tile.from_string(t) for t in ["7z", "1p", "1m"]]
sorted_tiles = sort_tiles(unsorted)
# [1m, 1p, 7z]
```

**Parameters**:
- `tiles` (List[Tile]): Unsorted list of tiles

**Returns**: Sorted list of tiles

#### `tiles_to_string(tiles: List[Tile]) -> str`

Converts list of tiles to compact string representation.

```python
from app.engine.tiles import tiles_to_string

tiles = [Tile.from_string(t) for t in ["1m", "2m", "3m"]]
result = tiles_to_string(tiles)
# "1m 2m 3m"
```

**Parameters**:
- `tiles` (List[Tile]): List of tiles

**Returns**: Space-separated string

#### `string_to_tiles(s: str) -> List[Tile]`

Parses string representation to list of tiles.

```python
from app.engine.tiles import string_to_tiles

tiles = string_to_tiles("1m 2m 3m 5p")
# [Tile(MANZU, 1), Tile(MANZU, 2), Tile(MANZU, 3), Tile(PINZU, 5)]
```

**Parameters**:
- `s` (str): Space-separated tile strings

**Returns**: List of Tile objects

---

## Player Management

### Meld

Represents a called meld (pon, chi, kan).

```python
from app.engine.player import Meld

@dataclass
class Meld:
    type: str  # "pon", "chi", "kan"
    tiles: List[Tile]
    from_player: Optional[int] = None  # Which player the tile was called from
```

### Player

Represents a single player in the game.

```python
from app.engine.player import Player

@dataclass
class Player:
    position: int  # 0=East, 1=South, 2=West, 3=North
    hand: List[Tile] = field(default_factory=list)
    discards: List[Tile] = field(default_factory=list)
    melds: List[Meld] = field(default_factory=list)
    score: int = 25000
    is_riichi: bool = False
    riichi_turn: Optional[int] = None
```

**Properties**:

- `hand_size: int` - Current number of tiles in hand
- `total_tiles: int` - Total tiles including melds
- `wind_name: str` - Wind position name ("East", "South", "West", "North")

**Methods**:

#### `draw_tile(tile: Tile) -> None`

Adds a tile to the hand.

```python
player = Player(position=0)
tile = Tile.from_string("5m")
player.draw_tile(tile)
```

**Parameters**:
- `tile` (Tile): The tile to draw

#### `discard_tile(tile: Tile) -> bool`

Discards a tile from the hand.

```python
player = Player(position=0)
# ... player has tiles in hand
tile = Tile.from_string("9p")
success = player.discard_tile(tile)
```

**Parameters**:
- `tile` (Tile): The tile to discard

**Returns**: True if successful, False if tile not in hand

#### `discard_by_index(index: int) -> Optional[Tile]`

Discards a tile from hand by index.

```python
player = Player(position=0)
# ... player has tiles in hand
discarded = player.discard_by_index(0)  # Discard first tile
```

**Parameters**:
- `index` (int): Index of the tile in hand

**Returns**: The discarded tile, or None if index invalid

#### `sort_hand() -> None`

Sorts the tiles in the hand.

```python
player.sort_hand()
# Hand is now sorted: manzu, pinzu, souzu, honors
```

#### `can_declare_riichi() -> bool`

Checks if player can declare riichi.

```python
if player.can_declare_riichi():
    print("Can declare riichi!")
```

**Returns**: True if riichi can be declared

**Requirements**:
- Not already in riichi
- Has exactly 13 tiles
- Score ≥ 1000
- No open melds

#### `declare_riichi(turn: int) -> bool`

Declares riichi for this player.

```python
if player.declare_riichi(turn=5):
    print("Riichi declared!")
```

**Parameters**:
- `turn` (int): Current turn number

**Returns**: True if successful

**Effects**:
- Sets `is_riichi = True`
- Sets `riichi_turn = turn`
- Deducts 1000 from score

#### `add_meld(meld: Meld) -> None`

Adds a meld (pon/chi/kan) to the player.

```python
tiles = [Tile.from_string(t) for t in ["5m", "5m", "5m"]]
meld = Meld(type="pon", tiles=tiles, from_player=2)
player.add_meld(meld)
```

**Parameters**:
- `meld` (Meld): The meld to add

**Effects**:
- Adds meld to `melds` list
- Removes tiles from hand

---

## Game Engine

### GameAction

Represents a single game action for logging.

```python
from app.engine.game import GameAction

@dataclass
class GameAction:
    turn: int
    player: int  # -1 for system actions
    action_type: str  # "draw", "discard", "pon", "chi", "kan", "riichi", "tsumo", "ron"
    tile: Optional[str] = None
    tiles: Optional[List[str]] = None
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    metadata: Dict[str, Any] = field(default_factory=dict)
```

### MahjongGame

Main game class managing game state and flow.

```python
from app.engine.game import MahjongGame

game = MahjongGame()
```

**Attributes**:

- `players: List[Player]` - Four Player objects
- `wall: List[Tile]` - Remaining tiles in the wall
- `dead_wall: List[Tile]` - Last 14 tiles (for dora and replacements)
- `dora_indicators: List[Tile]` - Dora indicator tiles
- `current_player: int` - Index of current player (0-3)
- `turn_count: int` - Total number of turns
- `round_wind: int` - Current round (0=East, 1=South, etc.)
- `dealer: int` - Index of dealer
- `game_log: List[GameAction]` - All game actions
- `is_game_over: bool` - Whether game has ended
- `winner: Optional[int]` - Index of winner if game over

**Methods**:

#### `start_new_round() -> None`

Starts a new round of mahjong.

```python
game = MahjongGame()
game.start_new_round()
```

**Effects**:
- Creates and shuffles tile pool
- Separates dead wall
- Deals 13 tiles to each player
- Dealer draws 14th tile
- Resets all player state
- Logs game start

#### `draw_tile(player_idx: int) -> Optional[Tile]`

Draws a tile from the wall for specified player.

```python
tile = game.draw_tile(player_idx=0)
if tile:
    print(f"Drew: {tile}")
```

**Parameters**:
- `player_idx` (int): Index of player (0-3)

**Returns**: The drawn tile, or None if wall is empty

**Effects**:
- Removes tile from wall
- Adds tile to player's hand
- Logs draw action

#### `discard_tile(player_idx: int, tile_idx: int) -> Optional[Tile]`

Player discards a tile by index.

```python
discarded = game.discard_tile(player_idx=0, tile_idx=5)
```

**Parameters**:
- `player_idx` (int): Index of player
- `tile_idx` (int): Index of tile in player's hand

**Returns**: The discarded tile, or None if invalid

**Effects**:
- Removes tile from hand
- Adds to discard pile
- Logs discard action
- Advances turn
- Auto-draws for next player

#### `advance_turn() -> None`

Advances to the next player's turn.

```python
game.advance_turn()
```

**Effects**:
- Increments `current_player` (wraps at 4)
- Increments `turn_count`
- Draws tile for next player

#### `check_win(player_idx: int, tile: Optional[Tile] = None) -> bool`

Checks if player has won.

```python
if game.check_win(player_idx=0):
    print("Player 0 wins!")
```

**Parameters**:
- `player_idx` (int): Player to check
- `tile` (Optional[Tile]): Optional winning tile (for ron)

**Returns**: True if player has won

**Effects** (if win):
- Sets `winner = player_idx`
- Sets `is_game_over = True`
- Logs win action

#### `check_tenpai(player_idx: int) -> List[Tile]`

Checks which tiles the player is waiting for.

```python
waiting = game.check_tenpai(player_idx=0)
print(f"Waiting for: {[str(t) for t in waiting]}")
```

**Parameters**:
- `player_idx` (int): Player to check

**Returns**: List of tiles that would complete the hand

#### `declare_riichi(player_idx: int) -> bool`

Player declares riichi.

```python
if game.declare_riichi(player_idx=0):
    print("Riichi declared!")
```

**Parameters**:
- `player_idx` (int): Player declaring riichi

**Returns**: True if successful

**Effects**:
- Calls `player.declare_riichi()`
- Logs riichi action

#### `log_action(player: int, action_type: str, ...) -> None`

Logs a game action.

```python
game.log_action(
    player=0,
    action_type="discard",
    tile="5m",
    metadata={"hand_size": 13}
)
```

**Parameters**:
- `player` (int): Player index (-1 for system)
- `action_type` (str): Type of action
- `tile` (Optional[str]): Tile involved
- `tiles` (Optional[List[str]]): Multiple tiles
- `metadata` (Optional[Dict]): Additional data

#### `get_game_state() -> Dict[str, Any]`

Gets current game state as dictionary.

```python
state = game.get_game_state()
print(state["current_player"])
print(state["players"][0]["hand"])
```

**Returns**: Dictionary containing:
- `current_player`: Current player index
- `turn_count`: Number of turns
- `dealer`: Dealer index
- `round_wind`: Round wind
- `wall_remaining`: Tiles left in wall
- `is_game_over`: Game over flag
- `winner`: Winner index or None
- `players`: List of player states
- `dora_indicators`: Dora indicator tiles

#### `export_log_json() -> str`

Exports game log as JSON string.

```python
json_log = game.export_log_json()
print(json_log)  # Pretty-printed JSON
```

**Returns**: JSON string with game state and all actions

---

## Hand Evaluation

### HandEvaluator

Static class for evaluating mahjong hands.

```python
from app.engine.scoring import HandEvaluator
```

**Methods** (all static):

#### `is_complete_hand(tiles: List[Tile]) -> bool`

Checks if the hand is complete (ready to win).

```python
tiles = [Tile.from_string(t) for t in [
    "1m", "1m", "1m",  # triplet
    "2p", "3p", "4p",  # sequence
    "5s", "6s", "7s",  # sequence
    "1z", "1z", "1z",  # triplet
    "2z", "2z"         # pair
]]
is_complete = HandEvaluator.is_complete_hand(tiles)
# True
```

**Parameters**:
- `tiles` (List[Tile]): List of tiles to check (must be 14)

**Returns**: True if hand is complete

**Complete hand structure**:
- 4 melds (3 tiles each) + 1 pair (2 tiles)
- Melds: triplets or sequences
- Pair: two identical tiles

#### `check_tenpai(tiles: List[Tile]) -> List[Tile]`

Checks which tiles would complete the hand.

```python
hand = [Tile.from_string(t) for t in [
    "1m", "2m", "3m",
    "4p", "5p", "6p",
    "7s", "8s", "9s",
    "1z", "1z", "1z", "2z"
]]
waiting = HandEvaluator.check_tenpai(hand)
# [Tile(JIHAI, 2)]  - waiting for 2z to make pair
```

**Parameters**:
- `tiles` (List[Tile]): Current hand (must be 13 tiles)

**Returns**: List of tiles that would complete the hand

#### `calculate_basic_score(player: Player, winning_tile: Tile, is_tsumo: bool = False) -> Dict[str, Any]`

Calculates basic score for a winning hand (simplified).

```python
score_info = HandEvaluator.calculate_basic_score(
    player=player,
    winning_tile=Tile.from_string("5m"),
    is_tsumo=True
)
print(score_info)
# {
#     "han": 2,
#     "fu": 30,
#     "points": 2000,
#     "yaku": ["Riichi", ...],
#     "is_tsumo": True
# }
```

**Parameters**:
- `player` (Player): The winning player
- `winning_tile` (Tile): The tile that completed the hand
- `is_tsumo` (bool): True if self-drawn win

**Returns**: Dictionary with:
- `han`: Number of han (doubles)
- `fu`: Number of fu (minipoints)
- `points`: Calculated points
- `yaku`: List of yaku names
- `is_tsumo`: Self-drawn flag

**Note**: Current implementation is simplified. Phase 2 will use `mahjong` library for full yaku detection.

---

## State Management

### MahjongState

Reflex state class managing UI state.

```python
from app.state import MahjongState
```

**State Variables**:

```python
# Game state
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
```

**Event Handlers**:

#### `start_new_game()`

Starts a new game.

```python
# In component:
rx.button("New Game", on_click=MahjongState.start_new_game)
```

#### `discard_tile(tile_index: int)`

Discards a tile from current player's hand.

```python
# In component:
rx.button("Tile", on_click=lambda: MahjongState.discard_tile(index))
```

**Parameters**:
- `tile_index` (int): Index of tile to discard

#### `check_current_tenpai()`

Checks what tiles the current player is waiting for.

```python
# In component:
rx.button("Check Tenpai", on_click=MahjongState.check_current_tenpai)
```

#### `declare_riichi()`

Declares riichi for the current player.

```python
# In component:
rx.button("Riichi", on_click=MahjongState.declare_riichi)
```

#### `check_win()`

Checks if current player has won.

```python
# In component:
rx.button("Check Win", on_click=MahjongState.check_win)
```

#### `export_log()`

Exports game log as JSON.

```python
# In component:
rx.button("Export", on_click=MahjongState.export_log)
```

**Computed Variables**:

#### `player_names: List[str]`

Gets player names with wind positions, scores, and riichi status.

```python
# Usage in component:
rx.text(MahjongState.player_names[0])
# "East (25000)"
# or "East (24000) [RIICHI]"
```

**Returns**: List of formatted player names

---

## Example Usage

### Complete Game Flow

```python
from app.engine.game import MahjongGame

# Create and start game
game = MahjongGame()
game.start_new_round()

# Game loop
while not game.is_game_over and game.wall:
    current = game.current_player
    player = game.players[current]

    print(f"\n{player.wind_name}'s turn")
    print(f"Hand: {[str(t) for t in player.hand]}")

    # Check if in tenpai
    waiting = game.check_tenpai(current)
    if waiting:
        print(f"Tenpai! Waiting for: {[str(t) for t in waiting]}")

        # Maybe declare riichi
        if player.can_declare_riichi():
            game.declare_riichi(current)

    # Discard a tile (example: discard first tile)
    game.discard_tile(current, 0)

# Export log
log = game.export_log_json()
print(log)
```

### Custom Hand Evaluation

```python
from app.engine.tiles import Tile, string_to_tiles
from app.engine.scoring import HandEvaluator

# Create a hand
hand_str = "1m 2m 3m 4p 5p 6p 7s 8s 9s 1z 1z 1z 2z"
tiles = string_to_tiles(hand_str)

# Check if waiting
waiting = HandEvaluator.check_tenpai(tiles)
print(f"Waiting for: {[str(t) for t in waiting]}")

# Add winning tile and check complete
tiles.append(Tile.from_string("2z"))
is_win = HandEvaluator.is_complete_hand(tiles)
print(f"Complete hand: {is_win}")
```

---

# APIリファレンス（日本語クイックガイド）

## 牌システム (`app/engine/tiles.py`)

### Tile - 牌クラス
```python
# 牌の作成
tile = Tile(TileType.MANZU, 5)  # 5萬
tile = Tile.from_string("5m")    # 文字列から作成

# プロパティ
tile.is_honor      # 字牌かどうか
tile.is_terminal   # 老頭牌（1, 9）かどうか
tile.is_simple     # 中張牌（2-8）かどうか
```

### 主要関数
- `create_tile_pool()` - 136枚の牌を生成（シャッフル済み）
- `sort_tiles(tiles)` - 牌をソート（萬子→筒子→索子→字牌）
- `tiles_to_string(tiles)` - 牌リストを文字列に変換
- `string_to_tiles(s)` - 文字列を牌リストに変換

## プレイヤー管理 (`app/engine/player.py`)

### Player - プレイヤークラス
```python
player = Player(position=0)  # 0=東, 1=南, 2=西, 3=北

# 主要メソッド
player.draw_tile(tile)           # ツモ
player.discard_tile(tile)        # 打牌
player.sort_hand()               # 手牌をソート
player.declare_riichi(turn)      # 立直宣言

# プロパティ
player.hand_size                 # 手牌の枚数
player.wind_name                 # "East", "South"など
```

## ゲームエンジン (`app/engine/game.py`)

### MahjongGame - メインゲームクラス
```python
game = MahjongGame()
game.start_new_round()           # 局を開始

# 主要メソッド
game.draw_tile(player_idx)               # プレイヤーがツモ
game.discard_tile(player_idx, tile_idx)  # プレイヤーが打牌
game.check_win(player_idx)               # 和了判定
game.check_tenpai(player_idx)            # テンパイ判定
game.declare_riichi(player_idx)          # 立直宣言
game.export_log_json()                   # ログをJSON出力
```

## 手牌評価 (`app/engine/scoring.py`)

### HandEvaluator - 手牌評価クラス
```python
# テンパイチェック（13枚）
waiting_tiles = HandEvaluator.check_tenpai(hand)

# 和了形チェック（14枚）
is_complete = HandEvaluator.is_complete_hand(hand)

# 点数計算（簡易版）
score = HandEvaluator.calculate_basic_score(player, winning_tile, is_tsumo)
```

## Reflexステート (`app/state.py`)

### MahjongState - UIステート管理
```python
class MahjongState(rx.State):
    # 状態変数
    current_player: int
    player_hands: List[List[str]]
    player_discards: List[List[str]]

    # イベントハンドラ
    def start_new_game(self)
    def discard_tile(self, player_idx: int, tile_str: str)
    def check_current_tenpai(self)
    def declare_riichi(self)
    def export_log(self)
```

### Reflexコンポーネントでの使用
```python
# UIでの使用例
rx.button("New Game", on_click=MahjongState.start_new_game)
rx.text(MahjongState.current_player_name)
rx.foreach(MahjongState.player_hands[0], render_tile)
```

## 牌の表記法

- **萬子**: `1m`, `2m`, ..., `9m`
- **筒子**: `1p`, `2p`, ..., `9p`
- **索子**: `1s`, `2s`, ..., `9s`
- **字牌**: `1z`(東), `2z`(南), `3z`(西), `4z`(北), `5z`(白), `6z`(發), `7z`(中)

## よくあるパターン

### ゲームフロー全体
```python
# ゲーム作成と開始
game = MahjongGame()
game.start_new_round()

# ゲームループ
while not game.is_game_over:
    current = game.current_player

    # テンパイチェック
    waiting = game.check_tenpai(current)
    if waiting:
        game.declare_riichi(current)

    # 打牌（最初の牌を捨てる）
    game.discard_tile(current, 0)

# ログ出力
log_json = game.export_log_json()
```

### 手牌の評価
```python
# 手牌を作成
tiles = string_to_tiles("1m 2m 3m 4p 5p 6p 7s 8s 9s 1z 1z 1z 2z")

# テンパイチェック（13枚）
waiting = HandEvaluator.check_tenpai(tiles)
print(f"待ち: {[str(t) for t in waiting]}")

# 和了判定（14枚）
tiles.append(Tile.from_string("2z"))
is_win = HandEvaluator.is_complete_hand(tiles)
```
