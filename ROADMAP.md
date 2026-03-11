# Development Roadmap

This document outlines the development plan for the Mahjong Self-Play Simulator, from the current state to production deployment.

## Project Vision

Build a web-based mahjong simulator where one person can play all four positions, with complete game logging for analysis and machine learning training data generation.

### Core Goals

1. **Self-Play Experience**: Enable practice and analysis by controlling all 4 players
2. **Data Collection**: Capture comprehensive game logs for BigQuery analytics
3. **Learning Tool**: Visualize all hands simultaneously for study and improvement
4. **ML Pipeline**: Generate training data for mahjong AI development

---

## Current Status: Phase 2.1 & 2.2 Complete ✅

### Implemented Features

**Phase 1 - Core Foundation:**
- [x] **Tile Engine**: 136-tile pool with shuffling and distribution
- [x] **Game Logic**: Turn management, draw/discard mechanics, wall management
- [x] **Player Management**: 4-player state with hands, discards, scores, riichi status
- [x] **Reflex UI**: Interactive web interface with all 4 player displays
- [x] **Tenpai Detection**: Check waiting tiles for 13-tile hands
- [x] **Riichi Declaration**: Full riichi implementation with validation
- [x] **Game Logging**: JSON logging of all game actions with timestamps
- [x] **Basic Hand Evaluation**: Simplified win detection (4 melds + 1 pair)

**Phase 2.1 - Winning Detection & Scoring:**
- [x] **Ron Detection**: Win on discard with proper validation and scoring
- [x] **Tsumo Detection**: Self-draw win with correct payment distribution
- [x] **Yaku Integration**: Complete yaku detection using `mahjong` library
- [x] **Score Calculation**: Full han/fu to points conversion with dealer/non-dealer handling
- [x] **Win Display**: Detailed win information showing yaku, han, fu, and points

**Phase 2.2 - Meld Calls (Naki):**
- [x] **Pon Implementation**: Triple calls with UI buttons and turn flow
- [x] **Chi Implementation**: Sequence calls (from previous player only)
- [x] **Kan Detection**: Quad call detection (daiminkan, ankan, shouminkan)
- [x] **Call Priority System**: Ron > Kan > Pon > Chi with proper handling
- [x] **Pass on Calls**: Ability to skip all call opportunities
- [x] **Meld Display**: Visual representation of called melds

**Phase 2.2.5 - Hand Organization (Partial from Phase 3):**
- [x] **Drawn Tile Separation**: Last drawn tile displayed separately on the right
- [x] **Auto-sort Hand**: Hand automatically sorted after discarding
- [x] **Visual Clarity**: Improved hand readability with proper spacing

**Phase 2.3 - Round Management:**
- [x] **Exhaustive Draw**: Detect流局 when wall empties, with tenpai/noten status and payments
- [x] **Dealer Rotation**: 連荘 (dealer wins/tenpai) vs 輪荘 (dealer rotates)
- [x] **Round Progression**: East 1-4 → South 1-4 with proper tracking
- [x] **Game Types**: Support for 半荘 (hanchan, default) and 東風戦 (tonpuu)
- [x] **Game Completion**: Detect game end after final round

### Technical Foundation

- Reflex 0.8 with reactive state management
- Clean separation: `app/engine/` (pure Python) and `app/components/` (UI)
- Type-safe codebase with comprehensive docstrings
- Modular architecture ready for expansion
- Integration with `mahjong` library for authentic scoring

---

## Phase 2: Core Game Features ✅ (2.1 & 2.2 Complete)

**Goal**: Complete the fundamental mahjong game mechanics

### 2.1 Winning Detection & Scoring ✅ COMPLETE

**Priority**: HIGH

- [x] **Ron (ロン) - Winning on Discard**
  - Detect when any player can win on another's discard ✅
  - Show "Ron" button to eligible players ✅
  - Handle furiten (振聴) rules (TODO: full furiten)
  - Priority handling (dealer vs non-dealer) ✅

