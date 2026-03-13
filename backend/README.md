# Backend - Flask API Server

Flask backend for Mahjong Self-Play Simulator.

## Quick Start

### 1. Activate Virtual Environment

```bash
source venv/bin/activate
# On Windows: venv\Scripts\activate
```

### 2. Install Dependencies (if not already installed)

```bash
pip install -r requirements.txt
```

### 3. Run Development Server

```bash
python run.py
```

The server will start on `http://localhost:5000`

## API Endpoints

### Health Check
- `GET /health` - Server health check

### Game Management
- `POST /api/game/new` - Start new game
- `GET /api/game/state` - Get current game state

### Game Actions
- `POST /api/game/discard` - Discard a tile
- `POST /api/game/riichi` - Declare riichi
- `POST /api/game/tsumo` - Declare tsumo (self-draw win)
- `POST /api/game/ron` - Declare ron (win on discard)
- `POST /api/game/pon` - Call pon
- `POST /api/game/chi` - Call chi
- `POST /api/game/kan` - Call kan
- `POST /api/game/pass` - Pass on all calls
- `GET /api/game/tenpai/<player_idx>` - Check tenpai status
- `POST /api/game/continue` - Continue after exhaustive draw

### Static Files
- `GET /static/tiles/<filename>.svg` - Serve tile images

## Testing API

### Test Health Check
```bash
curl http://localhost:5000/health
```

### Start New Game
```bash
curl -X POST http://localhost:5000/api/game/new \
  -H "Content-Type: application/json" \
  -d '{"game_type": "hanchan"}'
```

### Get Game State
```bash
curl http://localhost:5000/api/game/state
```

### Test Tile Image
```bash
curl -I http://localhost:5000/static/tiles/Man1.svg
```

## WebSocket Events

The server uses Socket.IO for real-time updates:

### Client → Server
- `connect` - Establish connection
- `disconnect` - Close connection
- `join_game` - Join game room
- `leave_game` - Leave game room
- `request_state` - Request current state
- `ping` - Connection test

### Server → Client
- `connection_status` - Connection established
- `game_state_update` - Game state changed
- `win_declared` - Win occurred (ron/tsumo)
- `pong` - Response to ping

## Project Structure

```
backend/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── routes.py            # REST API endpoints
│   ├── socketio_events.py  # WebSocket handlers
│   ├── game_manager.py      # Game state bridge
│   └── engine/              # Game logic (from Reflex)
│       ├── game.py          # Core game loop
│       ├── player.py        # Player management
│       ├── scoring.py       # Yaku and scoring
│       └── tiles.py         # Tile operations
├── static/
│   └── tiles/               # SVG tile images (43 files)
├── tests/                   # Test files (TODO)
├── venv/                    # Python virtual environment
├── requirements.txt         # Python dependencies
├── run.py                   # Development server entry
└── README.md                # This file
```

## Development

### Running Tests
```bash
pytest
```

### Environment Variables
Create a `.env` file (see `.env.example`):
```bash
FLASK_ENV=development
FLASK_DEBUG=1
SECRET_KEY=your-secret-key
```

### Code Style
The codebase follows:
- PEP 8 style guide
- Type hints for function signatures
- Comprehensive docstrings

## Troubleshooting

### Import Errors
Make sure virtual environment is activated:
```bash
source venv/bin/activate
```

### Port Already in Use
Change port in `run.py`:
```python
socketio.run(app, port=5001)  # Use different port
```

### CORS Issues
CORS is enabled for all origins in development. For production, update `app/__init__.py`:
```python
CORS(app, resources={r"/api/*": {"origins": "https://your-domain.com"}})
```

## Production Deployment

### Using Gunicorn
```bash
pip install gunicorn
gunicorn -k eventlet -w 1 -b 0.0.0.0:5000 "app:create_app()"
```

### Using Docker
```bash
docker build -t mahjong-backend .
docker run -p 5000:5000 mahjong-backend
```

## Next Steps

After backend is running:
1. Set up React frontend (Phase M2)
2. Connect frontend to backend API
3. Test full game flow
4. Deploy both services

See [MIGRATION.md](../MIGRATION.md) for complete migration guide.
