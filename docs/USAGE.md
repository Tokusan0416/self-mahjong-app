# Usage Guide

Complete guide to using the Mahjong Self-Play Simulator.

## Table of Contents

- [Getting Started](#getting-started)
- [Basic Gameplay](#basic-gameplay)
- [Game Controls](#game-controls)
- [Understanding the Interface](#understanding-the-interface)
- [Advanced Features](#advanced-features)
- [Tips and Best Practices](#tips-and-best-practices)

## Getting Started

### First Time Setup

1. **Install dependencies**:
```bash
pip install -e .
```

2. **Initialize Reflex** (first time only):
```bash
reflex init
```

3. **Start the development server**:
```bash
reflex run
```

4. **Open your browser**:
Navigate to `http://localhost:3000`

### Starting Your First Game

1. Click the **"New Game"** button at the top of the page
2. The system will automatically:
   - Create and shuffle 136 tiles
   - Deal 13 tiles to each of 4 players
   - Give the East player (dealer) an extra 14th tile
   - Display all hands and start the game

## Basic Gameplay

### The Turn Flow

The game follows standard Mahjong turn flow:

1. **Current Player** (highlighted with blue border):
   - Has 14 tiles in hand
   - Must discard one tile

2. **Discarding**:
   - Click any tile in the current player's hand
   - Tile moves to that player's discard pile
   - Turn automatically advances to next player

3. **Auto-Draw**:
   - Next player automatically draws a tile from the wall
   - Now has 14 tiles and can discard

4. **Repeat** until someone wins or the wall is empty

### Example Turn Sequence

```
East's Turn:
  Hand: [1m, 1m, 2m, 3m, 4m, 5m, 6m, 7m, 8m, 9m, 1p, 1p, 1p, 2p]
  → Click 9m to discard
  → 9m moves to East's discard pile
  → Turn advances to South

South's Turn:
  Auto-draws: 3s
  Hand: [1s, 2s, 3s, 4s, 5s, 6s, 7s, 8s, 9s, 1z, 1z, 1z, 2z, 3s]
  → Ready to discard
```

## Game Controls

### Main Control Buttons

Located at the top of the page:

#### New Game
- **Purpose**: Start a fresh game
- **Action**: Resets all state and deals new tiles
- **When to use**:
  - Starting your first game
  - After a game ends
  - When you want to practice a new scenario

#### Check Tenpai
- **Purpose**: Check if you're one tile away from winning
- **Action**: Shows which tiles would complete your hand
- **When to use**:
  - After organizing your hand
  - Before declaring Riichi
  - To see if you should change strategy

**Example Output**:
```
Waiting for: 4m 7m
```
This means either 4m or 7m would complete your hand.

#### Declare Riichi
- **Purpose**: Commit to your current hand (no more changes)
- **Requirements**:
  - Must have exactly 13 tiles (after discarding)
  - Must be in tenpai (one tile from winning)
  - Must have at least 1000 points
  - Cannot have any open melds
- **Cost**: 1000 points deposit
- **Effect**:
  - Marks player as "RIICHI"
  - Adds 1 han to winning hand
  - Cannot change hand after declaration

#### Export Log
- **Purpose**: Save game data for analysis
- **Action**: Prints JSON log to console
- **When to use**:
  - After completing a game
  - For analysis or debugging
  - Before importing to BigQuery (future feature)

## Understanding the Interface

### Game Board (Center)

Displays current game status:

```
┌─────────────────────────────────────────────┐
│              Game Board                      │
├─────────────────────────────────────────────┤
│ Current Player: East (Position 0)           │
│ Turn: 12                                     │
│ Wall Remaining: 58 tiles left                │
│ Dora Indicators: 5s                          │
└─────────────────────────────────────────────┘
```

**Key Information**:
- **Current Player**: Who must discard now
- **Turn**: Total number of turns taken
- **Wall Remaining**: Tiles left to draw
- **Dora Indicators**: Bonus tiles (tile after indicator adds value)

### Player Displays

Each player has two sections:

#### Hand Section
```
┌─────────────────────────────────────────────┐
│ East (25000) [RIICHI]                        │
│ ┌──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┐   │
│ │1m│2m│3m│4m│5m│6m│7m│8m│9m│1p│1p│1p│2p│   │
│ └──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┘   │
└─────────────────────────────────────────────┘
```

- **Player Name**: Wind position (East/South/West/North)
- **Score**: Current points
- **[RIICHI]**: Shows if player has declared Riichi
- **Tiles**: All tiles in hand (clickable when it's your turn)

#### Discard Pile
```
┌─────────────────────────────────────────────┐
│ East's discards:                             │
│ 9p 8s 7z 3m 4p 2s...                        │
└─────────────────────────────────────────────┘
```

Shows all tiles this player has discarded in order.

### Info Panel

Shows important messages and waiting tiles:

```
┌─────────────────────────────────────────────┐
│ ℹ East discarded 3m. Now South's turn.     │
├─────────────────────────────────────────────┤
│ Waiting for: 4m 7m                          │
│ ┌──┬──┐                                     │
│ │4m│7m│                                     │
│ └──┴──┘                                     │
└─────────────────────────────────────────────┘
```

## Advanced Features

### Checking for Tenpai

Tenpai means you're one tile away from a complete hand.

**Steps**:
1. Click **"Check Tenpai"** button
2. If in tenpai, you'll see waiting tiles
3. If not, message says "Not in tenpai yet"

**What Makes a Complete Hand**:
- 4 melds (3 tiles each) + 1 pair (2 tiles)
- Melds can be:
  - **Triplet (Pon)**: Three identical tiles (e.g., 5m 5m 5m)
  - **Sequence (Chi)**: Three consecutive tiles same suit (e.g., 3p 4p 5p)
- Pair: Two identical tiles (e.g., 7z 7z)

**Example**:
```
Hand: 1m 2m 3m 4p 5p 6p 7s 8s 9s 1z 1z 1z 2z

Melds:
- 1m 2m 3m (sequence)
- 4p 5p 6p (sequence)
- 7s 8s 9s (sequence)
- 1z 1z 1z (triplet)

Waiting: 2z (to make pair)
```

### Declaring Riichi

Riichi is a powerful declaration that adds value to your hand.

**Pre-Riichi Checklist**:
- [ ] Have exactly 13 tiles (ready to discard)
- [ ] In tenpai (verified with Check Tenpai button)
- [ ] Have 1000+ points
- [ ] No open melds
- [ ] Confident in your waiting tiles

**Steps**:
1. Organize hand and verify tenpai
2. Click **"Declare Riichi"**
3. If successful, your display shows **[RIICHI]**
4. Score decreases by 1000 (deposit)
5. Continue discarding normally

**After Riichi**:
- You cannot change your hand composition
- Must continue discarding tiles automatically
- Win gives +1 han bonus
- Get 1000 points back on win

### Understanding Tile Notation

All tiles use a simple string format:

**Number Tiles** (1-9 + suit):
- `1m` - `9m`: Manzu (萬子, characters)
- `1p` - `9p`: Pinzu (筒子, dots/circles)
- `1s` - `9s`: Souzu (索子, bamboo)

**Honor Tiles** (1-7 + z):
- `1z`: East wind (東)
- `2z`: South wind (南)
- `3z`: West wind (西)
- `4z`: North wind (北)
- `5z`: White dragon (白)
- `6z`: Green dragon (發)
- `7z`: Red dragon (中)

## Tips and Best Practices

### Strategy Tips

1. **Look for Patterns**: Try to form sequences and triplets
2. **Keep Flexibility**: Keep tiles that can form multiple combinations
3. **Watch Discards**: See what others are throwing away
4. **Riichi Timing**: Don't riichi too early if wall is almost empty

### Learning Tips

1. **Practice Hand Reading**: Try to spot complete hands
2. **Use Check Tenpai Often**: Learn what makes a hand "ready"
3. **Experiment with All Positions**: Play through entire games
4. **Study Discards**: Look at patterns in your own discards

### Common Patterns to Recognize

**Waiting on Two Sides** (良形待ち):
```
Hand: 3m 4m 5m 6m
Waiting: 2m or 7m (both complete a sequence)
```

**Waiting on One Tile** (単騎待ち):
```
Hand: [Complete melds] + 5p
Waiting: 5p only (to make pair)
```

**Waiting in Middle** (嵌張待ち):
```
Hand: 3m 5m
Waiting: 4m only (to complete 3-4-5)
```

### Using the Export Log

The game log contains valuable data:

```json
{
  "game_state": { ... },
  "actions": [
    {
      "turn": 1,
      "player": 0,
      "action_type": "discard",
      "tile": "9m",
      "timestamp": "2026-03-09T10:30:45.123456"
    },
    ...
  ]
}
```

**Current Usage**:
- Printed to browser console (F12 → Console)
- Copy and save to file for analysis

**Future Usage** (Phase 3):
- Automatic upload to BigQuery
- Statistical analysis dashboards
- Machine learning training data

## Troubleshooting

### Game Won't Start
- Check console for errors (F12)
- Try refreshing the page
- Verify dependencies are installed

### Tiles Not Clickable
- Check if it's the current player's turn (blue border)
- Only current player's tiles are clickable
- Ensure game is not over

### Riichi Won't Declare
- Verify tenpai with "Check Tenpai" button
- Ensure you have 13 tiles (after discarding)
- Check score is 1000+
- No open melds allowed

### Wall Empty
- Game ends when wall reaches 0
- Start a new game to continue playing

## Next Steps

Once comfortable with basic gameplay:
1. Try different hand patterns
2. Practice tenpai recognition
3. Experiment with riichi timing
4. Study the game logs
5. Prepare for Phase 2 features (full scoring)

For development and customization, see [DEVELOPMENT.md](DEVELOPMENT.md).

---

# 使い方ガイド（日本語要約）

## 基本的な遊び方

### ゲームの流れ
1. **「New Game」** - ゲーム開始、4人に牌を配る
2. **牌をクリック** - 現在のプレイヤー（青枠）の手牌をクリックして打牌
3. **自動ツモ** - 次のプレイヤーが自動的にツモ
4. **繰り返し** - 東→南→西→北の順で進行

### インターフェース

**ゲームボード（中央）**:
- 現在のプレイヤー
- ターン数
- 山の残り枚数
- ドラ表示牌

**プレイヤー表示**:
- 名前と点数（青枠=現在のプレイヤー）
- 手牌（クリック可能）
- 捨て牌（河）

### 主要機能

**テンパイチェック**:
- 「Check Tenpai」ボタンをクリック
- 待ち牌が表示される
- 例: 「Waiting for: 4m 7m」

**立直宣言**:
- 条件: 13枚、テンパイ、1000点以上、鳴きなし
- 「Declare Riichi」をクリック
- コスト: 1000点供託
- メリット: 和了時+1翻

**ログのエクスポート**:
- 「Export Log」をクリック
- コンソール（F12）にJSON形式で出力
- 将来的にBigQueryに送信予定

## 牌の表記

- **萬子**: 1m-9m
- **筒子**: 1p-9p
- **索子**: 1s-9s
- **字牌**: 1z(東), 2z(南), 3z(西), 4z(北), 5z(白), 6z(發), 7z(中)

## 和了形

**基本構造**: 4面子 + 1雀頭
- **面子**: 刻子（5m 5m 5m）または順子（3p 4p 5p）
- **雀頭**: 同じ牌2枚（7z 7z）

## 待ちの種類

**両面待ち**: 3m 4m → 2mまたは5m待ち
**単騎待ち**: [完成形] + 5p → 5p待ち
**嵌張待ち**: 3m 5m → 4m待ち

## トラブルシューティング

**牌がクリックできない**: 青枠の現在のプレイヤーのみクリック可能
**立直できない**: テンパイを確認、13枚、1000点以上
**ゲームが進まない**: 山が空（ゲーム終了）、ページを更新

## 練習のヒント

1. 手牌の読み方を練習
2. テンパイチェックを頻繁に使用
3. 4つの立場を全て経験
4. 捨て牌のパターンを研究