- [x] **Tsumo (ツモ) - Self-Draw Win**
  - Auto-detect winning hand on draw ✅
  - Show "Tsumo" button to current player ✅
  - Calculate payment from all players ✅

- [x] **Yaku Integration**
  - Integrate `mahjong` library for complete yaku detection ✅
  - Display winning hand breakdown (yaku names, han, fu) ✅
  - Implement all standard yaku (38+ types) ✅
  - Handle multiple yaku combinations ✅

- [x] **Score Calculation**
  - Full point calculation based on han/fu ✅
  - Handle special cases: dealer wins, multiple rons, etc. ✅
  - Display score changes with animations (basic display) ✅
  - Update player scores correctly ✅

**Completed**: 2025-03-10

### 2.2 Meld Calls (Naki - 鳴き) ✅ COMPLETE

**Priority**: HIGH

- [x] **Pon (ポン) - Triple Call**
  - Detect when player can call pon on discard ✅
  - Show "Pon" button with timeout ✅
  - Move tiles from hand to meld area ✅
  - Skip player's draw, require immediate discard ✅

- [x] **Chi (チー) - Sequence Call**
  - Detect valid chi patterns (only from previous player) ✅
  - Show chi options if multiple patterns possible ✅
  - Lower priority than pon/kan ✅
  - Update display to show open meld ✅

- [x] **Kan (カン) - Quad**
  - **Daiminkan (大明槓)**: Open kan from discard ✅
  - **Ankan (暗槓)**: Concealed kan from hand (detection ready)
  - **Shouminkan (小明槓)**: Added kan to existing pon (detection ready)
  - Draw replacement tile from dead wall (TODO)
  - Reveal new dora indicator (TODO)

- [x] **Priority System**
  - Ron > Kan > Pon > Chi priority order ✅
  - Handle multiple simultaneous calls ✅
  - Proper turn flow after calls ✅

**Completed**: 2025-03-10

**Notes**:
- UI visibility fix applied (tile text color corrected)
- Kan replacement tile draw and additional dora reveal need implementation
- Furiten detection needs enhancement for complete rule compliance

### 2.2.5 Hand Organization (Early UI Improvements) ✅ COMPLETE

**Priority**: HIGH (pulled forward from Phase 3)

- [x] **Drawn Tile Separation**
  - Last drawn tile displayed separately on the right ✅
  - Visual spacing between main hand and drawn tile ✅
  - Improves hand readability significantly ✅

- [x] **Auto-sort Hand**
  - Hand automatically sorted after discarding ✅
  - Maintains traditional mahjong tile organization ✅
  - Helps players quickly identify patterns ✅

**Completed**: 2025-03-11

**Implementation Details**:
- Added `last_drawn_tile` attribute to Player class
- Modified `draw_tile()` to track the drawn tile
- Modified `discard_tile()` to clear drawn tile and auto-sort hand
- Updated UI to display main hand (13 tiles) and drawn tile (1 tile) separately
- Drawn tile shown with 16px spacing for visual clarity

### 2.3 Round Management ✅ COMPLETE

**Priority**: MEDIUM

- [x] **End-of-Round Handling**
  - Detect exhaustive draw (流局) ✅
  - Show tenpai/noten status ✅
  - Calculate noten payments (3000 point distribution) ✅
  - Handle dealer rotation (連荘 vs 輪荘) ✅

- [x] **Multiple Rounds**
  - Support full East round (東場 4 rounds) ✅
  - Optional South round (南場) ✅
  - Track round wind and dealer position ✅
  - Game type selection: 半荘 (hanchan) and 東風戦 (tonpuu) ✅

- [x] **Game Completion**
  - Detect game end conditions ✅
  - Round progression with proper game termination ✅
  - UI display of current round and game type ✅

**Completed**: 2026-03-11

