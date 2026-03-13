# Setup Guide for Flask + React Migration

This guide walks through setting up the development environment for the Flask (backend) + React (frontend) architecture.

## Prerequisites

Before starting, ensure you have:

- **Python 3.11+** installed
  ```bash
  python --version  # Should be 3.11 or higher
  ```

- **Node.js 18+** installed
  ```bash
  node --version    # Should be 18.0.0 or higher
  npm --version     # Should be 9.0.0 or higher
  ```

- **Git** installed (for version control)

- **Code Editor** (VS Code recommended with Python and TypeScript extensions)

---

## Phase M1: Backend Setup

### Step 1: Create Backend Directory Structure

```bash
# From project root
mkdir -p backend/app/engine
mkdir -p backend/static/tiles
mkdir -p backend/tests
```

### Step 2: Copy Game Engine Code

```bash
# Copy the entire engine directory (pure Python, no changes needed)
cp -r app/engine/* backend/app/engine/

# Verify all files copied
ls -la backend/app/engine/
# Should see: tiles.py, player.py, game.py, scoring.py, hand_evaluator.py
```

### Step 3: Copy Tile Images

```bash
# Copy SVG tile images
cp assets/tiles/*.svg backend/static/tiles/

# Verify 43 tiles copied
ls backend/static/tiles/*.svg | wc -l
# Should output: 43
```

### Step 4: Set Up Python Virtual Environment

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Upgrade pip
pip install --upgrade pip
```

### Step 5: Install Python Dependencies

```bash
# Install from requirements file
pip install -r ../backend-requirements.txt

# Verify mahjong library installed correctly
python -c "import mahjong; print('Mahjong library OK')"
```

### Step 6: Create Flask Application Files

Create `backend/app/__init__.py`:

```python
"""Flask application factory."""
from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO

socketio = SocketIO()

def create_app():
    """Create and configure Flask application."""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'

    # Enable CORS for development
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Initialize SocketIO
    socketio.init_app(app, cors_allowed_origins="*")

    # Register blueprints
    from app.routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    # Serve static files (tile images)
    @app.route('/static/<path:filename>')
    def serve_static(filename):
        return app.send_static_file(filename)

    return app
```

Create `backend/app/routes.py`:

```python
"""REST API routes for game actions."""
from flask import Blueprint, jsonify, request
from app.game_manager import GameManager

api_bp = Blueprint('api', __name__)
game_manager = GameManager()

@api_bp.route('/game/new', methods=['POST'])
def new_game():
    """Start a new game."""
    data = request.json
    game_type = data.get('game_type', 'hanchan')
    game_state = game_manager.start_new_game(game_type)
    return jsonify({'success': True, 'game_state': game_state})

@api_bp.route('/game/state', methods=['GET'])
def get_game_state():
    """Get current game state."""
    state = game_manager.get_game_state()
    return jsonify({'game_state': state})

# Add more routes for discard, riichi, ron, tsumo, pon, chi, kan, pass...
```

Create `backend/app/game_manager.py`:

```python
"""Game state manager - bridges Flask routes and game engine."""
from app.engine.game import Game

class GameManager:
    """Manages game instance and provides serializable state."""

    def __init__(self):
        self.game = None

    def start_new_game(self, game_type='hanchan'):
        """Start new game and return initial state."""
        self.game = Game()
        self.game.start_new_game(game_type=game_type)
        return self.get_game_state()

    def get_game_state(self):
        """Get serializable game state."""
        if not self.game:
            return None

        return {
            'players': [
                {
                    'hand': p.hand,
                    'discards': p.discards,
                    'melds': p.melds,
                    'score': p.score,
                    'is_riichi': p.is_riichi,
                    'last_drawn_tile': p.last_drawn_tile
                }
                for p in self.game.players
            ],
            'current_player': self.game.current_player,
            'wall_remaining': len(self.game.wall),
            'dora_indicators': self.game.dora_indicators,
            'round_wind': self.game.round_wind,
            'round_number': self.game.round_number,
            # ... add more fields as needed
        }
```

Create `backend/run.py`:

```python
"""Development server entry point."""
from app import create_app, socketio

app = create_app()

if __name__ == '__main__':
    # Run with SocketIO support
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
```

### Step 7: Test Backend

```bash
# From backend directory with venv activated
python run.py

# Should see:
#  * Running on http://127.0.0.1:5000
#  * Running on http://0.0.0.0:5000

