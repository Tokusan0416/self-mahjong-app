# 🀄 Mahjong Self-Play Simulator

A web-based Mahjong simulator that allows you to play all four positions yourself. Designed for practice, game analysis, and generating training data for machine learning.

## ⚠️ Migration in Progress

**Status**: Currently migrating from Reflex to Flask (backend) + React (frontend) architecture.

- **Original Implementation**: Reflex 0.8 (Python full-stack)
- **New Architecture**: Flask + React (TypeScript)
- **Reason**: SVG tile image loading issues in Reflex static file serving
- **Game Engine**: 100% preserved (pure Python, framework-agnostic)
- **Timeline**: 3-4 working days

See [MIGRATION.md](MIGRATION.md) for detailed migration plan and progress.

## Features

- **Self-Play Mode**: Control all 4 players simultaneously
- **Full Visibility**: See all hands at once for analysis and learning
- **Game Logging**: Comprehensive JSON logs of all actions for BigQuery integration
- **Japanese Riichi Mahjong**: Implements standard Japanese mahjong rules
- **Interactive UI**: Click tiles to discard, check tenpai status, declare riichi
- **Modern Stack**: Built entirely in Python with Reflex (React frontend + FastAPI backend)

## Quick Start

### Current Version (Reflex - Limited Functionality)

**Prerequisites**:
- Python 3.11 or higher
- pip or uv package manager

**Note**: The current Reflex version has SVG image loading issues. Tiles display as text codes instead of images.

```bash
# Clone the repository
git clone <repository-url>
cd private-self-mahjong-reflex

# Install dependencies
pip install -e .
# Or: uv pip install -e .

# Initialize Reflex
reflex init

# Run the application
reflex run
```

The app will be available at `http://localhost:3000`

### New Version (Flask + React - Coming Soon)

**Prerequisites**:
- Python 3.11 or higher
- Node.js 18 or higher

**Status**: In development (Phase M1-M5)

```bash
# Backend (Flask)
cd backend
pip install -r requirements.txt
python run.py

# Frontend (React)
cd frontend
npm install
npm run dev
```

Backend: `http://localhost:5000` | Frontend: `http://localhost:5173`

## How to Play

1. **Start a New Game**: Click the "New Game" button to deal tiles to all 4 players
2. **Discard Tiles**: Click on any tile in the current player's hand to discard it
3. **Check Tenpai**: Use the "Check Tenpai" button to see which tiles complete your hand
4. **Declare Riichi**: When in tenpai, click "Declare Riichi" to commit to your hand
5. **Export Logs**: Click "Export Log" to save the game data (currently prints to console)

## Project Structure

### Current Structure (Reflex)

```
private-self-mahjong-reflex/
├── app/                      # Main application package
│   ├── engine/               # Game logic and rules (REUSABLE ✅)
│   │   ├── tiles.py          # Tile definitions and operations
│   │   ├── player.py         # Player state management
│   │   ├── game.py           # Core game loop and logic
│   │   ├── scoring.py        # Hand evaluation and scoring
│   │   └── hand_evaluator.py # Tenpai and yaku detection
│   ├── components/           # Reflex UI components (TO BE REWRITTEN)
│   │   ├── hand.py           # Hand and tile rendering
│   │   ├── board.py          # Board and controls
│   │   ├── tile_image.py     # Tile image components
│   │   ├── mahjong_table.py  # Table layout
│   │   └── ...               # Other UI components
│   ├── state.py              # Reflex state management
│   └── app.py                # Main Reflex application
├── assets/                   # Static assets
│   └── tiles/                # 43 SVG tile images (FluffyStuff)
├── docs/                     # Documentation
├── pyproject.toml            # Project dependencies
└── rxconfig.py               # Reflex configuration
```

### Planned Structure (Flask + React)