**Implementation Details**:
- Added `game_type` parameter to `MahjongGame.__init__()` (default: "hanchan")
- Implemented round tracking: `round_wind`, `round_number`, `honba_sticks`, `riichi_sticks`
- Created `handle_exhaustive_draw()`: checks all players' tenpai status, distributes noten payments
- Created `handle_round_end_after_win()`: manages dealer rotation based on winner
- Created `advance_round()`: progresses rounds and handles game end detection
- Modified `advance_turn()` to detect exhaustive draw when wall empties
- Modified `declare_tsumo()` and `declare_ron()` to trigger round end handling
- Updated UI with game type buttons and round display (e.g., "東1局 2本場")
- Dealer continues (連荘) if dealer wins or is tenpai at exhaustive draw
- Dealer rotates (輪荘) if dealer loses or is noten at exhaustive draw

---

## Phase 3: UI/UX Improvements (3-4 weeks)

**Goal**: Create a polished, game-like experience

### 3.1 Tile Graphics

**Priority**: HIGH

- [ ] **Tile Image Assets**
  - Source or create tile images (SVG or PNG)
  - Standard size: ~50x70px for regular display
  - Rotated versions for discards
  - Dora indicator styling

- [ ] **Image Integration**
  - Replace text tiles ("1m") with images
  - Maintain accessibility (alt text, title attributes)
  - Optimize image loading and caching
  - Support both horizontal and vertical display

- [ ] **Visual Polish**
  - Smooth tile animations (discard, draw, meld)
  - Hover effects and active states
  - Tile shadows and depth
  - Color-coding for tile suits

**Estimated Time**: 1-2 weeks

### 3.2 Layout Improvements

**Priority**: MEDIUM

- [ ] **Traditional Mahjong Layout**
  - Position players in cross pattern (上下左右)
  - Center area for discards (like real table)
  - Proper wall visualization
  - Dora display area

- [ ] **Player Position Views**
  - Bottom: Current player (primary focus)
  - Right: Next player (kamicha - 上家)
  - Top: Opposite player (toimen - 対面)
  - Left: Previous player (shimocha - 下家)

- [ ] **Responsive Design**
  - Desktop: full 4-player view
  - Tablet: compact layout
  - Mobile: focus on current player (optional)
  - Proper scaling for different screen sizes

**Estimated Time**: 1-2 weeks

### 3.3 Enhanced Interactions

**Priority**: MEDIUM

- [ ] **Action Buttons**
  - Context-aware button visibility
  - Keyboard shortcuts (R: Riichi, T: Tsumo, etc.)
  - Auto-hide irrelevant actions
  - Confirmation dialogs for important actions

- [ ] **Game Information Display**
  - Dora count with indicators
  - Remaining tiles in wall
  - Current round and dealer indicator
  - Turn timer (optional)

- [ ] **Hand Organization**
  - ~~Auto-sort hand option~~ ✅ **Completed in Phase 2.2.5**
  - ~~Drawn tile separation~~ ✅ **Completed in Phase 2.2.5**
  - Manual tile arrangement (drag-and-drop)
  - Visual tenpai hints
  - Tile grouping suggestions

**Estimated Time**: 1 week (reduced to ~3-4 days due to Phase 2.2.5 completion)

---

## Phase 4: Data Collection & BigQuery (2-3 weeks)

**Goal**: Complete logging pipeline for analytics

### 4.1 Enhanced Logging

**Priority**: HIGH

- [ ] **Comprehensive Game State Logging**
  - Full hand state at each decision point
  - All player scores at each turn
  - Remaining wall count
  - Dora indicators revealed
  - Wind/round information

- [ ] **Action Metadata**
  - Differentiate tedashi (手出し) vs tsumo-giri (ツモ切り)
  - Capture decision timing
  - Log visible information vs hidden state
  - Include winning hand details (yaku, han, fu)

- [ ] **Structured Log Format**
  ```json
  {
    "game_id": "uuid",
    "timestamp": "ISO8601",
    "round": {"wind": "east", "round_number": 1, "honba": 0},
    "players": [
      {
        "position": 0,
        "hand": ["1m", "2m", ...],
        "discards": [...],
        "score": 25000,
        "is_riichi": false
      }
    ],
    "action": {
      "type": "discard",
      "player": 0,
      "tile": "3m",
      "is_tedashi": true
    },
    "game_state": {
      "wall_remaining": 70,
      "dora_indicators": ["5s"]
    }
  }
  ```

