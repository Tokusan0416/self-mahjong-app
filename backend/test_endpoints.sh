#!/bin/bash
# Test all backend endpoints

echo "🧪 Testing Backend Endpoints"
echo "=========================================="

echo ""
echo "1. Root endpoint (http://localhost:5000/)"
curl -s http://localhost:5000/ | python -m json.tool

echo ""
echo "2. Health check (http://localhost:5000/health)"
curl -s http://localhost:5000/health | python -m json.tool

echo ""
echo "3. Game state (http://localhost:5000/api/game/state)"
curl -s http://localhost:5000/api/game/state | python -m json.tool

echo ""
echo "4. Start new game (POST http://localhost:5000/api/game/new)"
curl -s -X POST http://localhost:5000/api/game/new \
  -H "Content-Type: application/json" \
  -d '{"game_type": "hanchan"}' | python -m json.tool | head -20

echo ""
echo "5. Tile image (http://localhost:5000/static/tiles/Man1.svg)"
curl -s -I http://localhost:5000/static/tiles/Man1.svg | head -3

echo ""
echo "=========================================="
echo "✅ Endpoint tests complete!"
