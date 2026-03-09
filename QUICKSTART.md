# Quick Start Guide

Get up and running with the Mahjong Self-Play Simulator in 5 minutes.

## Installation

```bash
# 1. Install dependencies
pip install -e .

# 2. Initialize Reflex (first time only)
reflex init

# 3. Run the application
reflex run
```

Open your browser to `http://localhost:3000`

## First Steps

1. **Click "New Game"** - Deals tiles to all 4 players
2. **Click any tile** in the current player's hand to discard it
3. **Click "Check Tenpai"** - See which tiles complete your hand
4. **Click "Declare Riichi"** - Commit to your hand when in tenpai

## Game Flow

```
East (14 tiles) → Click tile to discard → Turn advances
  ↓
South (auto-draws) → Click tile to discard → Turn advances
  ↓
West (auto-draws) → Click tile to discard → Turn advances
  ↓
North (auto-draws) → Click tile to discard → Turn advances
  ↓
Back to East...
```

## Understanding the Interface

### Current Player
- **Blue border** = It's their turn
- **Click tiles** to discard (only when it's your turn)

### Game Board (Center)
- Shows whose turn it is
- Displays remaining tiles in wall
- Shows dora indicators

### Player Displays
- **Top**: Player name, score, [RIICHI] status
- **Middle**: Hand tiles (click to discard)
- **Bottom**: Discard pile (河)

## Quick Reference

### Tile Notation
- `1m-9m`: Manzu (萬子, characters)
- `1p-9p`: Pinzu (筒子, dots)
- `1s-9s`: Souzu (索子, bamboo)
- `1z-7z`: Honors (winds 1-4, dragons 5-7)

### Winning Hand Structure
- 4 melds (3 tiles each) + 1 pair (2 tiles)
- **Triplet**: 5m 5m 5m
- **Sequence**: 3p 4p 5p
- **Pair**: 7z 7z

### Tenpai (Ready)
- One tile away from winning
- Use "Check Tenpai" button to verify

### Riichi
- **Requirements**: 13 tiles, in tenpai, 1000+ points, no open melds
- **Cost**: 1000 points deposit
- **Benefit**: +1 han bonus when you win

## Example Game

```
1. Click "New Game"
   → All players receive 13 tiles, East gets 14

2. East's turn (you see 14 tiles)
   → Click "9m" to discard
   → Turn advances to South

3. South's turn (auto-drew a tile, now 14)
   → Click "8s" to discard
   → Turn advances to West

4. Continue playing all 4 positions...

5. When you have 13 tiles and might be close to winning:
   → Click "Check Tenpai"
   → If shows "Waiting for: 4m 7m" → You're ready!

6. Declare Riichi:
   → Click "Declare Riichi"
   → Status shows [RIICHI]
   → Keep playing until you win

7. Export your game:
   → Click "Export Log"
   → Check console (F12) for JSON data
```

## Troubleshooting

**Can't click tiles?**
- Only current player's tiles are clickable
- Look for blue border indicating current player

**Riichi won't work?**
- Click "Check Tenpai" first
- Must have exactly 13 tiles
- Need 1000+ points

**Game seems stuck?**
- Check if wall is empty (game ends)
- Refresh page if needed

## Next Steps

- [Full Usage Guide](docs/USAGE.md) - Complete gameplay instructions
- [Architecture](docs/ARCHITECTURE.md) - How the system works
- [API Reference](docs/API.md) - Developer documentation
- [Development Guide](docs/DEVELOPMENT.md) - Contributing

## Need Help?

Check the documentation:
- [README.md](README.md) - Project overview
- [USAGE.md](docs/USAGE.md) - Detailed usage
- [ROADMAP.md](ROADMAP.md) - Future plans

Enjoy playing! 🀄

---

# クイックスタートガイド

麻雀セルフプレイシミュレーターを5分で起動して実行できます。

## インストール

```bash
# 1. 依存関係をインストール
pip install -e .

# 2. Reflexを初期化（初回のみ）
reflex init

# 3. アプリケーションを実行
reflex run
```

ブラウザで `http://localhost:3000` を開く

## 最初のステップ

1. **「New Game」をクリック** - 4人全員に牌を配る
2. **現在のプレイヤーの手牌の牌をクリック** - 打牌する
3. **「Check Tenpai」をクリック** - どの牌で和了できるか確認
4. **「Declare Riichi」をクリック** - テンパイ時に手牌を固定

## ゲームの流れ

```
東家（14枚） → 牌をクリックして打牌 → ターン進行
  ↓
南家（自動ツモ） → 牌をクリックして打牌 → ターン進行
  ↓
西家（自動ツモ） → 牌をクリックして打牌 → ターン進行
  ↓
北家（自動ツモ） → 牌をクリックして打牌 → ターン進行
  ↓
東家に戻る...
```

## インターフェースの理解

### 現在のプレイヤー
- **青い枠線** = そのプレイヤーのターン
- **牌をクリック** - 打牌（自分のターンのみ）

### ゲームボード（中央）
- 現在誰のターンかを表示
- 山に残っている牌の数を表示
- ドラ表示牌を表示

### プレイヤー表示
- **上部**: プレイヤー名、点数、[RIICHI]ステータス
- **中央**: 手牌（クリックで打牌）
- **下部**: 捨て牌（河）

## クイックリファレンス

### 牌の表記
- `1m-9m`: 萬子（マンズ）
- `1p-9p`: 筒子（ピンズ）
- `1s-9s`: 索子（ソーズ）
- `1z-7z`: 字牌（風牌1-4、三元牌5-7）

### 和了形
- 4面子（各3枚） + 1雀頭（2枚）
- **刻子**: 5m 5m 5m
- **順子**: 3p 4p 5p
- **雀頭**: 7z 7z

### テンパイ（聴牌）
- あと1枚で和了
- 「Check Tenpai」ボタンで確認

### リーチ
- **条件**: 13枚、テンパイ、1000点以上、鳴きなし
- **コスト**: 1000点供託
- **メリット**: 和了時+1翻ボーナス

## ゲーム例

```
1. 「New Game」をクリック
   → 全プレイヤーが13枚、東家は14枚受け取る

2. 東家のターン（14枚表示）
   → 「9m」をクリックして打牌
   → 南家のターンに進む

3. 南家のターン（自動ツモで14枚に）
   → 「8s」をクリックして打牌
   → 西家のターンに進む

4. 4つの立場を続けてプレイ...

5. 13枚で和了が近いとき:
   → 「Check Tenpai」をクリック
   → 「Waiting for: 4m 7m」と表示 → テンパイ！

6. リーチ宣言:
   → 「Declare Riichi」をクリック
   → ステータスに[RIICHI]表示
   → 和了まで続行

7. ゲームをエクスポート:
   → 「Export Log」をクリック
   → コンソール（F12）でJSONデータを確認
```

## トラブルシューティング

**牌がクリックできない？**
- 現在のプレイヤーの牌のみクリック可能
- 青い枠線で現在のプレイヤーを確認

**リーチが宣言できない？**
- 先に「Check Tenpai」をクリック
- 13枚である必要がある
- 1000点以上必要

**ゲームが進まない？**
- 山が空か確認（ゲーム終了）
- 必要に応じてページを更新

## 次のステップ

- [完全な使い方ガイド](docs/USAGE.md) - 完全なゲームプレイ説明
- [アーキテクチャ](docs/ARCHITECTURE.md) - システムの仕組み
- [APIリファレンス](docs/API.md) - 開発者向けドキュメント
- [開発ガイド](docs/DEVELOPMENT.md) - 貢献方法

## サポートが必要？

ドキュメントを確認:
- [README.md](README.md) - プロジェクト概要
- [USAGE.md](docs/USAGE.md) - 詳細な使い方
- [ROADMAP.md](ROADMAP.md) - 今後の計画

楽しんでください！🀄
