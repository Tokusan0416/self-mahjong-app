#!/usr/bin/env python
"""Simple API test script for backend verification."""
import sys
import json

def test_imports():
    """Test that all imports work."""
    print("🧪 Testing imports...")
    try:
        from app.engine.game import MahjongGame
        print("  ✅ MahjongGame import OK")

        from app import create_app, socketio
        print("  ✅ Flask app import OK")

        from app.game_manager import game_manager
        print("  ✅ GameManager import OK")

        return True
    except Exception as e:
        print(f"  ❌ Import error: {e}")
        return False


def test_game_engine():
    """Test game engine functionality."""
    print("\n🧪 Testing game engine...")
    try:
        from app.game_manager import game_manager

        # Start new game
        state = game_manager.start_new_game('hanchan')
        print(f"  ✅ New game started: {state['game_type']}")
        print(f"  ✅ Players initialized: {len(state['players'])} players")
        print(f"  ✅ Wall remaining: {state['wall_remaining']} tiles")
        print(f"  ✅ Current player: {state['player_names'][state['current_player']]}")

        # Test discard
        player = state['players'][0]
        if player['hand']:
            tile_to_discard = player['hand'][0]
            new_state = game_manager.discard_tile(0, tile_to_discard, False)
            print(f"  ✅ Discard test OK: {tile_to_discard}")

        # Test tenpai check
        tenpai_result = game_manager.check_tenpai(0)
        print(f"  ✅ Tenpai check OK: {tenpai_result['is_tenpai']}")

        return True
    except Exception as e:
        print(f"  ❌ Game engine error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_flask_app():
    """Test Flask app creation."""
    print("\n🧪 Testing Flask app...")
    try:
        from app import create_app

        app = create_app()
        print(f"  ✅ Flask app created: {app.name}")
        print(f"  ✅ Debug mode: {app.config['DEBUG']}")

        # Test routes are registered
        rules = [rule.rule for rule in app.url_map.iter_rules()]
        api_routes = [r for r in rules if r.startswith('/api/')]
        print(f"  ✅ API routes registered: {len(api_routes)} routes")

        # Show some key routes
        key_routes = ['/api/game/new', '/api/game/state', '/api/game/discard']
        for route in key_routes:
            if route in rules:
                print(f"    ✓ {route}")

        return True
    except Exception as e:
        print(f"  ❌ Flask app error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_static_files():
    """Test that static files exist."""
    print("\n🧪 Testing static files...")
    try:
        import os

        static_dir = os.path.join(os.path.dirname(__file__), 'static', 'tiles')
        if not os.path.exists(static_dir):
            print(f"  ❌ Static directory not found: {static_dir}")
            return False

        svg_files = [f for f in os.listdir(static_dir) if f.endswith('.svg')]
        print(f"  ✅ Found {len(svg_files)} SVG files")

        # Check for key tiles
        key_tiles = ['Man1.svg', 'Pin1.svg', 'Sou1.svg', 'Ton.svg', 'Haku.svg']
        for tile in key_tiles:
            if tile in svg_files:
                print(f"    ✓ {tile}")
            else:
                print(f"    ✗ {tile} missing")

        return len(svg_files) > 0
    except Exception as e:
        print(f"  ❌ Static files error: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("🀄 Backend Verification Tests")
    print("=" * 60)

    results = []

    results.append(("Imports", test_imports()))
    results.append(("Game Engine", test_game_engine()))
    results.append(("Flask App", test_flask_app()))
    results.append(("Static Files", test_static_files()))

    print("\n" + "=" * 60)
    print("📊 Test Results")
    print("=" * 60)

    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status:12} {test_name}")

    all_passed = all(result[1] for result in results)

    print("=" * 60)
    if all_passed:
        print("✅ All tests passed! Backend is ready.")
        print("\n🚀 To start the server:")
        print("   cd backend")
        print("   source venv/bin/activate")
        print("   python run.py")
        return 0
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return 1


if __name__ == '__main__':
    sys.exit(main())
