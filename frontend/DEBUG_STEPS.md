# Debug Steps for White Screen Issue

## Issue
Frontend shows a white/blank screen with no content.

## Possible Causes
1. JavaScript error crashing the app
2. WebSocket connection error
3. Missing dependencies
4. TailwindCSS not loading
5. React not mounting

## Debug Step 1: Check Browser Console

**Action**: Open browser console (F12) and check for errors.

Look for errors like:
- `Failed to fetch` - Network/CORS issue
- `WebSocket connection failed` - Backend not running
- `Cannot read property of undefined` - JavaScript error
- `Module not found` - Missing dependency

## Debug Step 2: Test Simple Version

**Action**: Temporarily use the simple test app (no WebSocket).

```bash
# In frontend/src/main.tsx, change line 4:
# FROM: import App from './App.tsx'
# TO:   import App from './App.simple.tsx'
```

Then restart Vite server:
```bash
# Ctrl+C to stop
npm run dev
```

**Expected Result**: If the simple version works, the issue is in App.tsx (likely WebSocket).

## Debug Step 3: Check Backend Status

**Action**: Verify backend is running.

```bash
# In another terminal
curl http://localhost:5000/health

# Expected output:
# {"status":"healthy","service":"mahjong-api"}
```

If backend is not running:
```bash
cd backend
source venv/bin/activate
python run.py
```

## Debug Step 4: Check Network Tab

**Action**: Open browser DevTools → Network tab → Refresh page.

Look for:
- Red/failed requests
- 404 errors for static files
- CORS errors
- WebSocket connection failures

## Debug Step 5: Common Fixes

### Fix 1: Clear Browser Cache
```
Ctrl+Shift+R (hard refresh)
or
Clear cache and hard reload
```

### Fix 2: Restart Vite Dev Server
```bash
# Kill existing process
pkill -f "vite"

# Restart
cd frontend
npm run dev -- --force
```

### Fix 3: Reinstall Dependencies
```bash
cd frontend
rm -rf node_modules
npm install
npm run dev
```

### Fix 4: Check Port Conflicts
```bash
# Check if port 5173 is already in use
lsof -i :5173

# If in use, kill the process
kill -9 <PID>
```

## Debug Step 6: Minimal Test

Create a minimal test file:

**frontend/src/test.html**:
```html
<!DOCTYPE html>
<html>
<head>
  <title>Test</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50">
  <div class="p-8">
    <h1 class="text-4xl font-bold text-blue-600">Test Page</h1>
    <p class="mt-4">If you see this, TailwindCSS is working.</p>
  </div>
  <script>
    console.log('JavaScript is working');
    alert('Test successful!');
  </script>
</body>
</html>
```

Open: `http://localhost:5173/src/test.html`

## Most Likely Issues

### Issue 1: Backend Not Running
**Symptoms**: WebSocket shows "Disconnected"
**Fix**: Start backend on port 5000

### Issue 2: WebSocket Error Crashes App
**Symptoms**: White screen, console shows WebSocket error
**Fix**: Add better error handling in useSocket.ts

### Issue 3: Missing Import
**Symptoms**: Console shows "Cannot find module"
**Fix**: Check all imports in App.tsx, useSocket.ts, gameApi.ts

### Issue 4: TailwindCSS Not Loading
**Symptoms**: White screen, no styles
**Fix**: Check tailwind.config.js and postcss.config.js

## What to Report

When debugging, please provide:
1. Browser console errors (copy full error messages)
2. Network tab status (any red/failed requests?)
3. Vite terminal output (any build errors?)
4. Backend terminal output (is it running?)
5. Does the simple test app work? (App.simple.tsx)

## Quick Fix Commands

```bash
# Terminal 1: Backend
cd backend
source venv/bin/activate
python run.py

# Terminal 2: Frontend (fresh start)
cd frontend
pkill -f vite
rm -rf node_modules/.vite
npm run dev -- --force

# Then open: http://localhost:5173
# And press F12 to open console
```
