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

### 2.3 Round Management ✅ COMPLETE (Core Features)

**Priority**: MEDIUM

- [x] **End-of-Round Handling**
  - Detect exhaustive draw (流局) when wall empties ✅
  - Check tenpai/noten status internally ✅
  - Calculate and distribute noten payments (3000 point total) ✅
  - Handle dealer rotation (連荘 vs 輪荘) ✅

- [x] **Multiple Rounds**
  - Support full East round (東場 4 rounds) ✅
  - Support South round (南場 4 rounds) for hanchan ✅
  - Track round wind and dealer position ✅
  - Game type selection: 半荘 (hanchan) and 東風戦 (tonpuu) ✅

- [x] **Game Completion**
  - Detect game end conditions (after 東4局 for tonpuu, 南4局 for hanchan) ✅
  - Round progression with proper game termination ✅
  - UI display of current round and game type (e.g., "半荘 - 東1局 2本場") ✅

- [ ] **UI Enhancements** (Deferred to Phase 3)
  - Show tenpai/noten status to players after exhaustive draw
  - Display final scores and rankings when game ends
  - Option to save/export game results

**Completed**: 2026-03-11

**Implementation Details**:
- **Core Files Modified**: `app/engine/game.py`, `app/state.py`, `app/components/board.py`, `app/app.py`
- **Round Tracking**: Added `round_wind`, `round_number`, `honba_sticks`, `riichi_sticks`, `game_type` to game state
- **Key Methods Implemented**:
  - `handle_exhaustive_draw()`: Checks tenpai (using `HandEvaluator.check_tenpai()`), distributes 3000 points from noten to tenpai players, manages dealer rotation
  - `handle_round_end_after_win()`: Manages dealer rotation based on winner (連荘 if dealer wins, 輪荘 if non-dealer wins)
  - `advance_round()`: Progresses rounds (東1→東2→...→南1→...→南4), detects game end
- **Game Flow**:
  - `advance_turn()` checks for exhaustive draw when `wall` is empty
  - `declare_tsumo()` and `declare_ron()` call `handle_round_end_after_win()` after scoring
  - Automatic round progression and game restart until game end condition met
- **Dealer Rotation Rules**:
  - 連荘 (Renchan): Dealer continues when dealer wins OR dealer is tenpai at exhaustive draw (honba_sticks += 1)
  - 輪荘 (Rinshou): Dealer rotates when non-dealer wins OR dealer is noten at exhaustive draw (honba_sticks = 0)
- **UI Updates**:
  - Two game start buttons: "New Game (半荘)" and "New Game (東風戦)"
  - Round display shows game type and current round: "{game_type_label} - {round_name}"
  - `round_name` computed var formats as "東1局 2本場" style

**Known Limitations**:
- **UI Display**: Tenpai/noten status is calculated internally but not shown to players after exhaustive draw
- **Game End**: Game terminates correctly but no final score/ranking screen implemented
- **Save/Export**: No functionality to save or export game results
- **Oorasu Detection**: Last round is not explicitly marked or announced
- **West/North Rounds**: System supports only East/South (半荘/東風戦); West/North rounds not implemented

**Bug Fixes Applied** (during Phase 2.3):
- Fixed drawn tile discard issue: Added `is_drawn_tile` parameter to properly identify and discard drawn tiles
- Fixed winning detection with melds: Modified `check_tsumo()` and `check_ron()` to handle meld-adjusted hand sizes
- Fixed drawn tile display: Changed from `hand.remove()` to `hand[:-1]` to correctly separate drawn tile

---

## Phase 3: UI/UX Improvements ✅ COMPLETE

**Goal**: Create a polished, game-like experience

**Status**: All core features completed (2026-03-13)

### 3.1 Tile Graphics ✅ COMPLETE

**Priority**: HIGH

- [x] **Tile Image Assets**
  - Source tile images from FluffyStuff/riichi-mahjong-tiles (SVG) ✅
  - All 34 tile types (9 manzu, 9 pinzu, 9 souzu, 7 jihai) ✅
  - High-quality SVG format for scalability ✅
  - Placed in `assets/tiles/` directory ✅

- [x] **Image Integration**
  - Replace text tiles ("1m") with SVG images ✅
  - Tile code to filename mapping system ✅
  - Accessibility support (alt attributes) ✅
  - Support for normal (40x56px) and small (32x42px) sizes ✅