```
mahjong-flask-react/          # New project (to be created)
├── backend/                  # Flask application
│   ├── app/
│   │   ├── engine/           # ← COPIED from app/engine/ (100% reusable)
│   │   ├── routes.py         # REST API endpoints
│   │   └── socketio_events.py # WebSocket handlers
│   ├── static/tiles/         # ← COPIED from assets/tiles/
│   ├── requirements.txt      # Python dependencies
│   └── run.py                # Flask entry point
├── frontend/                 # React application
│   ├── src/
│   │   ├── components/       # React components (Tile, Hand, Board, etc.)
│   │   ├── hooks/            # Custom hooks (useGameState, useSocket)
│   │   ├── types/            # TypeScript type definitions
│   │   └── App.tsx           # Main React app
│   ├── package.json          # Node dependencies
│   └── vite.config.ts        # Vite configuration
├── MIGRATION.md              # Migration documentation
└── README.md                 # Updated documentation
```

## Documentation

- [Architecture Overview](docs/ARCHITECTURE.md) - System design and data flow
- [Usage Guide](docs/USAGE.md) - Detailed usage instructions
- [API Documentation](docs/API.md) - Engine API reference
- [Development Guide](docs/DEVELOPMENT.md) - Contributing and extending

## Roadmap

See [ROADMAP.md](ROADMAP.md) for the full development plan.

### Current Status: Phase 1-2.3 Complete ✅ + Migration in Progress ⚠️

**Reflex Version (Current)**:
- [x] Phase 1: Basic tile engine and game logic
- [x] Phase 2.1: Win detection (ron, tsumo) and full scoring
- [x] Phase 2.2: Meld calls (pon, chi, kan) with priority system
- [x] Phase 2.2.5: Hand organization (drawn tile separation, auto-sort)
- [x] Phase 2.3: Round management (exhaustive draw, dealer rotation, game types)
- [x] Phase 3.2: Cross-pattern table layout
- [x] Phase 3.3: End screens (exhaustive draw, game end, oorasu indicator)
- [⚠️] Phase 3.1: Tile graphics (SVG images not loading - **blocked**)

**Flask + React Migration (In Progress)**:
- [ ] Phase M1: Backend setup (Flask + SocketIO + game engine)
- [ ] Phase M2: Frontend setup (React + TypeScript + Vite)
- [ ] Phase M3: Core UI components (Tile, Hand, Board, MahjongTable)
- [ ] Phase M4: Game flow integration (state management, WebSocket)
- [ ] Phase M5: End screens & polish

**Next Steps**: Complete migration (estimated 3-4 days), then proceed to Phase 4 (BigQuery integration)

## Technologies