**Estimated Time**: 1 week

### 4.2 BigQuery Integration

**Priority**: MEDIUM

- [ ] **BigQuery Setup**
  - Create GCP project and dataset
  - Define table schema
  - Setup authentication (service account)
  - Implement connection pooling

- [ ] **Data Pipeline**
  - Batch upload on game completion
  - Async upload to avoid blocking UI
  - Retry logic for failed uploads
  - Local cache for offline mode

- [ ] **Query Examples**
  - Most common discards by position
  - Riichi success rate analysis
  - Winning hand statistics
  - Player decision patterns

**Estimated Time**: 1-2 weeks

---

## Phase 5: Advanced Features & Deployment (4-6 weeks)

**Goal**: Production-ready application with advanced capabilities

### 5.1 Analysis & Statistics

**Priority**: MEDIUM

- [ ] **In-App Statistics**
  - Win rate by position
  - Average han per win
  - Most common yaku
  - Riichi success/failure rate

- [ ] **Game Replay**
  - Save complete game state
  - Step through game turn-by-turn
  - Alternative decision analysis ("what if")
  - Export replay data

- [ ] **Visualization Dashboard**
  - Score progression charts
  - Tile efficiency analysis
  - Decision tree visualization
  - Comparison with optimal play

**Estimated Time**: 2 weeks

### 5.2 Performance Optimization

**Priority**: LOW-MEDIUM

- [ ] **Frontend Optimization**
  - Lazy load images
  - Memoize expensive computations
  - Reduce state updates
  - Code splitting

- [ ] **Backend Optimization**
  - Cache tenpai calculations
  - Optimize hand evaluation
  - Database query optimization
  - CDN for static assets

**Estimated Time**: 1 week

### 5.3 Testing & Quality Assurance

**Priority**: HIGH (before deployment)

- [ ] **Unit Tests**
  - Tile engine logic
  - Hand evaluation
  - Score calculation
  - Player state management

- [ ] **Integration Tests**
  - Full game flow
  - State synchronization
  - BigQuery upload
  - Error handling

- [ ] **E2E Tests**
  - UI interactions
  - Complete game scenarios
  - Edge cases (multiple rons, etc.)

**Estimated Time**: 1-2 weeks

### 5.4 Deployment

**Priority**: MEDIUM

- [ ] **Production Build**
  - Environment configuration
  - Secrets management
  - Error logging (Sentry, etc.)
  - Analytics (optional)

- [ ] **Hosting Options**
  - **Option A**: Reflex Cloud (easiest)
  - **Option B**: Docker + GCP Cloud Run
  - **Option C**: Docker + AWS ECS
  - **Option D**: Traditional VPS

- [ ] **CI/CD Pipeline**
  - Automated testing
  - Build and deploy on merge
  - Staging environment
  - Rollback capability

**Estimated Time**: 1-2 weeks

---

## Technical Considerations

### Architecture Decisions

**State Management**
- Continue using Reflex reactive state
- Consider Redis for session persistence (future)
- WebSocket for real-time updates (future multiplayer)

**Tile Images**
- SVG preferred for scalability
- Fallback to PNG for compatibility
- Consider sprite sheets for performance
- License: Use open-source assets or create custom

**BigQuery Schema Design**
```sql
-- games table
CREATE TABLE games (
  game_id STRING PRIMARY KEY,
  started_at TIMESTAMP,
  completed_at TIMESTAMP,
  total_rounds INT64,
  players ARRAY<STRUCT<position INT64, final_score INT64>>
);

-- actions table (partitioned by date)
CREATE TABLE actions (
  game_id STRING,
  action_id STRING,
  timestamp TIMESTAMP,
  turn_number INT64,
  player_position INT64,
  action_type STRING,
  action_data JSON,
  game_state JSON
)
PARTITION BY DATE(timestamp);
```