- [x] **Visual Polish**
  - Smooth hover animations with scale and lift effects ✅
  - Gradient backgrounds on clickable tiles ✅
  - Shadow effects (2px static, 8px on hover) ✅
  - Cubic-bezier easing for smooth transitions (0.3s) ✅
  - Enhanced melds display with gradient backgrounds ✅

**Completed**: 2026-03-13

**Implementation Details**:
- **Core Files**: `app/components/tile_image.py` (new), `app/components/hand.py` (updated), `app/components/mahjong_table.py` (updated)
- **Tile Mapping**: Created `TILE_IMAGE_MAP` dictionary (tile code → filename)
  - Examples: "1m" → "Man1.svg", "5p" → "Pin5.svg", "1z" → "Ton.svg"
- **Image Components**:
  - `render_tile_image()`: Base component with size/clickability options
  - `render_tile_static_image()`: Non-interactive display
  - `render_tile_clickable_image()`: Interactive with click handler
- **Visual Effects**:
  - Clickable: Gradient background, 6px lift on hover, 1.08x scale, shadow
  - Static: Subtle shadow for depth
  - Transition: cubic-bezier(0.4, 0, 0.2, 1)
- **Asset Management**:
  - Tiles in `assets/tiles/` → symlinked to `.web/public/tiles/`
  - 43 SVG files (34 tiles + variants)
- **Center Discard Area**: All players' discards use small tile images ✅

**Notes**:
- Melds display remains text-based (Reflex variable system limitation)
- Enhanced with gradient backgrounds
- Images: FluffyStuff/riichi-mahjong-tiles (CC0 License)

### 3.2 Layout Improvements ✅ COMPLETE

**Priority**: MEDIUM

- [x] **Traditional Mahjong Layout**
  - Position players in cross pattern (上下左右) ✅
  - Center area for discards (like real table) ✅
  - Dora display area ✅

- [x] **Player Position Views**
  - Bottom: Player 0 (East) - larger display ✅
  - Right: Player 1 (South) ✅
  - Top: Player 2 (West) ✅
  - Left: Player 3 (North) ✅

- [x] **Tile Size Adjustment**
  - Bottom player: normal size tiles ✅
  - Other players: small size tiles ✅
  - Dynamic sizing based on position ✅

- [ ] **Responsive Design** (Deferred)
  - Desktop: full 4-player view (✅ implemented)
  - Tablet: compact layout
  - Mobile: focus on current player
  - Proper scaling for different screen sizes

**Completed**: 2026-03-12

**Implementation Details**:
- **Core Files**: `app/components/mahjong_table.py` (new), `app/components/hand.py` (modified), `app/app.py` (modified)
- **Layout Structure**:
  - Cross-pattern with absolute positioning for top/bottom players
  - hstack for middle row (left, center, right)
  - Center discard area shows all 4 players' discards in a 2x2 grid
- **Tile Sizing**:
  - Added `tile_size` parameter to `render_hand()`, `render_tile_clickable()`, `render_tile_static()`
  - Normal size: 18px font, 8px 12px padding
  - Small size: 12px font, 4px 8px padding
- **Center Discard Area**:
  - Compact display showing recent discards for each player
  - Player name labels for clarity
  - 2x2 grid matching player positions
- **Key Components**:
  - `render_mahjong_table()`: Main table layout
  - `render_center_discard_area()`: Center discard display
  - `_render_discard_section()`: Individual player discard section

**Notes**:
- Responsive design (tablet/mobile) deferred to future phase
- Layout works well on desktop (1200px+)

### 3.3 Enhanced Interactions ✅ COMPLETE (Core Features)

**Priority**: MEDIUM

- [x] **End-of-Game Displays**
  - Exhaustive draw (流局) display with tenpai/noten status ✅
  - Final game end screen with rankings ✅
  - Oorasu (final round) indicator ✅

- [x] **Game Information Display**
  - Dora indicators ✅
  - Remaining tiles in wall ✅
  - Current round and dealer indicator ✅
  - Game type display (半荘/東風戦) ✅

- [x] **Hand Organization**
  - Auto-sort hand option ✅ **Completed in Phase 2.2.5**
  - Drawn tile separation ✅ **Completed in Phase 2.2.5**

- [ ] **Advanced Features** (Deferred)
  - Context-aware button visibility (partial)
  - Keyboard shortcuts (R: Riichi, T: Tsumo, etc.)
  - Manual tile arrangement (drag-and-drop)
  - Visual tenpai hints
  - Tile grouping suggestions
  - Turn timer

**Completed**: 2026-03-12

**Estimated Time for Remaining**: ~2-3 days

---

## Phase 3.1 Alternative: Flask/React Migration ⚠️ IN PROGRESS

