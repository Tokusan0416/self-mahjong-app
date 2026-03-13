# Migration Guide: Reflex → Flask/React

## Overview

This document outlines the migration from Reflex to a Flask (backend) + React (frontend) architecture to resolve persistent image loading issues and provide better control over the frontend experience.

## Migration Rationale

### Why Migrate?

1. **Image Loading Issues**: SVG tile images consistently fail to load in Reflex despite multiple troubleshooting attempts
2. **Framework Maturity**: Reflex 0.8 is still evolving; static asset management has limitations
3. **Frontend Flexibility**: React provides more mature ecosystem for complex UI interactions
4. **Industry Standard Stack**: Flask/React is battle-tested and has extensive documentation
5. **Long-term Maintainability**: Easier to find developers familiar with Flask/React vs Reflex

### What We're Preserving

- ✅ **All game engine code** (`app/engine/` directory - 100% reusable)
- ✅ **Game logic and rules** (tile management, scoring, meld detection, round management)
- ✅ **43 SVG tile images** (FluffyStuff/riichi-mahjong-tiles assets)
- ✅ **Game flow and mechanics** (all Phase 1-2.3 features)
- ✅ **Japanese Riichi Mahjong rules** (complete implementation)

### What Needs Rewriting

- ❌ **UI Layer** (`app/components/` - Reflex-specific components → React components)
- ❌ **State Management** (`app/state.py` - Reflex state → React state + API calls)
- ❌ **Application Entry** (`app/app.py` - Reflex app → Flask routes + React app)
- ❌ **Configuration** (`rxconfig.py` → Flask config + React config)

---

## New Architecture

### Tech Stack

**Backend (Flask + SocketIO)**
- Flask 3.0+ for REST API and static file serving
- Flask-SocketIO for real-time game state updates
- SQLAlchemy for future database integration (optional)
- Flask-CORS for cross-origin requests during development

**Frontend (React + TypeScript)**
- React 18+ with functional components and hooks
- TypeScript for type safety
- Vite for fast development and optimized builds
- TailwindCSS for styling (consistent with Reflex theme)
- Socket.IO client for real-time updates
- Zustand or React Context for state management

**Alternative Frontend (Vue)**
- Vue 3+ with Composition API (if preferred over React)
- TypeScript support
- Vite + Pinia for state management

### Project Structure

```
mahjong-flask-react/
├── backend/                      # Flask application
│   ├── app/
│   │   ├── __init__.py          # Flask app factory
│   │   ├── routes.py            # REST API endpoints
│   │   ├── socketio_events.py  # WebSocket event handlers
│   │   ├── engine/              # ← COPIED FROM EXISTING PROJECT
│   │   │   ├── tiles.py         # Game logic (reusable)
│   │   │   ├── player.py        # Player management (reusable)
│   │   │   ├── game.py          # Core game loop (reusable)
│   │   │   ├── scoring.py       # Scoring and yaku (reusable)
│   │   │   └── hand_evaluator.py # Hand evaluation (reusable)
│   │   └── config.py            # Configuration
│   ├── static/                  # Static files (tiles, etc.)
│   │   └── tiles/               # ← COPIED FROM assets/tiles/
│   ├── requirements.txt         # Python dependencies
│   └── run.py                   # Development server entry point
│
├── frontend/                    # React application
│   ├── src/
│   │   ├── components/          # React components
│   │   │   ├── MahjongTable.tsx # Main table layout
│   │   │   ├── Hand.tsx         # Player hand display
│   │   │   ├── Tile.tsx         # Tile image component
│   │   │   ├── Board.tsx        # Game board info
│   │   │   ├── Controls.tsx     # Game controls
│   │   │   └── EndScreens/      # Game end overlays
│   │   ├── hooks/               # Custom React hooks
│   │   │   ├── useGameState.ts  # Game state management
│   │   │   └── useSocket.ts     # SocketIO connection
│   │   ├── types/               # TypeScript type definitions
│   │   │   └── game.ts          # Game state types
│   │   ├── api/                 # API client functions
│   │   │   └── gameApi.ts       # Backend API calls
│   │   ├── App.tsx              # Main app component
│   │   └── main.tsx             # React entry point
│   ├── public/                  # Public static files
│   │   └── tiles/               # ← SYMLINK to backend/static/tiles/
│   ├── package.json             # Node dependencies
│   ├── tsconfig.json            # TypeScript config
│   ├── vite.config.ts           # Vite config
│   └── tailwind.config.js       # TailwindCSS config
│
└── README.md                    # Updated documentation
```

---