### Performance Targets

- **Page Load**: < 2 seconds
- **Action Response**: < 100ms
- **BigQuery Upload**: Async, non-blocking
- **Memory Usage**: < 200MB per session

### Security Considerations

- Input validation for all user actions
- Rate limiting on API endpoints
- Secure BigQuery credentials
- HTTPS only in production
- CORS configuration

---

## Future Enhancements (Post v1.0)

### Potential Features

- [ ] **AI Opponent**: Integrate ML model for single-player mode
- [ ] **Multiplayer Mode**: Real-time games with multiple users
- [ ] **Rule Variants**: Support for different mahjong rulesets
- [ ] **Tournament Mode**: Bracket-style competitions
- [ ] **Mobile Apps**: Native iOS/Android apps
- [ ] **Tile Counter**: Display remaining tiles by type
- [ ] **Probability Calculator**: Show winning odds
- [ ] **Training Scenarios**: Practice specific situations
- [ ] **Achievement System**: Badges and goals
- [ ] **Social Features**: Share games, leaderboards

### Integration Opportunities

- **ML Training Pipeline**: Automated model training from BigQuery data
- **Analytics Dashboard**: Separate analytics web app
- **API**: RESTful API for external tools
- **Discord Bot**: Game stats and notifications
- **Data Export**: CSV/Excel export for offline analysis

---

## Success Metrics

### Phase 2 Success Criteria
- Complete games playable from start to finish
- All standard yaku detected correctly
- Meld calls working with proper priority
- Accurate score calculation

### Phase 3 Success Criteria
- Professional-looking tile graphics
- Intuitive layout similar to traditional games
- Smooth animations and transitions
- < 2 second page load time

### Phase 4 Success Criteria
- 100% of games logged successfully
- BigQuery pipeline handles 1000+ games
- Query response time < 1 second
- No data loss or corruption

### Phase 5 Success Criteria
- 95%+ test coverage
- Zero critical bugs in production
- Successfully deployed and accessible
- User feedback collected and positive

---

## Timeline Summary

| Phase | Duration | Focus | Status |
|-------|----------|-------|--------|
| Phase 1 | ✅ Complete | Basic tile engine and UI | ✅ Done |
| Phase 2.1 | ✅ Complete | Winning detection & scoring | ✅ Done (2025-03-10) |
| Phase 2.2 | ✅ Complete | Meld calls (Pon/Chi/Kan) | ✅ Done (2025-03-10) |
| Phase 2.2.5 | ✅ Complete | Hand organization (drawn tile separation, auto-sort) | ✅ Done (2025-03-11) |
| Phase 2.3 | 1-2 weeks | Round management | 🔄 Next |
| Phase 3 | 3-4 weeks | UI/UX improvements (graphics, layout) | ⏳ Planned |
| Phase 4 | 2-3 weeks | Data collection and BigQuery | ⏳ Planned |
| Phase 5 | 4-6 weeks | Advanced features and deployment | ⏳ Planned |
| **Total** | **13-19 weeks** | From current state to production | In Progress |

---

## Getting Started with Next Phase

### Immediate Next Steps (Phase 2.3 - Round Management)

1. **End-of-Round Handling**
   - Detect exhaustive draw (流局) when wall is empty
   - Show tenpai/noten status for all players
   - Calculate noten payments (3000 points from noten to tenpai players)
   - Handle dealer rotation (連荘 vs 輪荘)

2. **Multiple Rounds**
   - Implement round progression (East 1 → East 2 → ... → East 4)
   - Track round wind and dealer position
   - Support full East round (東場 4 rounds minimum)
   - Optional South round (南場) implementation

3. **Game Completion**
   - Detect game end conditions (after oorasu)
   - Show final scores and rankings (1st/2nd/3rd/4th)
   - Option to save/export game results
   - "Start New Game" resets all state

### Recommended Reading