**Status**: Migration in progress (2026-03-13)

**Rationale**: Due to persistent SVG image loading issues in Reflex 0.8, we are migrating to a Flask (backend) + React (frontend) architecture. This provides:
- ✅ Mature static asset management
- ✅ Industry-standard stack with extensive documentation
- ✅ Better frontend control and flexibility
- ✅ Preservation of all game engine code (100% reusable)

### Migration Overview

**What's Preserved**:
- ✅ All game engine code (`app/engine/` directory - pure Python)
- ✅ Game logic and rules (tile management, scoring, melds, round management)
- ✅ 43 SVG tile images from FluffyStuff/riichi-mahjong-tiles
- ✅ All Phase 1-2.3 features and mechanics

**What's Being Rewritten**:
- ❌ UI Layer (`app/components/` → React components)
- ❌ State Management (`app/state.py` → React state + API)
- ❌ Application Entry (`app/app.py` → Flask routes + React app)

### Migration Phases (3-5 days)

#### Phase M1: Backend Setup (Day 1 - Morning)
**Estimated Time**: 3-4 hours

- [ ] **Flask Application**
  - Initialize Flask app with factory pattern
  - Set up Flask-SocketIO for real-time updates
  - Configure CORS for development

- [ ] **Copy Game Engine**
  - Copy `app/engine/` to `backend/app/engine/`
  - Verify imports and functionality
  - No code changes needed

- [ ] **REST API**
  - Endpoints for game actions (new game, discard, riichi, ron, tsumo)
  - Endpoints for meld calls (pon, chi, kan, pass)
  - Tenpai checking endpoint

- [ ] **WebSocket Events**
  - Real-time game state updates
  - Call availability notifications
  - Round/game end events

- [ ] **Static Files**
  - Copy tile images to `backend/static/tiles/`
  - Test image serving

#### Phase M2: Frontend Setup (Day 1 - Afternoon)
**Estimated Time**: 3-4 hours

- [ ] **React + Vite Project**
  - Initialize React TypeScript project
  - Install dependencies (SocketIO, Zustand, TailwindCSS)
  - Configure development environment

- [ ] **Type Definitions**
  - Define TypeScript interfaces for game state
  - Player, GameState, WinInfo types
  - API request/response types

- [ ] **API Client & WebSocket**
  - Create API client functions
  - Set up SocketIO connection hook
  - Implement state synchronization

#### Phase M3: Core UI Components (Day 2)
**Estimated Time**: 6-8 hours

- [ ] **Tile Component** (1 hour)
  - SVG image display with fallback
  - Click handlers and hover effects
  - Size variants (normal, small)

- [ ] **Hand Component** (2 hours)
  - Display 13 tiles + drawn tile separately
  - Interactive vs static modes
  - Call buttons (Ron, Tsumo, Pon, Chi, Kan)

- [ ] **Board Component** (1 hour)
  - Current player indicator
  - Wall remaining counter
  - Dora indicators display
  - Round information

- [ ] **MahjongTable Component** (2-3 hours)
  - Cross-pattern layout (上下左右)
  - Four player positions
  - Player-adjacent discards
  - Responsive design

- [ ] **Controls Component** (1 hour)
  - New Game buttons (半荘/東風戦)
  - Check Tenpai button
  - Riichi declaration
  - Pass on calls
  - Export logs

#### Phase M4: Game Flow Integration (Day 3 - Morning)
**Estimated Time**: 3-4 hours

- [ ] **State Management**
  - Connect components to WebSocket state
  - Implement optimistic updates
  - Handle state synchronization

- [ ] **Game Actions**
  - Wire up discard actions
  - Connect call buttons
  - Implement riichi flow
  - Pass on calls

- [ ] **Real-time Updates**
  - Listen to SocketIO events
  - Update UI on state changes
  - Handle connection errors

#### Phase M5: End Screens & Polish (Day 3 - Afternoon)
**Estimated Time**: 3-4 hours

- [ ] **Exhaustive Draw Overlay**
  - Tenpai/noten status display
  - 3000 point payment breakdown
  - Continue button

- [ ] **Game End Screen**
  - Final rankings with medals (🥇🥈🥉)
  - Score differences
  - New game buttons

- [ ] **Visual Polish**
  - Smooth animations (CSS transitions)
  - Hover effects
  - Loading states
  - Responsive design

- [ ] **Testing**
  - Play through complete games
  - Test all edge cases
  - Verify all features working

**Total Estimated Time**: 18-24 hours (3-4 working days)