## Migration Phases

### Phase M1: Backend Setup (Day 1 - Morning)

**Estimated Time**: 3-4 hours

1. **Create Flask Application Structure**
   - Initialize Flask app with factory pattern
   - Set up Flask-SocketIO for real-time communication
   - Configure CORS for development

2. **Copy Game Engine**
   - Copy entire `app/engine/` directory to `backend/app/engine/`
   - Verify all imports work correctly
   - No code changes needed (pure Python)

3. **Create REST API Endpoints**
   ```python
   POST   /api/game/new            # Start new game
   GET    /api/game/state          # Get current game state
   POST   /api/game/discard        # Discard a tile
   POST   /api/game/riichi         # Declare riichi
   POST   /api/game/ron            # Declare ron
   POST   /api/game/tsumo          # Declare tsumo
   POST   /api/game/pon            # Call pon
   POST   /api/game/chi            # Call chi
   POST   /api/game/kan            # Call kan
   POST   /api/game/pass           # Pass on calls
   GET    /api/game/tenpai/:player # Check tenpai status
   ```

4. **Set Up WebSocket Events**
   ```python
   # Emit events for real-time updates
   emit('game_state_update', game_state)
   emit('call_available', call_info)
   emit('round_end', round_result)
   emit('game_end', final_scores)
   ```

5. **Static File Serving**
   - Copy `assets/tiles/*.svg` to `backend/static/tiles/`
   - Configure Flask to serve static files
   - Test tile image loading with simple HTML page

**Deliverables**:
- ✅ Flask app running on http://localhost:5000
- ✅ All game engine code functional
- ✅ REST API responding to requests
- ✅ WebSocket connection established
- ✅ Tile images accessible at /static/tiles/Man1.svg

---

### Phase M2: Frontend Setup (Day 1 - Afternoon)

**Estimated Time**: 3-4 hours

1. **Initialize React + Vite Project**
   ```bash
   npm create vite@latest frontend -- --template react-ts
   cd frontend
   npm install
   ```

2. **Install Dependencies**
   ```bash
   npm install socket.io-client zustand axios
   npm install -D tailwindcss postcss autoprefixer
   npm install @radix-ui/react-dialog @radix-ui/react-button  # For UI components
   ```

3. **Configure TailwindCSS**
   - Set up Tailwind with similar theme to Reflex (blue accent)
   - Create base styles and color palette

4. **Create Type Definitions**
   ```typescript
   // types/game.ts
   interface Player {
     hand: string[];
     discards: string[];
     melds: string[];
     score: number;
     is_riichi: boolean;
     last_drawn_tile: string;
   }

   interface GameState {
     players: Player[];
     current_player: number;
     wall_remaining: number;
     dora_indicators: string[];
     round_wind: string;
     round_number: number;
     is_game_over: boolean;
     // ... etc
   }
   ```

5. **Set Up API Client and WebSocket Hook**
   ```typescript
   // hooks/useSocket.ts
   export const useSocket = () => {
     const [socket, setSocket] = useState<Socket | null>(null);
     const [gameState, setGameState] = useState<GameState | null>(null);

     useEffect(() => {
       const newSocket = io('http://localhost:5000');
       newSocket.on('game_state_update', setGameState);
       setSocket(newSocket);
       return () => { newSocket.close(); };
     }, []);

     return { socket, gameState };
   };
   ```

**Deliverables**:
- ✅ React app running on http://localhost:5173
- ✅ TypeScript type definitions complete
- ✅ SocketIO connection to backend working
- ✅ API client functions implemented
- ✅ TailwindCSS configured

---

### Phase M3: Core UI Components (Day 2)

**Estimated Time**: 6-8 hours

1. **Tile Component** (1 hour)
   - SVG image with fallback
   - Click handler
   - Hover effects
   - Size variants (normal, small)
   - Based on existing `app/components/tile_image.py` logic

2. **Hand Component** (2 hours)
   - Display 13 tiles + drawn tile
   - Interactive vs static mode
   - Call buttons (Ron, Tsumo, Pon, Chi, Kan)
   - Based on existing `app/components/hand.py`

3. **Board Component** (1 hour)
   - Current player indicator
   - Wall remaining
   - Dora indicators
   - Round information
   - Based on existing `app/components/board.py`

4. **MahjongTable Component** (2-3 hours)
   - Cross-pattern layout (上下左右)
   - Four player positions
   - Center discard area or player-adjacent discards
   - Responsive to different screen sizes
   - Based on existing `app/components/mahjong_table.py`

