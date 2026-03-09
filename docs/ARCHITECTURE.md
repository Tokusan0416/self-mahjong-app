# Architecture Overview

This document describes the system architecture of the Mahjong Self-Play Simulator.

## System Design

The application follows a clean separation between game logic and UI:

```
┌─────────────────────────────────────────────────────────────┐
│                      Reflex Frontend (React)                 │
│  - Hand displays (4 players)                                 │
│  - Discard piles                                             │
│  - Game controls                                             │
│  - Status information                                        │
└───────────────────────┬─────────────────────────────────────┘
                        │ Event Handlers
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                  MahjongState (Reflex State)                 │
│  - Manages UI state (hands, discards, scores)                │
│  - Handles user interactions                                 │
│  - Syncs with game engine                                    │
└───────────────────────┬─────────────────────────────────────┘
                        │ Method Calls
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                    MahjongGame (Engine)                      │
│  - Core game logic                                           │
│  - Rule enforcement                                          │
│  - Action logging                                            │
│  - State management                                          │
└───────────────────────┬─────────────────────────────────────┘
                        │ Uses
                        ▼
┌─────────────────────────────────────────────────────────────┐
│              Domain Models (Tile, Player, etc.)              │
│  - Tile: Individual mahjong tiles                            │
│  - Player: Player state and operations                       │
│  - HandEvaluator: Win condition checking                     │
└─────────────────────────────────────────────────────────────┘
```

## Components

### 1. Frontend Layer (Reflex/React)

**Location**: `app/components/`

- **hand.py**: Renders individual tiles and player hands
- **board.py**: Renders game board, controls, and information panels

**Responsibilities**:
- Display game state
- Capture user interactions
- Provide visual feedback

### 2. State Management (Reflex State)

**Location**: `app/state.py`

The `MahjongState` class manages the bridge between UI and game engine:

```python
class MahjongState(rx.State):
    # Rendered state (synced with game engine)
    current_player: int
    player_hands: List[List[str]]
    player_discards: List[List[str]]
    # ... other UI state

    # Event handlers
    def start_new_game(self): ...
    def discard_tile(self, player_idx: int, tile_str: str): ...
    def check_current_tenpai(self): ...
    def declare_riichi(self): ...
```

**Responsibilities**:
- Maintain UI-friendly state representations
- Handle user actions and events
- Call game engine methods
- Sync state after each action

### 3. Game Engine

**Location**: `app/engine/`

#### 3.1 MahjongGame (`game.py`)

The core game controller:

```python
class MahjongGame:
    players: List[Player]
    wall: List[Tile]
    current_player: int
    game_log: List[GameAction]

    def start_new_round(self): ...
    def draw_tile(self, player_idx: int): ...
    def discard_tile(self, player_idx: int, tile_idx: int): ...
    def check_win(self, player_idx: int): ...
    def log_action(self, ...): ...
```

**Responsibilities**:
- Manage game flow (turns, draws, discards)
- Enforce game rules
- Maintain game state
- Log all actions for analysis

#### 3.2 Tile System (`tiles.py`)

Tile representation and utilities:

```python
class TileType(Enum):
    MANZU = "m"  # 萬子 (characters)
    PINZU = "p"  # 筒子 (dots)
    SOUZU = "s"  # 索子 (bamboo)
    JIHAI = "z"  # 字牌 (honors)

@dataclass
class Tile:
    type: TileType
    number: int  # 1-9 for suits, 1-7 for honors
```

**Features**:
- 136 tiles total (34 types × 4 copies)
- String representation (e.g., "1m", "5p", "7z")
- Tile classification (honor, terminal, simple)

#### 3.3 Player Management (`player.py`)

Player state and operations:

```python
@dataclass
class Player:
    position: int  # 0=East, 1=South, 2=West, 3=North
    hand: List[Tile]
    discards: List[Tile]
    melds: List[Meld]
    score: int = 25000
    is_riichi: bool = False

    def draw_tile(self, tile: Tile): ...
    def discard_tile(self, tile: Tile): ...
    def declare_riichi(self, turn: int): ...
```

#### 3.4 Hand Evaluation (`scoring.py`)

Win condition checking and scoring:

```python
class HandEvaluator:
    @staticmethod
    def is_complete_hand(tiles: List[Tile]) -> bool: ...

    @staticmethod
    def check_tenpai(tiles: List[Tile]) -> List[Tile]: ...

    @staticmethod
    def calculate_basic_score(...) -> Dict: ...
```

## Data Flow

### 1. Starting a New Game

```
User clicks "New Game"
    ↓
MahjongState.start_new_game()
    ↓
Create new MahjongGame instance
    ↓
MahjongGame.start_new_round()
    ↓
- Shuffle tiles
- Deal to players
- Set initial state
    ↓
MahjongState._sync_state()
    ↓
UI updates with new game state
```

### 2. Discarding a Tile

```
User clicks tile in hand
    ↓
MahjongState.discard_tile(index)
    ↓
MahjongGame.discard_tile(player_idx, tile_idx)
    ↓
- Remove tile from hand
- Add to discard pile
- Log action
- Advance turn
- Auto-draw for next player
    ↓
MahjongState._sync_state()
    ↓
UI updates:
- Hand refreshes
- Discards update
- Current player changes
```

### 3. Checking Tenpai

```
User clicks "Check Tenpai"
    ↓
MahjongState.check_current_tenpai()
    ↓
MahjongGame.check_tenpai(player_idx)
    ↓
HandEvaluator.check_tenpai(hand)
    ↓
- Try adding each possible tile
- Check if hand becomes complete
- Return list of waiting tiles
    ↓
Update waiting_tiles state
    ↓
UI displays waiting tiles
```