**Documentation**: See [MIGRATION.md](MIGRATION.md) for detailed migration guide including:
- Architecture design (Flask + React)
- API design (REST + WebSocket)
- Project structure
- Code migration mapping
- Testing strategy
- Rollback plan

**Status**: Phase M1 ready to begin

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
| Phase 2.3 | ✅ Complete | Round management (exhaustive draw, game types) | ✅ Done (2026-03-12) |
| Phase 3.1 (Reflex) | ⚠️ Partial | Tile graphics (image loading issues) | ⚠️ Blocked (2026-03-13) |
| Phase 3.2 | ✅ Complete | Layout improvements (cross-pattern, center discard) | ✅ Done (2026-03-12) |
| Phase 3.3 | ✅ Complete | Enhanced interactions (end screens, oorasu indicator) | ✅ Done (2026-03-12) |
| **Phase M1** | **3-4 hours** | **Flask backend setup** | **⏳ In Progress** |
| **Phase M2** | **3-4 hours** | **React frontend setup** | **⏳ Next** |
| **Phase M3** | **6-8 hours** | **Core UI components** | **⏳ Planned** |
| **Phase M4** | **3-4 hours** | **Game flow integration** | **⏳ Planned** |
| **Phase M5** | **3-4 hours** | **End screens & polish** | **⏳ Planned** |
| **Migration** | **3-4 days** | **Reflex → Flask/React** | **⚠️ In Progress (2026-03-13)** |
| Phase 4 | 2-3 weeks | Data collection and BigQuery | ⏳ After Migration |
| Phase 5 | 4-6 weeks | Advanced features and deployment | ⏳ Planned |
| **Total** | **13-19 weeks** | From current state to production | In Progress |

---

## Getting Started with Next Phase

### Immediate Next Steps (Migration to Flask/React)

**Current Status**: Phase 1-2.3 and Phase 3.2-3.3 complete in Reflex. Migrating to Flask/React due to image loading issues.

**Next Actions**:

1. **Phase M1: Backend Setup** (Start Here!)
   - Create Flask application structure with factory pattern
   - Copy game engine code (`app/engine/` → `backend/app/engine/`)
   - Implement REST API endpoints for all game actions
   - Set up Flask-SocketIO for real-time updates
   - Copy and serve tile images from `backend/static/tiles/`

2. **Phase M2: Frontend Setup**
   - Initialize React + TypeScript + Vite project
   - Install dependencies (SocketIO, Zustand, TailwindCSS)
   - Create TypeScript type definitions for game state
   - Set up API client and WebSocket hooks

3. **Phase M3-M5: UI Implementation**
   - Build React components (Tile, Hand, Board, MahjongTable)
   - Wire up game flow and actions
   - Implement end screens (exhaustive draw, game end)
   - Apply visual polish and test thoroughly

**Estimated Timeline**: 3-4 working days (18-24 hours)

**Documentation**: See [MIGRATION.md](MIGRATION.md) for detailed step-by-step guide

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

### 2.3 局管理 ✅ 完了（コア機能）

**優先度**: 中

- [x] **局終了処理**
  - 流局検出（山が空の時） ✅
  - テンパイ・ノーテン状態の内部チェック ✅
  - ノーテン罰符計算（3000点分配） ✅
  - 親の連荘・輪荘判定 ✅

- [x] **複数局対応**
  - 東場全4局サポート ✅
  - 南場対応（半荘） ✅
  - 場風・親位置の追跡 ✅
  - ゲームタイプ選択：半荘と東風戦 ✅

- [x] **ゲーム終了**
  - ゲーム終了条件の検出 ✅
  - 局進行と適切なゲーム終了 ✅
  - 現在の局とゲームタイプのUI表示 ✅

- [ ] **UI改善**（Phase 3に延期）
  - プレイヤーへのテンパイ・ノーテン表示
  - 終局時の最終点数・順位表示
  - ゲーム結果の保存・エクスポート

**完了日**: 2026-03-12

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

### 3.2 レイアウト改善 ✅ 完了

**優先度**: 中

- [x] **伝統的な麻雀レイアウト**
  - 十字配置（上下左右） ✅
  - 中央に捨て牌エリア（実際の卓のように） ✅
  - ドラ表示エリア ✅

- [x] **プレイヤー配置ビュー**
  - 下: プレイヤー0（東） - 大きく表示 ✅
  - 右: プレイヤー1（南） ✅
  - 上: プレイヤー2（西） ✅
  - 左: プレイヤー3（北） ✅