5. **Controls Component** (1 hour)
   - New Game button (半荘/東風戦)
   - Check Tenpai button
   - Riichi declaration
   - Pass on calls button
   - Export logs
   - Based on existing `app/components/board.py`

**Deliverables**:
- ✅ All core components implemented
- ✅ Tile images displaying correctly
- ✅ Layout matching Reflex version
- ✅ Interactive elements functional

---

### Phase M4: Game Flow Integration (Day 3 - Morning)

**Estimated Time**: 3-4 hours

1. **State Management**
   - Connect components to WebSocket game state
   - Implement optimistic updates for better UX
   - Handle state synchronization

2. **Game Actions**
   - Wire up all discard actions
   - Connect call buttons (Ron, Tsumo, Pon, Chi, Kan)
   - Implement riichi declaration flow
   - Pass on calls functionality

3. **Real-time Updates**
   - Listen to SocketIO events
   - Update UI immediately on state changes
   - Handle connection errors gracefully

4. **Error Handling**
   - Display error messages
   - Handle network failures
   - Retry logic for failed actions

**Deliverables**:
- ✅ Full game playable from start to finish
- ✅ All actions working (discard, calls, riichi)
- ✅ Real-time updates functioning
- ✅ Error handling implemented

---

### Phase M5: End Screens & Polish (Day 3 - Afternoon)

**Estimated Time**: 3-4 hours

1. **Exhaustive Draw Overlay**
   - Display tenpai/noten status
   - Show 3000 point payment breakdown
   - Continue button
   - Based on existing `app/components/exhaustive_draw_display.py`

2. **Game End Screen**
   - Final rankings with medals (🥇🥈🥉)
   - Score differences
   - New game buttons
   - Based on existing `app/components/game_end_screen.py`

3. **Visual Polish**
   - Smooth animations (CSS transitions)
   - Hover effects
   - Loading states
   - Responsive design adjustments

4. **Testing**
   - Play through complete games (半荘 and 東風戦)
   - Test all edge cases (multiple rons, exhaustive draw, etc.)
   - Verify all features from Phase 1-3 working

**Deliverables**:
- ✅ All end screens implemented
- ✅ Visual polish applied
- ✅ Full functionality verified
- ✅ Migration complete

---

### Phase M6: Deployment Preparation (Day 4-5 - Optional)

**Estimated Time**: Variable (1-2 days if needed)

1. **Production Build**
   - Flask production configuration (Gunicorn)
   - React build optimization (Vite)
   - Environment variable management

2. **Docker Configuration**
   - Dockerfile for backend
   - Dockerfile for frontend
   - docker-compose.yml for local development

3. **Deployment**
   - Choose hosting platform (Cloud Run, Heroku, Railway, etc.)
   - CI/CD pipeline setup
   - Monitoring and logging

**Note**: This phase is optional for now. Focus on getting the application working locally first.

---

## API Design

### REST Endpoints

```typescript
// Game Management
POST /api/game/new { game_type: "hanchan" | "tonpuu" }
  → { game_id: string, game_state: GameState }

GET /api/game/state
  → { game_state: GameState }

// Game Actions
POST /api/game/discard { player_idx: number, tile: string, is_drawn: boolean }
  → { success: boolean, game_state: GameState }

POST /api/game/riichi { player_idx: number }
  → { success: boolean, game_state: GameState }

POST /api/game/ron { player_idx: number }
  → { success: boolean, win_info: WinInfo, game_state: GameState }

POST /api/game/tsumo { player_idx: number }
  → { success: boolean, win_info: WinInfo, game_state: GameState }

POST /api/game/pon { player_idx: number, tile: string }
  → { success: boolean, game_state: GameState }

POST /api/game/chi { player_idx: number, tile: string, pattern: string[] }
  → { success: boolean, game_state: GameState }

POST /api/game/kan { player_idx: number, tile: string }
  → { success: boolean, game_state: GameState }

POST /api/game/pass
  → { success: boolean, game_state: GameState }

GET /api/game/tenpai/:player_idx
  → { is_tenpai: boolean, waiting_tiles: string[] }
```

### WebSocket Events

```typescript
// Server → Client Events
socket.on('game_state_update', (state: GameState) => {
  // Update entire game state
});

socket.on('call_available', (info: CallInfo) => {
  // Show call buttons (Ron, Pon, Chi, Kan)
});

socket.on('round_end', (result: RoundEndResult) => {
  // Show exhaustive draw or win result
});

socket.on('game_end', (result: GameEndResult) => {
  // Show final rankings
});

socket.on('error', (error: ErrorInfo) => {
  // Display error message
});

// Client → Server Events (alternative to REST)
socket.emit('discard_tile', { player_idx, tile, is_drawn });
socket.emit('declare_riichi', { player_idx });
socket.emit('declare_ron', { player_idx });
// ... etc
```

