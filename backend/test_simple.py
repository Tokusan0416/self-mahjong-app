#!/usr/bin/env python
"""Simplified backend test - just verify core functionality."""
import sys

print("🧪 Simple Backend Test\n" + "=" * 60)

# Test 1: Import game engine
try:
    from app.engine.game import MahjongGame
    print("✅ Import MahjongGame")
except Exception as e:
    print(f"❌ Import failed: {e}")
    sys.exit(1)

# Test 2: Create game
try:
    game = MahjongGame(game_type='hanchan')
    print(f"✅ Create game: {game.game_type}")
except Exception as e:
    print(f"❌ Game creation failed: {e}")
    sys.exit(1)

# Test 3: Start round
try:
    game.start_new_round()
    print(f"✅ Start round: {len(game.players)} players, {len(game.wall)} tiles in wall")
except Exception as e:
    print(f"❌ Start round failed: {e}")
    sys.exit(1)

# Test 4: Check game state
try:
    player0 = game.players[0]
    print(f"✅ Player 0 hand: {len(player0.hand)} tiles")
    print(f"✅ Current player: {game.current_player}")
    print(f"✅ Dora indicators: {len(game.dora_indicators)}")
except Exception as e:
    print(f"❌ Game state check failed: {e}")
    sys.exit(1)

# Test 5: Flask app creation
try:
    from app import create_app
    app = create_app()
    print(f"✅ Flask app created: {app.name}")
except Exception as e:
    print(f"❌ Flask app creation failed: {e}")
    sys.exit(1)

# Test 6: Static files
try:
    import os
    tiles_dir = os.path.join(os.path.dirname(__file__), 'static', 'tiles')
    svg_count = len([f for f in os.listdir(tiles_dir) if f.endswith('.svg')])
    print(f"✅ Static files: {svg_count} SVG tiles")
except Exception as e:
    print(f"❌ Static files check failed: {e}")
    sys.exit(1)

print("\n" + "=" * 60)
print("✅ All basic tests passed!")
print("\n🚀 Backend is ready for Phase M2 (Frontend)")
print("\nTo start the server:")
print("  cd backend")
print("  source venv/bin/activate")
print("  python run.py")