# Test in another terminal:
curl http://localhost:5000/api/game/state
# Should return: {"game_state": null}

curl -X POST http://localhost:5000/api/game/new \
  -H "Content-Type: application/json" \
  -d '{"game_type": "hanchan"}'
# Should return game state with players array

# Test tile image serving:
curl -I http://localhost:5000/static/tiles/Man1.svg
# Should return: HTTP/1.1 200 OK
```

---

## Phase M2: Frontend Setup

### Step 1: Create Frontend Project

```bash
# From project root
npm create vite@latest frontend -- --template react-ts

# Alternative if above doesn't work:
npm create vite@latest
# Then select: React → TypeScript
# Project name: frontend
```

### Step 2: Install Dependencies

```bash
cd frontend

# Install runtime dependencies
npm install socket.io-client zustand axios
npm install @radix-ui/react-dialog @radix-ui/react-button @radix-ui/react-toast
npm install clsx

# Install dev dependencies
npm install -D tailwindcss postcss autoprefixer

# Initialize Tailwind CSS
npx tailwindcss init -p
```

### Step 3: Configure Tailwind CSS

Edit `frontend/tailwind.config.js`:

```javascript
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Match Reflex blue theme
        primary: {
          50: '#eff6ff',
          100: '#dbeafe',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
        }
      }
    },
  },
  plugins: [],
}
```

Edit `frontend/src/index.css`:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  body {
    @apply bg-gray-50 text-gray-900 antialiased;
  }
}
```

### Step 4: Configure Vite

Edit `frontend/vite.config.ts`:

```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      // Proxy API requests to Flask backend
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
      '/socket.io': {
        target: 'http://localhost:5000',
        changeOrigin: true,
        ws: true,
      },
    },
  },
})
```

### Step 5: Create TypeScript Type Definitions

Create `frontend/src/types/game.ts`:

```typescript
export interface Player {
  hand: string[];
  discards: string[];
  melds: string[];
  score: number;
  is_riichi: boolean;
  last_drawn_tile: string;
}

export interface GameState {
  players: Player[];
  current_player: number;
  wall_remaining: number;
  dora_indicators: string[];
  round_wind: string;
  round_number: number;
  honba_sticks: number;
  riichi_sticks: number;
  game_type: string;
  is_game_over: boolean;
  is_exhaustive_draw: boolean;
}

export interface WinInfo {
  winner_idx: number;
  loser_idx?: number;
  yaku_list: Array<{name: string, han: number}>;
  han: number;
  fu: number;
  points: number;
  is_dealer: boolean;
}
```

### Step 6: Create WebSocket Hook

Create `frontend/src/hooks/useSocket.ts`:

```typescript
import { useEffect, useState } from 'react';
import { io, Socket } from 'socket.io-client';
import { GameState } from '../types/game';

export const useSocket = () => {
  const [socket, setSocket] = useState<Socket | null>(null);
  const [gameState, setGameState] = useState<GameState | null>(null);
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    const newSocket = io('http://localhost:5000');

    newSocket.on('connect', () => {
      console.log('Connected to server');
      setIsConnected(true);
    });

    newSocket.on('disconnect', () => {
      console.log('Disconnected from server');
      setIsConnected(false);
    });

    newSocket.on('game_state_update', (state: GameState) => {
      console.log('Game state updated:', state);
      setGameState(state);
    });

    setSocket(newSocket);

    return () => {
      newSocket.close();
    };
  }, []);

  return { socket, gameState, isConnected };
};
```

### Step 7: Create API Client

Create `frontend/src/api/gameApi.ts`:

```typescript
import axios from 'axios';
import { GameState } from '../types/game';

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const gameApi = {
  startNewGame: async (gameType: 'hanchan' | 'tonpuu') => {
    const response = await api.post<{success: boolean, game_state: GameState}>(
      '/game/new',
      { game_type: gameType }
    );
    return response.data;
  },

  getGameState: async () => {
    const response = await api.get<{game_state: GameState}>('/game/state');
    return response.data;
  },

  discardTile: async (playerIdx: number, tile: string, isDrawn: boolean) => {
    const response = await api.post('/game/discard', {
      player_idx: playerIdx,
      tile,
      is_drawn: isDrawn
    });
    return response.data;
  },

  // Add more API methods as needed...
};
```

### Step 8: Create Basic App Component

Edit `frontend/src/App.tsx`:

