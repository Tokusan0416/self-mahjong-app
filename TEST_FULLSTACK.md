# Full Stack Test Instructions

## Current Status
✅ TailwindCSS v3.4.19 installed
✅ PostCSS configuration updated
✅ Backend ready (Phase M1 complete)
✅ Frontend ready (Phase M2 complete)

## Step 1: Start Backend

```bash
# Terminal 1
cd backend
source venv/bin/activate
python run.py
```

Expected output:
```
Server initialized for eventlet.
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
 * Running on http://0.0.0.0:5000
```

## Step 2: Start Frontend

```bash
# Terminal 2
cd frontend
npm run dev
```

Expected output:
```
VITE v6.0.6  ready in XXX ms

➜  Local:   http://localhost:5173/
➜  Network: use --host to expose
➜  press h + enter to show help
```

## Step 3: Open Browser

Open: **http://localhost:5173**

## Expected UI

### 1. Header
- Title: "🀄 Mahjong Self-Play Simulator"
- Subtitle: "Flask + React Migration (Phase M2)"

### 2. Connection Status Section
- **WebSocket**: ✓ Connected (green badge)
- **Send Ping** button (enabled)

### 3. Game Controls Section
- **New Game (半荘)** button (blue, enabled)
- **New Game (東風戦)** button (blue, enabled)

### 4. Game State Section
- Message: "No game in progress. Start a new game to begin."

### 5. Footer
- "Phase M2: Frontend Setup Complete ✓"
- Backend/Frontend URLs

## Step 4: Test Connection

1. Click **"Send Ping (Test Connection)"**
2. Open browser console (F12)
3. Look for: `🏓 Pong received: [timestamp]`

## Step 5: Test New Game

1. Click **"New Game (半荘)"**
2. Wait 1-2 seconds
3. Game State section should update with:
   - Game Type: hanchan
   - Current Player: East
   - Wall Remaining: ~69 tiles
   - Turn: 0
   - 4 Players displayed:
     - East (Dealer badge, blue highlight)
     - South
     - West
     - North
   - Each player:
     - Score: 25000
     - Hand: 13-14 tiles
     - Discards: 0

## Step 6: Check Console

Browser Console (F12) should show:
```
✅ Connected to server
📊 Game state updated: [GameState object]
Game started: [Response object]
```

Backend Terminal should show:
```
Client connected
POST /api/game/new 200 OK
```

## Troubleshooting

### Issue: "✗ Disconnected"
- Check backend is running on port 5000
- Check no other process using port 5000: `lsof -i :5000`

### Issue: TailwindCSS errors
- Version installed: v3.4.19 ✓
- PostCSS config: `tailwindcss: {}` ✓
- If still issues: `npm run dev -- --force`

### Issue: API errors
- Check backend logs for errors
- Verify backend running: `curl http://localhost:5000/health`
- Check CORS settings in Flask

### Issue: Images not loading (future Phase M3)
- Tiles will be text codes for now (e.g., "1m", "2p")
- Image display will be implemented in Phase M3

## Success Criteria

- [ ] Backend running on port 5000
- [ ] Frontend running on port 5173
- [ ] WebSocket shows "✓ Connected"
- [ ] Ping test works (check console)
- [ ] New Game button works
- [ ] Game state displays 4 players
- [ ] Each player has 13-14 tiles
- [ ] Current player (East) is highlighted in blue
- [ ] Dealer badge shows on East
- [ ] All scores are 25000
- [ ] No errors in browser console
- [ ] No errors in backend terminal

## Phase M2 Complete! ✅

If all criteria above are met, Phase M2 is successfully complete and you're ready for Phase M3 (UI Components).