## Game State Structure

The game state is a comprehensive dictionary:

```python
{
    "current_player": 0,
    "turn_count": 5,
    "dealer": 0,
    "round_wind": 0,
    "wall_remaining": 70,
    "is_game_over": False,
    "winner": None,
    "players": [
        {
            "position": 0,
            "wind": "East",
            "hand": ["1m", "2m", "3m", ...],
            "hand_size": 14,
            "discards": ["9p", "8s", ...],
            "melds": [],
            "score": 25000,
            "is_riichi": False
        },
        # ... 3 more players
    ],
    "dora_indicators": ["5s"]
}
```

## Logging System

All game actions are logged for analysis:

```python
@dataclass
class GameAction:
    turn: int
    player: int
    action_type: str  # "draw", "discard", "pon", "chi", "riichi", etc.
    tile: Optional[str]
    timestamp: str
    metadata: Dict[str, Any]
```

Example log entry:
```json
{
    "turn": 5,
    "player": 1,
    "action_type": "discard",
    "tile": "3m",
    "timestamp": "2026-03-09T10:30:45.123456",
    "metadata": {
        "hand_size": 13
    }
}
```

## Future Architecture Enhancements

### Phase 2: BigQuery Integration

```
Game End
    ↓
MahjongGame.export_log_json()
    ↓
BigQuery Client
    ↓
Insert into dataset.games table
```

### Phase 3: Advanced Features

- WebSocket support for real-time multiplayer
- Redis caching for game state
- Background task queue for analysis
- REST API for external tools

## Design Principles

1. **Separation of Concerns**: Game logic is independent of UI
2. **Single Source of Truth**: MahjongGame maintains authoritative state
3. **Event-Driven**: All actions are logged as discrete events
4. **Type Safety**: Extensive use of type hints and dataclasses
5. **Testability**: Pure functions and clear interfaces enable easy testing

## Performance Considerations

- **Tile Pool Generation**: Shuffled once per round (O(n) where n=136)
- **Win Checking**: Recursive algorithm, optimized with early exits
- **State Sync**: Only happens after user actions (not on every render)
- **UI Updates**: Reflex handles efficient React reconciliation

## Security Notes

For production deployment:
- Add authentication for multi-user access
- Sanitize all user inputs
- Use environment variables for credentials
- Implement rate limiting on API endpoints
- Enable CORS restrictions

## Reflex 0.8 Specific Implementation

### Key Patterns

**Reactive Variables**:
- Use `rx.cond()` instead of Python `if` statements for conditional rendering
- Use `rx.foreach()` instead of list comprehensions for iterating over Vars
- Use `.length()` instead of `len()` for Var sequences
- Use `.to_string()` for string conversion in templates

**Example**:
```python
# ❌ Wrong (Python conditionals with Vars)
header_color = "#2c5282" if is_current else "#4a5568"

# ✅ Correct (Reflex conditional)
color=rx.cond(is_current, "#2c5282", "#4a5568")

# ❌ Wrong (list comprehension with Vars)
*[render_tile(t) for t in tiles]

# ✅ Correct (rx.foreach)
rx.foreach(tiles, render_tile)
```

---

# アーキテクチャ概要（日本語）

## システム設計

麻雀セルフプレイシミュレーターは、ゲームロジックとUIを明確に分離したアーキテクチャを採用しています。

### 主要コンポーネント

1. **フロントエンド層** (`app/components/`)
   - `hand.py`: 牌と手牌のレンダリング
   - `board.py`: 盤面、コントロール、情報パネル

2. **状態管理** (`app/state.py`)
   - `MahjongState`クラス: UIとゲームエンジン間の橋渡し
   - イベントハンドラとUI状態の管理
   - ゲームエンジンとの同期

3. **ゲームエンジン** (`app/engine/`)
   - `tiles.py`: 136枚の牌の定義と操作
   - `player.py`: プレイヤーの状態（手牌、捨て牌、点数）
   - `game.py`: コアゲームロジック、ターン管理、ログ記録
   - `scoring.py`: 手牌評価とテンパイ判定

### データフロー

```
ユーザークリック → MahjongState（イベントハンドラ）
    ↓
MahjongGame（エンジン）でロジック処理
    ↓
_sync_state()でUI状態を同期
    ↓
Reflexが自動的にUIを更新
```

### Reflex 0.8の重要な実装パターン

**リアクティブ変数の扱い**:
- Python の `if` の代わりに `rx.cond()` を使用
- リスト内包表記の代わりに `rx.foreach()` を使用
- `len()` の代わりに `.length()` を使用
- 文字列変換に `.to_string()` を使用

**状態の計算プロパティ**:
```python
@rx.var
def current_player_name(self) -> str:
    """Varを配列インデックスで使えないため、計算プロパティで対応"""
    names = ["East", "South", "West", "North"]
    return names[self.current_player]
```

### 設計原則

1. **関心の分離**: ゲームロジックはUIから独立
2. **単一の真実の源**: MahjongGameが権威ある状態を維持
3. **イベント駆動**: 全アクションを離散イベントとしてログ記録
4. **型安全性**: 型ヒントとdataclassを広範に使用
5. **テスト可能性**: 純粋関数と明確なインターフェース

### ログシステム

全てのゲームアクションをJSON形式で記録:
- プレイヤー、ターン、アクションタイプ
- タイムスタンプとメタデータ
- BigQuery統合のための構造化データ

### 将来の拡張

**Phase 2**: BigQuery統合
**Phase 3**: WebSocket、Redis、REST API