---

## Code Migration Mapping

### Backend (Pure Python - Direct Copy)

| Original File | New Location | Changes Needed |
|--------------|--------------|----------------|
| `app/engine/tiles.py` | `backend/app/engine/tiles.py` | None ✅ |
| `app/engine/player.py` | `backend/app/engine/player.py` | None ✅ |
| `app/engine/game.py` | `backend/app/engine/game.py` | None ✅ |
| `app/engine/scoring.py` | `backend/app/engine/scoring.py` | None ✅ |
| `app/engine/hand_evaluator.py` | `backend/app/engine/hand_evaluator.py` | None ✅ |

### Frontend (Reflex → React Rewrite)

| Original Component | New Component | Complexity |
|-------------------|---------------|------------|
| `app/components/tile_image.py` | `frontend/src/components/Tile.tsx` | Low - Direct translation |
| `app/components/hand.py` | `frontend/src/components/Hand.tsx` | Medium - Reflex state → React state |
| `app/components/board.py` | `frontend/src/components/Board.tsx` | Low - Mostly display |
| `app/components/mahjong_table.py` | `frontend/src/components/MahjongTable.tsx` | Medium - Layout translation |
| `app/components/exhaustive_draw_display.py` | `frontend/src/components/ExhaustiveDrawOverlay.tsx` | Low - Modal overlay |
| `app/components/game_end_screen.py` | `frontend/src/components/GameEndScreen.tsx` | Low - Modal overlay |
| `app/state.py` | `frontend/src/hooks/useGameState.ts` | High - State management change |

---

## Testing Strategy

### Backend Testing

```python
# Test game engine directly (no API layer)
def test_discard_tile():
    game = Game()
    game.start_new_game()
    player = game.players[0]
    initial_hand_size = len(player.hand)

    game.discard_tile(0, player.hand[0], False)

    assert len(player.hand) == initial_hand_size - 1
    assert len(player.discards) == 1

# Test API endpoints
def test_api_discard(client):
    response = client.post('/api/game/new', json={"game_type": "hanchan"})
    assert response.status_code == 200

    response = client.post('/api/game/discard', json={
        "player_idx": 0,
        "tile": "1m",
        "is_drawn": False
    })
    assert response.status_code == 200
    assert response.json['success'] == True
```

### Frontend Testing

```typescript
// Component tests with React Testing Library
test('Tile component renders image', () => {
  render(<Tile tile="1m" size="normal" />);
  const img = screen.getByAltText('1m');
  expect(img).toBeInTheDocument();
  expect(img).toHaveAttribute('src', '/tiles/Man1.svg');
});

// Integration tests
test('Full game flow', async () => {
  render(<App />);

  // Start new game
  await userEvent.click(screen.getByText('New Game (半荘)'));

  // Discard tile
  const tile = screen.getAllByAltText(/[1-9][mps]|[1-7]z/)[0];
  await userEvent.click(tile);

  // Verify state update
  expect(screen.getByText(/Player 1's Turn/)).toBeInTheDocument();
});
```

---

## Rollback Plan

If migration encounters critical issues, we can:

1. **Keep Reflex Version Running**: Original codebase remains in `private-self-mahjong-reflex/`
2. **Gradual Migration**: Can migrate backend first, keep Reflex frontend temporarily
3. **Feature Parity Check**: Maintain checklist of all Phase 1-3 features
4. **Parallel Development**: Run both versions simultaneously during transition

---

## Timeline Summary

| Phase | Duration | Deliverable |
|-------|----------|-------------|
| M1: Backend Setup | 3-4 hours | Flask API + Game Engine |
| M2: Frontend Setup | 3-4 hours | React app scaffold |
| M3: Core UI Components | 6-8 hours | All UI components |
| M4: Game Flow Integration | 3-4 hours | Full game playable |
| M5: End Screens & Polish | 3-4 hours | Migration complete |
| **Total (M1-M5)** | **18-24 hours** | **3-4 days working time** |
| M6: Deployment (Optional) | 8-16 hours | Production-ready |

---

## Next Steps

1. **Review this migration plan** and confirm approach
2. **Create project structure** for Flask/React
3. **Set up development environment** (Python venv, Node.js)
4. **Begin Phase M1** (Backend setup)

Once approved, I'll proceed with creating the project structure and implementing Phase M1.