```typescript
import { useSocket } from './hooks/useSocket';
import './App.css';

function App() {
  const { socket, gameState, isConnected } = useSocket();

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-4xl font-bold text-center mb-8">
          🀄 Mahjong Self-Play Simulator
        </h1>

        <div className="text-center mb-4">
          <span className={`inline-block px-3 py-1 rounded ${
            isConnected ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
          }`}>
            {isConnected ? '✓ Connected' : '✗ Disconnected'}
          </span>
        </div>

        {gameState ? (
          <pre className="bg-white p-4 rounded shadow overflow-auto">
            {JSON.stringify(gameState, null, 2)}
          </pre>
        ) : (
          <div className="text-center text-gray-500">
            No game in progress. Start a new game to begin.
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
```

### Step 9: Test Frontend

```bash
# From frontend directory
npm run dev

# Should see:
#   VITE v6.0.6  ready in XXX ms
#   ➜  Local:   http://localhost:5173/
#   ➜  Network: use --host to expose

# Open http://localhost:5173 in browser
# Should see connection status and "No game in progress" message
```

---

## Verify Full Stack

### Test 1: Backend Only

```bash
# Terminal 1: Run backend
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
python run.py
```

### Test 2: Frontend Only

```bash
# Terminal 2: Run frontend
cd frontend
npm run dev
```

### Test 3: End-to-End

1. Open browser to `http://localhost:5173`
2. Check connection status shows "✓ Connected"
3. Open browser console (F12) and run:
   ```javascript
   fetch('/api/game/new', {
     method: 'POST',
     headers: {'Content-Type': 'application/json'},
     body: JSON.stringify({game_type: 'hanchan'})
   })
   .then(r => r.json())
   .then(console.log)
   ```
4. Should see game state logged in console

---

## Common Issues & Solutions

### Issue: Backend won't start

**Error**: `ModuleNotFoundError: No module named 'flask'`

**Solution**: Activate virtual environment and reinstall dependencies
```bash
cd backend
source venv/bin/activate
pip install -r ../backend-requirements.txt
```

### Issue: Frontend Vite proxy not working

**Error**: `Failed to fetch` or CORS errors

**Solution**: Ensure backend is running on port 5000 and Vite proxy config is correct

```bash
# Check if backend is running:
curl http://localhost:5000/api/game/state

# Restart frontend with clean cache:
npm run dev -- --force
```

### Issue: Tile images not loading

**Error**: 404 on `/static/tiles/Man1.svg`

**Solution**: Verify tiles copied to `backend/static/tiles/`
```bash
ls backend/static/tiles/*.svg | wc -l
# Should be: 43
```

### Issue: SocketIO connection fails

**Error**: WebSocket connection failed

**Solution**: Check Flask-SocketIO and eventlet installed
```bash
pip list | grep -i socketio
pip list | grep -i eventlet

# If missing, reinstall:
pip install Flask-SocketIO eventlet
```

---

## Next Steps

Once both backend and frontend are running successfully:

1. ✅ **Phase M1 Complete**: Backend serving API and static files
2. ✅ **Phase M2 Complete**: Frontend connected via WebSocket
3. ➡️ **Phase M3**: Build React components (Tile, Hand, Board, MahjongTable)
4. ➡️ **Phase M4**: Wire up game actions and real-time updates
5. ➡️ **Phase M5**: Add end screens and polish

See [MIGRATION.md](MIGRATION.md) for detailed phase breakdowns.

---

## Development Workflow

### Starting Development

```bash
# Terminal 1: Backend
cd backend
source venv/bin/activate
python run.py

# Terminal 2: Frontend
cd frontend
npm run dev
```

### Making Changes

- **Backend**: Edit files in `backend/app/`, Flask auto-reloads
- **Frontend**: Edit files in `frontend/src/`, Vite hot-reloads
- **Game Engine**: Edit files in `backend/app/engine/`, restart Flask

### Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests (when added)
cd frontend
npm test
```

---

## Environment Variables (Optional)

Create `backend/.env`:

```bash
FLASK_ENV=development
FLASK_DEBUG=1
SECRET_KEY=your-secret-key-here
```

Create `frontend/.env`:

```bash
VITE_API_URL=http://localhost:5000
```

---

## Ready to Start?

If everything is set up correctly, you should have:

- ✅ Backend running on `http://localhost:5000`
- ✅ Frontend running on `http://localhost:5173`
- ✅ WebSocket connection established
- ✅ Tile images accessible
- ✅ Game engine code copied and functional

**You're ready to begin Phase M3: Core UI Components!**