- [x] **牌サイズ調整**
  - 下のプレイヤー: 通常サイズの牌 ✅
  - 他のプレイヤー: 小さいサイズの牌 ✅
  - 位置に基づく動的サイズ調整 ✅

- [ ] **レスポンシブデザイン**（延期）
  - デスクトップ: 4人全員表示（✅ 実装済み）
  - タブレット: コンパクトレイアウト
  - モバイル: 現在のプレイヤーにフォーカス
  - 画面サイズに応じた適切なスケーリング

**完了日**: 2026-03-12

### 3.3 拡張インタラクション ✅ 完了（コア機能）

**優先度**: 中

- [x] **ゲーム終了表示**
  - 流局時のテンパイ・ノーテン表示 ✅
  - 最終順位画面 ✅
  - オーラス（最終局）インジケーター ✅

- [x] **ゲーム情報表示**
  - ドラ表示牌 ✅
  - 残り山の枚数 ✅
  - 現在の局と親表示 ✅
  - ゲームタイプ表示（半荘/東風戦） ✅

- [x] **手牌整理**
  - 手牌の自動ソート ✅ **Phase 2.2.5で完了**
  - ツモ牌の分離表示 ✅ **Phase 2.2.5で完了**

- [ ] **高度な機能**（延期）
  - コンテキスト依存のボタン表示（部分的）
  - キーボードショートカット（R: 立直、T: ツモなど）
  - 手動の牌配置（ドラッグ&ドロップ）
  - テンパイのビジュアルヒント
  - 牌グループ提案
  - ターンタイマー

**完了日**: 2026-03-12

**残り作業の推定時間**: 約2-3日

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
| Phase 2.3 | ✅ 完了 | 局管理（流局、ゲームタイプ） | ✅ 完了 (2026-03-12) |
| Phase 3.1 (Reflex) | ⚠️ 部分 | 牌グラフィック（画像読込問題） | ⚠️ ブロック (2026-03-13) |
| Phase 3.2 | ✅ 完了 | レイアウト改善（十字配置、中央捨て牌） | ✅ 完了 (2026-03-12) |
| Phase 3.3 | ✅ 完了 | 拡張インタラクション（終了画面、オーラス） | ✅ 完了 (2026-03-12) |
| **Phase M1** | **3-4時間** | **Flask バックエンド構築** | **⏳ 進行中** |
| **Phase M2** | **3-4時間** | **React フロントエンド構築** | **⏳ 次** |
| **Phase M3** | **6-8時間** | **コアUIコンポーネント** | **⏳ 予定** |
| **Phase M4** | **3-4時間** | **ゲームフロー統合** | **⏳ 予定** |
| **Phase M5** | **3-4時間** | **終了画面と仕上げ** | **⏳ 予定** |
| **マイグレーション** | **3-4日** | **Reflex → Flask/React** | **⚠️ 進行中 (2026-03-13)** |
| Phase 4 | 2-3週 | データ収集とBigQuery | ⏳ マイグレーション後 |
| Phase 5 | 4-6週 | 高度な機能とデプロイ | ⏳ 予定 |
| **合計** | **13-19週** | 現状からプロダクションまで | 進行中 |

---

## 次のフェーズの開始方法

### 直近の次のステップ（Flask/React マイグレーション）

**現在の状況**: Phase 1-2.3 および Phase 3.2-3.3 が Reflex で完成。画像読込問題により Flask/React へ移行中。

**次のアクション**:

1. **Phase M1: バックエンド構築** (ここから開始！)
   - Flask アプリケーション構造作成（ファクトリーパターン）
   - ゲームエンジンコードをコピー (`app/engine/` → `backend/app/engine/`)
   - 全ゲームアクション用の REST API エンドポイント実装
   - Flask-SocketIO でリアルタイム更新設定
   - `backend/static/tiles/` から牌画像コピーと配信

2. **Phase M2: フロントエンド構築**
   - React + TypeScript + Vite プロジェクト初期化
   - 依存関係インストール (SocketIO, Zustand, TailwindCSS)
   - ゲーム状態用の TypeScript 型定義作成
   - API クライアントと WebSocket フック設定

3. **Phase M3-M5: UI 実装**
   - React コンポーネント構築 (Tile, Hand, Board, MahjongTable)
   - ゲームフローとアクション接続
   - 終了画面実装（流局、ゲーム終了）
   - ビジュアル仕上げと徹底的なテスト

**推定スケジュール**: 3-4営業日（18-24時間）

**ドキュメント**: 詳細な手順は [MIGRATION.md](MIGRATION.md) を参照
