# Development Guide

Guide for developers who want to extend or modify the Mahjong Self-Play Simulator.

## Table of Contents

- [Setup](#setup)
- [Project Structure](#project-structure)
- [Development Workflow](#development-workflow)
- [Adding Features](#adding-features)
- [Testing](#testing)
- [Code Style](#code-style)
- [Common Tasks](#common-tasks)

## Setup

### Development Environment

1. **Clone and enter directory**:
```bash
git clone <repository-url>
cd private-self-mahjong-reflex
```

2. **Create virtual environment** (recommended):
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**:
```bash
# Install package in editable mode with dev dependencies
pip install -e ".[dev]"

# Or using uv (faster)
uv pip install -e ".[dev]"
```

4. **Initialize Reflex**:
```bash
reflex init
```

### Development Dependencies

The `[dev]` extras include:
- `pytest`: Testing framework
- `black`: Code formatter
- `ruff`: Fast Python linter

### Running in Development Mode

```bash
# Start dev server (auto-reloads on changes)
reflex run

# Run in debug mode
reflex run --loglevel debug

# Run on different port
reflex run --port 8000
```

## Project Structure

```
private-self-mahjong-reflex/
├── app/                      # Main application package
│   ├── __init__.py
│   ├── engine/               # Game logic (pure Python)
│   │   ├── __init__.py
│   │   ├── tiles.py          # Tile system
│   │   ├── player.py         # Player management
│   │   ├── game.py           # Game controller
│   │   └── scoring.py        # Hand evaluation
│   ├── components/           # Reflex UI components
│   │   ├── __init__.py
│   │   ├── hand.py           # Hand rendering
│   │   └── board.py          # Board rendering
│   ├── state.py              # Reflex state management
│   └── app.py                # Main Reflex app
├── docs/                     # Documentation
│   ├── ARCHITECTURE.md
│   ├── USAGE.md
│   ├── API.md
│   └── DEVELOPMENT.md
├── assets/                   # Static assets
├── tests/                    # Test files (to be created)
├── pyproject.toml            # Project configuration
├── rxconfig.py               # Reflex configuration
└── README.md
```

### Module Responsibilities

**engine/**: Pure Python game logic, no UI dependencies
- Can be imported and used standalone
- Fully testable without Reflex
- No Reflex imports allowed

**components/**: UI rendering logic
- Takes data as props
- Returns Reflex components
- Minimal state logic

**state.py**: Bridge between UI and engine
- Manages Reflex state
- Calls engine methods
- Syncs state after actions

**app.py**: Application entry point
- Defines pages and routes
- Configures Reflex app

## Development Workflow

### Making Changes

1. **Create a feature branch**:
```bash
git checkout -b feature/your-feature-name
```

2. **Make changes** to relevant files

3. **Test your changes**:
```bash
# Run app to test manually
reflex run

# Run automated tests (when available)
pytest
```

4. **Format and lint**:
```bash
# Format code
black app/

# Lint code
ruff check app/
```

5. **Commit changes**:
```bash
git add .
git commit -m "Add feature: description"
```

### Code Review Checklist

Before submitting changes:
- [ ] Code follows style guidelines
- [ ] All new functions have docstrings
- [ ] Type hints are added
- [ ] Manual testing completed
- [ ] No console errors
- [ ] Documentation updated if needed

## Adding Features

### Adding a New Game Action

Example: Adding a "Pon" (triplet call) feature

**1. Update Engine** (`engine/game.py`):

```python
def call_pon(
    self,
    calling_player: int,
    called_tile: Tile,
    from_player: int
) -> bool:
    """
    Player calls pon (triplet) on discarded tile.

    Args:
        calling_player: Player calling pon
        called_tile: The discarded tile
        from_player: Player who discarded

    Returns:
        True if successful
    """
    player = self.players[calling_player]

    # Check if player has 2 matching tiles
    matching = [t for t in player.hand if t == called_tile]
    if len(matching) < 2:
        return False

    # Create meld
    meld_tiles = [called_tile] + matching[:2]
    meld = Meld(type="pon", tiles=meld_tiles, from_player=from_player)

    # Remove tile from discard pile
    if called_tile in self.players[from_player].discards:
        self.players[from_player].discards.remove(called_tile)

    # Add meld to player
    player.add_meld(meld)

    # Log action
    self.log_action(
        player=calling_player,
        action_type="pon",
        tiles=[str(t) for t in meld_tiles],
        metadata={"from_player": from_player}
    )

    # Set current player
    self.current_player = calling_player

    return True
```

**2. Update State** (`state.py`):

```python
def call_pon(self, player_idx: int, tile: str):
    """Call pon for specified player."""
    if self.is_game_over:
        return

    tile_obj = Tile.from_string(tile)
    last_player = (self.current_player - 1) % 4

    if self._game.call_pon(player_idx, tile_obj, last_player):
        self._sync_state()
        self.info_message = f"{self.player_names[player_idx]} called Pon!"
    else:
        self.info_message = "Cannot call pon"
```

**3. Update UI** (`components/board.py`):

```python
def render_call_buttons(last_discard: str, current_player: int) -> rx.Component:
    """Render buttons to call melds on last discard."""
    from ..state import MahjongState

    if not last_discard:
        return rx.box()

    return rx.hstack(
        rx.button(
            "Pon",
            on_click=lambda: MahjongState.call_pon(
                current_player,
                last_discard
            ),
            color_scheme="purple",
        ),
        # Add Chi, Kan buttons...
    )
```

**4. Update Documentation**:
- Add to [API.md](API.md)
- Update [USAGE.md](USAGE.md) with new feature
- Update [ARCHITECTURE.md](ARCHITECTURE.md) if needed

### Adding a New UI Component

Example: Adding a score display widget

**1. Create Component** (`components/score.py`):

```python
"""Score display components."""

import reflex as rx
from typing import List

def render_score_table(scores: List[int], names: List[str]) -> rx.Component:
    """
    Render score table for all players.

    Args:
        scores: List of 4 scores
        names: List of 4 player names

    Returns:
        Score table component
    """
    return rx.table.root(
        rx.table.header(
            rx.table.row(
                rx.table.column_header_cell("Player"),
                rx.table.column_header_cell("Score"),
            )
        ),
        rx.table.body(
            *[
                rx.table.row(
                    rx.table.cell(names[i]),
                    rx.table.cell(str(scores[i])),
                )
                for i in range(4)
            ]
        ),
    )
```

**2. Export in `__init__.py`**:

```python
# components/__init__.py
from .score import render_score_table

__all__ = [
    # ... existing exports
    "render_score_table",
]
```

**3. Use in App**:

```python
# app.py
from .components.score import render_score_table

def index():
    return rx.container(
        # ... other components
        render_score_table(
            MahjongState.player_scores,
            MahjongState.player_names
        ),
    )
```

### Adding BigQuery Integration

When ready for Phase 3:

**1. Add dependency** (`pyproject.toml`):

```toml
dependencies = [
    # ... existing
    "google-cloud-bigquery>=3.0.0",
]
```

**2. Create BigQuery module** (`app/bigquery.py`):

```python
"""BigQuery integration for game log storage."""

from google.cloud import bigquery
from typing import Dict, Any
import os

class BigQueryLogger:
    """Handles uploading game logs to BigQuery."""

    def __init__(self, project_id: str, dataset_id: str, table_id: str):
        self.client = bigquery.Client(project=project_id)
        self.table_ref = f"{project_id}.{dataset_id}.{table_id}"

    def upload_game(self, game_data: Dict[str, Any]) -> bool:
        """
        Upload game log to BigQuery.

        Args:
            game_data: Game log dictionary

        Returns:
            True if successful
        """
        try:
            errors = self.client.insert_rows_json(self.table_ref, [game_data])
            return len(errors) == 0
        except Exception as e:
            print(f"Error uploading to BigQuery: {e}")
            return False
```

**3. Use in State**:

```python
from .bigquery import BigQueryLogger

class MahjongState(rx.State):
    # ... existing code

    def export_log(self):
        """Export game log to BigQuery."""
        log_json = self._game.export_log_json()

        # Save to BigQuery
        bq = BigQueryLogger(
            project_id=os.getenv("GCP_PROJECT_ID"),
            dataset_id="mahjong_games",
            table_id="game_logs"
        )

        if bq.upload_game(json.loads(log_json)):
            self.info_message = "Game log uploaded to BigQuery!"
        else:
            self.info_message = "Failed to upload log"
```

## Testing

### Writing Tests

Create test files in `tests/` directory:

**Example: `tests/test_tiles.py`**:

```python
"""Tests for tile system."""

import pytest
from app.engine.tiles import (
    Tile,
    TileType,
    create_tile_pool,
    sort_tiles,
    tiles_to_string,
    string_to_tiles,
)


def test_tile_creation():
    """Test creating a tile."""
    tile = Tile(TileType.MANZU, 1)
    assert str(tile) == "1m"
    assert tile.type == TileType.MANZU
    assert tile.number == 1


def test_tile_from_string():
    """Test creating tile from string."""
    tile = Tile.from_string("5p")
    assert tile.type == TileType.PINZU
    assert tile.number == 5


def test_tile_properties():
    """Test tile property checks."""
    honor = Tile(TileType.JIHAI, 1)
    assert honor.is_honor
    assert not honor.is_terminal
    assert not honor.is_simple

    terminal = Tile(TileType.MANZU, 1)
    assert not terminal.is_honor
    assert terminal.is_terminal
    assert not terminal.is_simple

    simple = Tile(TileType.PINZU, 5)
    assert not simple.is_honor
    assert not simple.is_terminal
    assert simple.is_simple


def test_create_tile_pool():
    """Test tile pool creation."""
    pool = create_tile_pool()
    assert len(pool) == 136

    # Each tile should appear exactly 4 times
    from collections import Counter
    tile_counts = Counter(pool)
    for tile, count in tile_counts.items():
        assert count == 4


def test_sort_tiles():
    """Test tile sorting."""
    tiles = [
        Tile.from_string("7z"),
        Tile.from_string("1p"),
        Tile.from_string("1m"),
    ]
    sorted_tiles = sort_tiles(tiles)
    assert [str(t) for t in sorted_tiles] == ["1m", "1p", "7z"]


def test_tiles_conversion():
    """Test converting between tiles and strings."""
    original = "1m 2m 3m 5p"
    tiles = string_to_tiles(original)
    result = tiles_to_string(tiles)
    assert result == original
```

**Run tests**:

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_tiles.py

# Run with coverage
pytest --cov=mahjong_app

# Run with verbose output
pytest -v
```

### Manual Testing

Always test manually after changes:

1. Start the app: `reflex run`
2. Test the specific feature
3. Check browser console for errors (F12)
4. Verify state updates correctly
5. Test edge cases

## Code Style

### Python Style Guide

Follow PEP 8 and project conventions:

**Formatting**:
```bash
# Format all code
black app/

# Check formatting
black --check app/
```

**Linting**:
```bash
# Lint code
ruff check app/

# Auto-fix issues
ruff check --fix app/
```

### Type Hints

Always add type hints:

```python
# Good
def discard_tile(self, tile: Tile) -> bool:
    """Discard a tile."""
    ...

# Bad
def discard_tile(self, tile):
    ...
```

### Docstrings

Use Google-style docstrings:

```python
def example_function(param1: int, param2: str) -> bool:
    """
    Short description of function.

    Longer description if needed. Explain what the function does,
    not how it does it.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of return value

    Raises:
        ValueError: When param1 is negative

    Example:
        >>> result = example_function(5, "test")
        >>> print(result)
        True
    """
    ...
```

### Import Order

Group imports in this order:

```python
# 1. Standard library
import os
from typing import List, Optional

# 2. Third-party packages
import reflex as rx

# 3. Local imports
from .tiles import Tile
from .player import Player
```

## Common Tasks

### Adding a New State Variable

1. **Add to State class**:
```python
class MahjongState(rx.State):
    # ... existing variables
    new_variable: str = "default"
```

2. **Update in `_sync_state`** if needed:
```python
def _sync_state(self):
    # ... existing sync
    self.new_variable = self._game.some_property
```

3. **Use in UI**:
```python
rx.text(MahjongState.new_variable)
```

### Debugging Tips

**Print debugging**:
```python
def discard_tile(self, tile_index: int):
    print(f"DEBUG: Discarding tile at index {tile_index}")
    print(f"DEBUG: Current player: {self.current_player}")
    # ... rest of function
```

**Browser console**:
- Open DevTools (F12)
- Check Console tab for errors
- Check Network tab for API calls
- Use React DevTools for component inspection

**Reflex debugging**:
```bash
# Run with debug logging
reflex run --loglevel debug

# Check Reflex internal state
# In state method:
print(f"State: {self.dict()}")
```

### Performance Optimization

**Avoid unnecessary re-renders**:
```python
# Use computed variables for expensive operations
@rx.var
def expensive_calculation(self) -> str:
    # This is cached and only recomputes when dependencies change
    return complex_operation(self.some_state)
```

**Batch state updates**:
```python
# Good: Single state update
def update_multiple(self):
    with rx.var_operations():
        self.var1 = "value1"
        self.var2 = "value2"
        self.var3 = "value3"

# Bad: Multiple separate updates (causes multiple re-renders)
def update_multiple(self):
    self.var1 = "value1"  # Re-render
    self.var2 = "value2"  # Re-render
    self.var3 = "value3"  # Re-render
```

## Contributing

### Pull Request Process

1. Fork the repository
2. Create feature branch
3. Make changes with tests
4. Format and lint code
5. Update documentation
6. Submit pull request with description

### Commit Message Format

```
type(scope): Short description

Longer description if needed.

- Bullet points for details
- More details

Closes #123
```

**Types**: feat, fix, docs, style, refactor, test, chore

**Examples**:
```
feat(engine): Add pon/chi/kan meld calling

fix(ui): Correct tile click detection on mobile

docs(api): Add examples for HandEvaluator

refactor(state): Simplify state sync logic
```

## Resources

- [Reflex Documentation](https://reflex.dev/docs)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)
- [Mahjong Rules](https://riichi.wiki/)
- [Project Architecture](ARCHITECTURE.md)
- [API Reference](API.md)

## Getting Help

- Check existing documentation
- Search issues on GitHub
- Ask in project discussions
- Review example code in codebase

## Next Steps

After setup:
1. Explore the codebase
2. Run and test the application
3. Read [ARCHITECTURE.md](ARCHITECTURE.md)
4. Try adding a small feature
5. Submit your first PR!

---

# 開発ガイド（日本語要約）

## セットアップ

```bash
# 1. リポジトリをクローン
git clone <repository-url>
cd private-self-mahjong-reflex

# 2. 仮想環境を作成
python -m venv .venv
source .venv/bin/activate

# 3. 依存関係をインストール
pip install -e ".[dev]"

# 4. Reflexを初期化
reflex init

# 5. 開発サーバーを起動
reflex run
```

## プロジェクト構造

```
app/                    # メインアプリケーション
  ├── engine/           # ゲームロジック（純粋Python、UIに依存しない）
  ├── components/       # UIコンポーネント
  ├── state.py          # Reflex状態管理
  └── app.py            # アプリケーションエントリーポイント
```

### モジュールの責務

**engine/**: 純粋なPythonゲームロジック
- UIに依存しない
- Reflexのインポート禁止
- 単独でテスト可能

**components/**: UIレンダリングロジック
- データをpropsとして受け取る
- Reflexコンポーネントを返す
- 最小限の状態ロジック

**state.py**: UIとエンジンの橋渡し
- Reflex状態の管理
- エンジンメソッドの呼び出し
- アクション後の状態同期

## 開発ワークフロー

1. **機能ブランチを作成**: `git checkout -b feature/your-feature`
2. **変更を加える**: コードを編集
3. **テスト**: `reflex run` で手動テスト
4. **フォーマット**: `black app/` でフォーマット
5. **リント**: `ruff check app/` でチェック
6. **コミット**: `git commit -m "Add feature: description"`

## 機能追加の例

### 新しいゲームアクションの追加

1. **エンジンを更新** (`engine/game.py`):
```python
def call_pon(self, calling_player: int, called_tile: Tile, from_player: int) -> bool:
    """ポンを呼ぶ"""
    # ロジックを実装
    self.log_action(player=calling_player, action_type="pon", ...)
    return True
```

2. **ステートを更新** (`state.py`):
```python
def call_pon(self, player_idx: int, tile: str):
    """指定プレイヤーのポンを呼ぶ"""
    tile_obj = Tile.from_string(tile)
    if self._game.call_pon(player_idx, tile_obj, last_player):
        self._sync_state()
```

3. **UIを更新** (`components/board.py`):
```python
rx.button("Pon", on_click=lambda: MahjongState.call_pon(player_idx, tile))
```

## テスト

```bash
# テストを実行
pytest

# カバレッジ付き
pytest --cov=app

# 詳細出力
pytest -v
```

## コーディング規約

### フォーマット
```bash
black app/           # コードをフォーマット
ruff check app/      # リントチェック
ruff check --fix app/ # 自動修正
```

### 型ヒント
```python
# 良い例
def discard_tile(self, tile: Tile) -> bool:
    """牌を捨てる"""
    ...

# 悪い例
def discard_tile(self, tile):
    ...
```

### Docstring
Google スタイルを使用:
```python
def example_function(param1: int, param2: str) -> bool:
    """
    関数の短い説明。

    Args:
        param1: param1の説明
        param2: param2の説明

    Returns:
        戻り値の説明
    """
```

## Reflex 0.8 特有のパターン

### リアクティブ変数の扱い
```python
# ❌ 悪い例（PythonのifをVarに使用）
if is_current:
    ...

# ✅ 良い例（rx.condを使用）
rx.cond(is_current, value_if_true, value_if_false)

# ❌ 悪い例（リスト内包表記をVarに使用）
*[render_tile(t) for t in tiles]

# ✅ 良い例（rx.foreachを使用）
rx.foreach(tiles, render_tile)

# ❌ 悪い例（len()をVarに使用）
len(tiles) > 0

# ✅ 良い例（.length()を使用）
tiles.length() > 0
```

### 配列インデックスアクセス
Varを使って配列にインデックスアクセスできないため、計算プロパティを使用:
```python
@rx.var
def current_player_name(self) -> str:
    names = ["East", "South", "West", "North"]
    return names[self.current_player]
```

## よくあるタスク

### 新しい状態変数の追加
```python
# 1. Stateクラスに追加
class MahjongState(rx.State):
    new_variable: str = "default"

# 2. _sync_stateで同期（必要に応じて）
def _sync_state(self):
    self.new_variable = self._game.some_property

# 3. UIで使用
rx.text(MahjongState.new_variable)
```

## デバッグのヒント

**ブラウザコンソール**:
- DevTools（F12）を開く
- Consoleタブでエラーを確認
- Networkタブでリクエストを確認

**Reflexデバッグ**:
```bash
# デバッグログ付きで実行
reflex run --loglevel debug
```

## リソース

- [Reflexドキュメント](https://reflex.dev/docs)
- [Pythonの型ヒント](https://docs.python.org/3/library/typing.html)
- [麻雀ルール](https://riichi.wiki/)
- [プロジェクトアーキテクチャ](ARCHITECTURE.md)

## 次のステップ

セットアップ後:
1. コードベースを探索
2. アプリケーションを実行してテスト
3. [ARCHITECTURE.md](ARCHITECTURE.md)を読む
4. 小さな機能を追加してみる
5. 最初のPRを提出！