### Current Stack (Reflex - Being Phased Out)
- **[Reflex](https://reflex.dev/) 0.8**: Full-stack Python framework (React + FastAPI)
- **Python 3.11+**: Modern Python features and type hints
- **mahjong library**: Comprehensive yaku and scoring rules

### New Stack (Flask + React - In Progress)

**Backend**:
- **Flask 3.0+**: Lightweight Python web framework
- **Flask-SocketIO**: WebSocket support for real-time updates
- **Python 3.11+**: Modern Python with type hints
- **mahjong library**: Yaku and scoring (preserved from Reflex version)

**Frontend**:
- **React 18+**: Modern React with functional components and hooks
- **TypeScript**: Type-safe JavaScript
- **Vite**: Fast development server and optimized builds
- **TailwindCSS**: Utility-first CSS framework
- **Socket.IO Client**: Real-time communication with backend
- **Zustand**: Lightweight state management

## Future Features

- BigQuery integration for game data storage
- Advanced statistics and analytics
- Multiple round support (East/South rounds)
- Image assets for tiles
- Deployment to cloud platforms

## Contributing

Contributions are welcome! Please see [DEVELOPMENT.md](docs/DEVELOPMENT.md) for guidelines.

## License

This project is for personal use and educational purposes.

## Acknowledgments

- Built with [Reflex](https://reflex.dev/)
- Inspired by traditional Japanese Riichi Mahjong
- Designed for game analysis and ML training data generation

---

# 🀄 麻雀セルフプレイシミュレーター

[Reflex](https://reflex.dev/)で構築されたWebベースの麻雀シミュレーターで、4人全ての立場を自分で操作できます。練習、ゲーム分析、機械学習のトレーニングデータ生成を目的としています。

## 機能

- **セルフプレイモード**: 4人全員を同時にコントロール
- **完全可視化**: 分析と学習のため、全ての手牌を一度に表示
- **ゲームログ**: BigQuery統合用の包括的なJSON形式のアクションログ
- **日本式リーチ麻雀**: 標準的な日本麻雀ルールを実装
- **インタラクティブUI**: 牌をクリックして打牌、テンパイ状態の確認、立直宣言
- **モダンスタック**: Pythonのみで構築（Reflex: React フロントエンド + FastAPI バックエンド）

## クイックスタート

### 前提条件

- Python 3.11以上
- pipまたはuvパッケージマネージャー

### インストール

1. **リポジトリをクローン**:
```bash
git clone <repository-url>
cd private-self-mahjong-reflex
```

2. **依存関係をインストール**:
```bash
# pipを使用
pip install -e .

# またはuv（推奨）
uv pip install -e .
```

3. **Reflexを初期化**:
```bash
reflex init
```

4. **アプリケーションを実行**:
```bash
reflex run
```

アプリは `http://localhost:3000` で利用できます

## 遊び方

1. **新しいゲームを開始**: 「New Game」ボタンをクリックして、4人全員に牌を配る
2. **牌を捨てる**: 現在のプレイヤーの手牌の牌をクリックして打牌
3. **テンパイ確認**: 「Check Tenpai」ボタンで、どの牌で和了できるか確認
4. **立直宣言**: テンパイ時に「Declare Riichi」をクリックして手牌を固定
5. **ログのエクスポート**: 「Export Log」をクリックしてゲームデータを保存（現在はコンソールに出力）

## プロジェクト構造

```
private-self-mahjong-reflex/
├── app/                      # メインアプリケーションパッケージ
│   ├── engine/               # ゲームロジックとルール
│   │   ├── tiles.py          # 牌の定義と操作
│   │   ├── player.py         # プレイヤーの状態管理
│   │   ├── game.py           # コアゲームループとロジック
│   │   └── scoring.py        # 手牌評価と点数計算
│   ├── components/           # Reflex UIコンポーネント
│   │   ├── hand.py           # 手牌と牌のレンダリング
│   │   └── board.py          # 盤面とコントロール
│   ├── state.py              # Reflex状態管理
│   └── app.py                # メインReflexアプリケーション
├── docs/                     # ドキュメント
├── assets/                   # 静的アセット（画像など）
├── pyproject.toml            # プロジェクト依存関係
└── rxconfig.py               # Reflex設定
```

## ドキュメント

- [アーキテクチャ概要](docs/ARCHITECTURE.md) - システム設計とデータフロー
- [使い方ガイド](docs/USAGE.md) - 詳細な使用方法
- [APIドキュメント](docs/API.md) - エンジンAPIリファレンス
- [開発ガイド](docs/DEVELOPMENT.md) - 貢献と拡張

## ロードマップ

完全な開発計画は[ROADMAP.md](ROADMAP.md)を参照してください。

### 現在の状態: Phase 1完了 ✅

- [x] 基本的な牌エンジンとゲームロジック
- [x] 4人全員の手牌を表示するReflex UI
- [x] 打牌とターン進行
- [x] テンパイ判定
- [x] 立直宣言
- [x] ゲームログ記録

### 次のステップ: Phase 2

- [ ] 完全な和了判定（ツモとロン）
- [ ] `mahjong`ライブラリを使った役判定
- [ ] 点数計算
- [ ] 鳴き（ポン、チー、カン）

## 使用技術

- **[Reflex](https://reflex.dev/)**: フルスタックPythonフレームワーク（React + FastAPI）
- **Python 3.11+**: モダンなPython機能と型ヒント
- **mahjongライブラリ**: 包括的な役と点数計算ルール用（予定）

## 将来の機能

- ゲームデータ保存のためのBigQuery統合
- 高度な統計と分析
- 複数局のサポート（東場・南場）
- 牌の画像アセット
- クラウドプラットフォームへのデプロイ

## 貢献

貢献を歓迎します！ガイドラインは[DEVELOPMENT.md](docs/DEVELOPMENT.md)を参照してください。

## ライセンス

このプロジェクトは個人利用および教育目的です。

## 謝辞

- [Reflex](https://reflex.dev/)で構築
- 伝統的な日本のリーチ麻雀にインスパイア
- ゲーム分析とML訓練データ生成用に設計