- [Riichi Mahjong Rules](https://riichi.wiki/)
- [Mahjong Library Documentation](https://pypi.org/project/mahjong/)
- [Reflex Performance Guide](https://reflex.dev/docs/performance/)
- [BigQuery Best Practices](https://cloud.google.com/bigquery/docs/best-practices)

---

# 開発ロードマップ（日本語版）

## プロジェクトビジョン

1人で4人分の立場をプレイできるWebベースの麻雀シミュレーターを構築し、分析と機械学習のトレーニングデータ生成のための完全なゲームログを実現します。

### 主要目標

1. **セルフプレイ体験**: 4人全員をコントロールして練習と分析を実現
2. **データ収集**: BigQuery分析用の包括的なゲームログ取得
3. **学習ツール**: 全ての手牌を同時表示して学習と改善をサポート
4. **MLパイプライン**: 麻雀AI開発用のトレーニングデータ生成

---

## 現在の状況: Phase 2.1 & 2.2 完了 ✅

### 実装済み機能

**Phase 1 - コア基盤:**
- [x] 牌エンジン: 136枚の牌生成・シャッフル・配布
- [x] ゲームロジック: ターン管理、ツモ・打牌機構、山管理
- [x] プレイヤー管理: 4人の状態（手牌、捨て牌、点数、立直状態）
- [x] Reflex UI: 4人全員を表示するインタラクティブなWebインターフェース
- [x] テンパイ判定: 13枚手牌の待ち牌検出
- [x] 立直宣言: バリデーション付き完全実装
- [x] ゲームログ: タイムスタンプ付きJSON形式でのアクション記録
- [x] 基本的な手牌評価: 簡易和了判定（4面子1雀頭）

**Phase 2.1 - 和了判定とスコアリング:**
- [x] ロン検出: 捨て牌での和了判定と点数計算
- [x] ツモ検出: 自摸和了と正確な支払い分配
- [x] 役判定統合: `mahjong`ライブラリによる完全な役検出
- [x] 点数計算: 翻・符から点数への変換（親・子対応）
- [x] 和了表示: 役名、翻、符、点数の詳細表示

**Phase 2.2 - 鳴き:**
- [x] ポン実装: 刻子コールとUIボタン、ターン進行
- [x] チー実装: 順子コール（上家からのみ）
- [x] カン検出: 槓コール検出（大明槓、暗槓、小明槓）
- [x] コール優先順位: ロン > カン > ポン > チーの処理
- [x] コールパス: 全てのコール機会をスキップ
- [x] 面子表示: 鳴いた面子の視覚的表現

**Phase 2.2.5 - 手牌整理（Phase 3から前倒し）:**
- [x] ツモ牌分離表示: 最後にツモった牌を右側に分離表示
- [x] 手牌自動ソート: 打牌後に手牌を自動ソート
- [x] 視覚的明瞭さ: 適切な間隔で手牌の可読性向上

---

## Phase 2: コアゲーム機能 ✅（2.1 & 2.2 完了）

**目標**: 麻雀ゲームの基本メカニクスを完成

### 2.1 和了判定とスコアリング ✅ 完了

**優先度**: 高

- [x] **ロン - 他家の捨て牌で和了**
  - 他プレイヤーの捨て牌で和了可能な検出 ✅
  - 該当プレイヤーに「ロン」ボタン表示 ✅
  - フリテン（振聴）ルール対応（TODO: 完全対応）
  - 優先順位処理（親 vs 子） ✅

- [x] **ツモ - 自摸和了**
  - ツモ時の和了手自動検出 ✅
  - 「ツモ」ボタン表示 ✅
  - 全プレイヤーからの支払い計算 ✅

- [x] **役判定統合**
  - `mahjong`ライブラリ統合で完全な役検出 ✅
  - 和了手の内訳表示（役名、翻、符） ✅
  - 標準的な役全て実装（38種類以上） ✅
  - 複合役の処理 ✅

- [x] **点数計算**
  - 翻・符からの完全な点数計算 ✅
  - 特殊ケース対応：親の和了、頭ハネなど ✅
  - 点数変動のアニメーション表示（基本表示） ✅
  - プレイヤー点数の正確な更新 ✅

**完了日**: 2025-03-10

### 2.2 鳴き（Naki） ✅ 完了

**優先度**: 高

- [x] **ポン - 刻子の鳴き**
  - 捨て牌でポン可能な検出 ✅
  - タイムアウト付き「ポン」ボタン表示 ✅
  - 手牌から面子エリアへ牌を移動 ✅
  - ツモスキップして即打牌 ✅

- [x] **チー - 順子の鳴き**
  - 有効なチーパターン検出（上家からのみ） ✅
  - 複数パターン可能時に選択肢表示 ✅
  - ポン・カンより低優先度 ✅
  - 明面子として表示更新 ✅

- [x] **カン - 槓**
  - **大明槓**: 捨て牌から槓 ✅
  - **暗槓**: 手牌から暗槓（検出準備完了）
  - **小明槓**: ポンへの加槓（検出準備完了）
  - 嶺上牌をツモ（TODO）
  - 新しいドラ表示牌を公開（TODO）

- [x] **優先順位システム**
  - ロン > カン > ポン > チーの優先順位 ✅
  - 複数同時コール処理 ✅
  - コール後の適切なターン進行 ✅

**完了日**: 2025-03-10

**備考**:
- UI表示問題修正（牌テキスト色の修正）
- カン後の嶺上牌ツモと追加ドラ表示は未実装
- フリテン検出の完全対応が必要

### 2.2.5 手牌整理（Phase 3からの前倒し実装） ✅ 完了

**優先度**: 高（Phase 3から前倒し）

- [x] **ツモ牌の分離表示**
  - ツモ牌を右側に分離して表示 ✅
  - 手牌とツモ牌の間に視覚的なスペース ✅
  - 手牌の可読性が大幅に向上 ✅

- [x] **手牌の自動ソート**
  - 打牌後に手牌を自動ソート ✅
  - 伝統的な麻雀の牌配置を維持 ✅
  - パターン識別が容易に ✅

**完了日**: 2025-03-11

**実装詳細**:
- Playerクラスに`last_drawn_tile`属性を追加
- `draw_tile()`でツモ牌を記録
- `discard_tile()`でツモ牌をクリアし手牌を自動ソート
- UIで手牌（13枚）とツモ牌（1枚）を分離表示
- 視覚的な明瞭さのため16pxの間隔で表示

### 2.3 局管理

**優先度**: 中

- [ ] **局終了処理**
  - 流局検出
  - テンパイ・ノーテン表示
  - ノーテン罰符計算
  - 親の連荘・輪荘判定

- [ ] **複数局対応**
  - 東場全4局サポート
  - 南場オプション
  - 場風・親位置の追跡
  - オーラス（最終局）検出

---

## Phase 3: UI/UX改善（3-4週間）

**目標**: 洗練されたゲーム体験の実現

### 3.1 牌グラフィック

**優先度**: 高

- [ ] **牌画像アセット**
  - 牌画像の入手または作成（SVG/PNG）
  - 標準サイズ: 約50x70px
  - 捨て牌用の回転版
  - ドラ表示牌のスタイリング

- [ ] **画像統合**
  - テキスト牌（"1m"）を画像に置換
  - アクセシビリティ維持（alt、title属性）
  - 画像読み込みとキャッシュの最適化
  - 縦横表示の両対応

### 3.2 レイアウト改善

**優先度**: 中

- [ ] **伝統的な麻雀レイアウト**
  - 十字配置（上下左右）
  - 中央に捨て牌エリア（実際の卓のように）
  - 適切な山の可視化
  - ドラ表示エリア

- [ ] **プレイヤー配置ビュー**
  - 下: 現在のプレイヤー（主フォーカス）
  - 右: 次のプレイヤー（上家）
  - 上: 対面
  - 左: 前のプレイヤー（下家）

---

## Phase 4: データ収集とBigQuery（2-3週間）

**目標**: 分析用のログパイプライン完成

### 4.1 拡張ログ

**優先度**: 高

- [ ] **包括的なゲーム状態ログ**
  - 各決定ポイントでの完全な手牌状態
  - 各ターンの全プレイヤー点数
  - 残り山の枚数
  - 公開されたドラ表示牌
  - 場風・局情報

- [ ] **アクションメタデータ**
  - 手出し vs ツモ切りの区別
  - 決定タイミング記録
  - 可視情報 vs 隠し状態
  - 和了手詳細（役、翻、符）

### 4.2 BigQuery統合

**優先度**: 中

- [ ] **BigQueryセットアップ**
  - GCPプロジェクトとデータセット作成
  - テーブルスキーマ定義
  - 認証設定（サービスアカウント）
  - コネクションプーリング実装

- [ ] **データパイプライン**
  - ゲーム終了時のバッチアップロード
  - UI非ブロッキングな非同期アップロード
  - 失敗時のリトライロジック
  - オフラインモード用のローカルキャッシュ

---

## Phase 5: 高度な機能とデプロイ（4-6週間）

**目標**: プロダクション対応アプリケーション

### 5.1 分析と統計

**優先度**: 中

- [ ] **アプリ内統計**
  - 位置別勝率
  - 和了時の平均翻数
  - 最頻出役
  - 立直成功/失敗率

- [ ] **棋譜再生**
  - 完全なゲーム状態保存
  - ターン毎のステップ実行
  - 代替手の分析（"What if"）
  - リプレイデータのエクスポート

### 5.2 テストと品質保証

**優先度**: 高（デプロイ前）

- [ ] **ユニットテスト**
  - 牌エンジンロジック
  - 手牌評価
  - 点数計算
  - プレイヤー状態管理

### 5.3 デプロイ

**優先度**: 中

- [ ] **本番ビルド**
  - 環境設定
  - シークレット管理
  - エラーログ（Sentryなど）

- [ ] **ホスティングオプション**
  - オプションA: Reflex Cloud（最も簡単）
  - オプションB: Docker + GCP Cloud Run
  - オプションC: Docker + AWS ECS

---

## タイムライン要約

| フェーズ | 期間 | 焦点 | ステータス |
|---------|------|------|-----------|
| Phase 1 | ✅ 完了 | 基本的な牌エンジンとUI | ✅ 完了 |
| Phase 2.1 | ✅ 完了 | 和了判定とスコアリング | ✅ 完了 (2025-03-10) |
| Phase 2.2 | ✅ 完了 | 鳴き（ポン・チー・カン） | ✅ 完了 (2025-03-10) |
| Phase 2.2.5 | ✅ 完了 | 手牌整理（ツモ牌分離、自動ソート） | ✅ 完了 (2025-03-11) |
| Phase 2.3 | 1-2週 | 局管理 | 🔄 次のステップ |
| Phase 3 | 3-4週 | UI/UX改善（グラフィック、レイアウト） | ⏳ 予定 |
| Phase 4 | 2-3週 | データ収集とBigQuery | ⏳ 予定 |
| Phase 5 | 4-6週 | 高度な機能とデプロイ | ⏳ 予定 |
| **合計** | **13-19週** | 現状からプロダクションまで | 進行中 |

---

## 次のフェーズの開始方法

### 直近の次のステップ（Phase 2.3 - 局管理）

1. **局終了処理**
   - 山が空の場合の流局検出
   - 全プレイヤーのテンパイ・ノーテン状態表示
   - ノーテン罰符計算（ノーテンからテンパイへ3000点）
   - 親の連荘・輪荘判定

2. **複数局対応**
   - 局進行の実装（東1局 → 東2局 → ... → 東4局）
   - 場風と親位置の追跡
   - 東場全4局サポート（最低）
   - 南場オプション実装

3. **ゲーム終了**
   - ゲーム終了条件の検出（オーラス後）
   - 最終点数と順位表示（1位/2位/3位/4位）
   - ゲーム結果の保存・エクスポートオプション
   - 「新規ゲーム開始」で全状態リセット
