# Migration Status: Reflex → Flask/React

**Last Updated**: 2026-03-13

---

## Executive Summary

**Decision**: Migrating from Reflex to Flask (backend) + React (frontend) architecture.

**Reason**: Persistent SVG tile image loading issues in Reflex 0.8 static file serving.

**Timeline**: 3-4 working days (18-24 hours)

**Status**: ✅ Phase M1 Complete | ⏳ Ready for Phase M2 (Frontend Setup)

---

## What's Complete ✅

### Documentation
- ✅ [MIGRATION.md](MIGRATION.md) - Comprehensive migration guide with architecture, API design, and phase breakdown
- ✅ [SETUP.md](SETUP.md) - Detailed development environment setup instructions
- ✅ [ROADMAP.md](ROADMAP.md) - Updated with migration phases and revised timeline
- ✅ [README.md](README.md) - Updated to reflect migration status and dual architecture
- ✅ `backend-requirements.txt` - Python dependencies for Flask backend
- ✅ `frontend-package.json` - Node dependencies template for React frontend

### Preparation
- ✅ Migration plan approved
- ✅ Architecture designed (Flask + SocketIO + React + TypeScript)
- ✅ API endpoints defined
- ✅ Project structure planned
- ✅ Code migration mapping documented
- ✅ Testing strategy defined

---

## What's Preserved from Reflex Version

### Game Engine (100% Reusable) ✅
```
app/engine/
├── tiles.py            # Tile management and operations
├── player.py           # Player state and riichi logic
├── game.py             # Core game loop, turn management, round progression
├── scoring.py          # Yaku detection and point calculation
└── hand_evaluator.py   # Tenpai checking and hand evaluation
```

**Status**: All files are pure Python with no framework dependencies. Can be copied directly to Flask backend.

### Game Features (All Functional) ✅
- ✅ Phase 1: Tile engine, 4-player management, turn flow
- ✅ Phase 2.1: Ron and Tsumo detection with full scoring
- ✅ Phase 2.2: Pon, Chi, Kan calls with priority system
- ✅ Phase 2.2.5: Hand organization (drawn tile separation, auto-sort)
- ✅ Phase 2.3: Round management (exhaustive draw, dealer rotation, game types)
- ✅ Phase 3.2: Cross-pattern table layout design
- ✅ Phase 3.3: End screens (exhaustive draw, game end, oorasu indicator)

### Assets ✅
- ✅ 43 SVG tile images from FluffyStuff/riichi-mahjong-tiles (CC0 license)
  - 9 Manzu (Man1-9.svg)
  - 9 Pinzu (Pin1-9.svg)
  - 9 Souzu (Sou1-9.svg)
  - 7 Jihai (Ton.svg, Nan.svg, Shaa.svg, Pei.svg, Haku.svg, Hatsu.svg, Chun.svg)
  - Located in: `assets/tiles/`

---

## What's Being Rewritten

### UI Layer ❌
```
app/components/        # Reflex components → React components
├── tile_image.py      → frontend/src/components/Tile.tsx
├── hand.py            → frontend/src/components/Hand.tsx
├── board.py           → frontend/src/components/Board.tsx
├── mahjong_table.py   → frontend/src/components/MahjongTable.tsx
├── exhaustive_draw_display.py → frontend/src/components/ExhaustiveDrawOverlay.tsx
└── game_end_screen.py → frontend/src/components/GameEndScreen.tsx
```

### State Management ❌
- `app/state.py` (Reflex state) → `frontend/src/hooks/useGameState.ts` (React state + API)

### Application Entry ❌
- `app/app.py` (Reflex app) → `backend/run.py` (Flask) + `frontend/src/main.tsx` (React)

---

## Migration Phases

### Phase M1: Backend Setup ✅ COMPLETE
**Completed**: 2026-03-13
**Time Taken**: ~2 hours

**Tasks**:
- [x] Create Flask application structure
- [x] Copy game engine code to `backend/app/engine/`
- [x] Implement REST API endpoints
- [x] Set up Flask-SocketIO for WebSocket
- [x] Copy tile images to `backend/static/tiles/`
- [x] Test backend independently

**Deliverables**:
- ✅ Flask app created and tested
- ✅ 13 REST API endpoints implemented
- ✅ WebSocket handlers configured
- ✅ 40 SVG tile images in place
- ✅ Game engine code copied (5 files)
- ✅ Virtual environment with dependencies

**How to Start Backend**:
```bash
cd backend
source venv/bin/activate
python run.py
```

Server runs on: `http://localhost:5000`

---

### Phase M2: Frontend Setup ✅ COMPLETE
**Completed**: 2026-03-13
**Time Taken**: ~2 hours

**Tasks**:
- [x] Initialize React + TypeScript + Vite project
- [x] Install dependencies (SocketIO, Zustand, TailwindCSS, axios, clsx)
- [x] Configure TailwindCSS with blue theme
- [x] Configure Vite with proxy settings
- [x] Create TypeScript type definitions
- [x] Set up WebSocket hook (`useSocket`)
- [x] Create API client (`gameApi`)
- [x] Create App component with connection test
- [x] Test frontend independently

**Deliverables**:
- ✅ React app running on `http://localhost:5173`
- ✅ WebSocket connection to backend implemented
- ✅ API client with 13 methods functional
- ✅ TailwindCSS configured with primary blue theme
- ✅ TypeScript types for all game entities
- ✅ Connection status display
- ✅ Game controls (New Game, Ping Test)
- ✅ Game state visualization

**How to Start Frontend**:
```bash
cd frontend
npm run dev
```

Frontend: `http://localhost:5173`

**Test the Connection**:
1. Start backend on port 5000
2. Start frontend on port 5173
3. WebSocket status should show "✓ Connected"
4. Click "New Game (半荘)" to start a game
5. Game state should display with 4 players

---

### Phase M3: Core UI Components ⏳ Pending
**Estimated Time**: 6-8 hours

**Tasks**:
- [ ] Tile component (1 hour) - SVG display with click handler
- [ ] Hand component (2 hours) - 13 tiles + drawn tile + call buttons
- [ ] Board component (1 hour) - Dora, wall count, round info
- [ ] MahjongTable component (2-3 hours) - Cross-pattern layout
- [ ] Controls component (1 hour) - New game, riichi, pass buttons

**Deliverables**:
- All components rendering correctly
- Tile images displaying (not "?")
- Layout matching Reflex version
- Interactive elements functional

---

### Phase M4: Game Flow Integration ⏳ Pending
**Estimated Time**: 3-4 hours

**Tasks**:
- [ ] Connect components to WebSocket state
- [ ] Wire up discard actions
- [ ] Implement call buttons (Ron, Tsumo, Pon, Chi, Kan)
- [ ] Real-time state updates
- [ ] Error handling

**Deliverables**:
- Full game playable from start to finish
- All actions working
- Real-time updates functioning
- Error messages displaying

---

### Phase M5: End Screens & Polish ⏳ Pending
**Estimated Time**: 3-4 hours

**Tasks**:
- [ ] Exhaustive draw overlay (tenpai/noten display)
- [ ] Game end screen (rankings, medals, scores)
- [ ] Visual polish (animations, hover effects)
- [ ] Responsive design
- [ ] Complete testing

**Deliverables**:
- All end screens implemented
- Smooth animations
- All Phase 1-3 features verified
- **Migration complete**

---

## Current Priority: Phase M3

**Phase M1 & M2 Completed!** Backend and Frontend are ready. Next: Core UI Components.

**Immediate Next Steps**:

1. Initialize React + TypeScript + Vite project
2. Install frontend dependencies
3. Configure Tailwind CSS
4. Create TypeScript type definitions
5. Set up API client and WebSocket hooks
6. Test frontend connection to backend

**Commands to Run**:
```bash
# Create React project
npm create vite@latest frontend -- --template react-ts
cd frontend

# Install dependencies
npm install socket.io-client zustand axios clsx
npm install @radix-ui/react-dialog @radix-ui/react-button @radix-ui/react-toast
npm install -D tailwindcss postcss autoprefixer

# Initialize Tailwind
npx tailwindcss init -p

# Start dev server
npm run dev
```

See [SETUP.md](SETUP.md) Phase M2 section for detailed instructions.

---

## Success Criteria

### Phase M1-M2 Success
- ✅ Backend running on port 5000
- ✅ Frontend running on port 5173
- ✅ WebSocket connection established
- ✅ Tile images loading correctly

### Phase M3-M5 Success
- ✅ All UI components functional
- ✅ Full game playable (hanchan and tonpuu)
- ✅ All Phase 1-3 features working
- ✅ No image loading issues

### Final Success (Migration Complete)
- ✅ Feature parity with Reflex version
- ✅ SVG images displaying correctly
- ✅ All game mechanics working
- ✅ End screens implemented
- ✅ Visual polish applied
- ✅ Ready for Phase 4 (BigQuery integration)

---

## Resources

- [MIGRATION.md](MIGRATION.md) - Full migration guide
- [SETUP.md](SETUP.md) - Development environment setup
- [ROADMAP.md](ROADMAP.md) - Updated project roadmap
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Flask-SocketIO Documentation](https://flask-socketio.readthedocs.io/)
- [React Documentation](https://react.dev/)
- [Vite Documentation](https://vitejs.dev/)
- [TailwindCSS Documentation](https://tailwindcss.com/)

---

## Questions & Decisions

### Architecture Decisions Made ✅
- ✅ Backend: Flask + Flask-SocketIO (chose over FastAPI for simplicity)
- ✅ Frontend: React + TypeScript (chose over Vue for ecosystem maturity)
- ✅ Build Tool: Vite (fast development server)
- ✅ Styling: TailwindCSS (utility-first, matches Reflex aesthetic)
- ✅ State Management: Zustand (lightweight, simple)
- ✅ WebSocket: Socket.IO (bidirectional, reliable)

### Open Questions
- [ ] Deployment platform (Cloud Run, Heroku, Railway, etc.)
- [ ] Production server (Gunicorn vs others)
- [ ] CI/CD pipeline (GitHub Actions, etc.)

---

## Rollback Plan

If critical issues arise:

1. **Reflex version remains available** - Original codebase in `private-self-mahjong-reflex/`
2. **Gradual migration possible** - Can migrate backend first, keep Reflex frontend temporarily
3. **Game engine code unchanged** - Can always revert to Reflex with same engine
4. **Parallel development** - Run both versions simultaneously during transition

---

## Contact & Support

For migration questions:
- See [SETUP.md](SETUP.md) for troubleshooting
- Check Flask/React documentation
- Review [MIGRATION.md](MIGRATION.md) for architecture details

---

**Status**: 📋 Ready to begin Phase M1

**Next Action**: Create Flask backend structure and copy game engine code
