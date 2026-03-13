"""REST API routes for game actions."""
from flask import Blueprint, jsonify, request
from app.game_manager import game_manager

api_bp = Blueprint('api', __name__)


@api_bp.route('/game/new', methods=['POST'])
def new_game():
    """
    Start a new game.

    Request JSON:
        {
            "game_type": "hanchan" | "tonpuu"
        }

    Returns:
        {
            "success": true,
            "game_state": {...}
        }
    """
    try:
        data = request.json or {}
        game_type = data.get('game_type', 'hanchan')

        if game_type not in ['hanchan', 'tonpuu']:
            return jsonify({
                'success': False,
                'error': 'Invalid game_type. Must be "hanchan" or "tonpuu"'
            }), 400

        game_state = game_manager.start_new_game(game_type)

        return jsonify({
            'success': True,
            'game_state': game_state
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_bp.route('/game/state', methods=['GET'])
def get_game_state():
    """
    Get current game state.

    Returns:
        {
            "game_state": {...} | null
        }
    """
    try:
        state = game_manager.get_game_state()
        return jsonify({'game_state': state})

    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500


@api_bp.route('/game/discard', methods=['POST'])
def discard_tile():
    """
    Discard a tile.

    Request JSON:
        {
            "player_idx": 0-3,
            "tile": "1m",
            "is_drawn": true|false
        }

    Returns:
        {
            "success": true,
            "game_state": {...}
        }
    """
    try:
        data = request.json
        player_idx = data.get('player_idx')
        tile = data.get('tile')
        is_drawn = data.get('is_drawn', False)

        if player_idx is None or tile is None:
            return jsonify({
                'success': False,
                'error': 'Missing required fields: player_idx, tile'
            }), 400

        game_state = game_manager.discard_tile(player_idx, tile, is_drawn)

        # Emit WebSocket event for real-time update
        from app import socketio
        socketio.emit('game_state_update', game_state)

        return jsonify({
            'success': True,
            'game_state': game_state
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_bp.route('/game/riichi', methods=['POST'])
def declare_riichi():
    """
    Declare riichi.

    Request JSON:
        {
            "player_idx": 0-3
        }

    Returns:
        {
            "success": true,
            "game_state": {...}
        }
    """
    try:
        data = request.json
        player_idx = data.get('player_idx')

        if player_idx is None:
            return jsonify({
                'success': False,
                'error': 'Missing required field: player_idx'
            }), 400

        game_state = game_manager.declare_riichi(player_idx)

        from app import socketio
        socketio.emit('game_state_update', game_state)

        return jsonify({
            'success': True,
            'game_state': game_state
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_bp.route('/game/tsumo', methods=['POST'])
def declare_tsumo():
    """
    Declare tsumo win.

    Request JSON:
        {
            "player_idx": 0-3
        }

    Returns:
        {
            "success": true,
            "game_state": {...},
            "win_info": {...}
        }
    """
    try:
        data = request.json
        player_idx = data.get('player_idx')

        if player_idx is None:
            return jsonify({
                'success': False,
                'error': 'Missing required field: player_idx'
            }), 400

        result = game_manager.declare_tsumo(player_idx)

        from app import socketio
        socketio.emit('win_declared', {
            'type': 'tsumo',
            'game_state': result
        })

        return jsonify({
            'success': True,
            **result
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_bp.route('/game/ron', methods=['POST'])
def declare_ron():
    """
    Declare ron win.

    Request JSON:
        {
            "player_idx": 0-3
        }

    Returns:
        {
            "success": true,
            "game_state": {...},
            "win_info": {...}
        }
    """
    try:
        data = request.json
        player_idx = data.get('player_idx')

        if player_idx is None:
            return jsonify({
                'success': False,
                'error': 'Missing required field: player_idx'
            }), 400

        result = game_manager.declare_ron(player_idx)

        from app import socketio
        socketio.emit('win_declared', {
            'type': 'ron',
            'game_state': result
        })

        return jsonify({
            'success': True,
            **result
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_bp.route('/game/pon', methods=['POST'])
def declare_pon():
    """
    Declare pon.

    Request JSON:
        {
            "player_idx": 0-3,
            "tile": "1m"
        }

    Returns:
        {
            "success": true,
            "game_state": {...}
        }
    """
    try:
        data = request.json
        player_idx = data.get('player_idx')
        tile = data.get('tile')

        if player_idx is None or tile is None:
            return jsonify({
                'success': False,
                'error': 'Missing required fields: player_idx, tile'
            }), 400

        game_state = game_manager.declare_pon(player_idx, tile)

        from app import socketio
        socketio.emit('game_state_update', game_state)

        return jsonify({
            'success': True,
            'game_state': game_state
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_bp.route('/game/chi', methods=['POST'])
def declare_chi():
    """
    Declare chi.

    Request JSON:
        {
            "player_idx": 0-3,
            "tile": "1m",
            "pattern": ["1m", "2m", "3m"]
        }

    Returns:
        {
            "success": true,
            "game_state": {...}
        }
    """
    try:
        data = request.json
        player_idx = data.get('player_idx')
        tile = data.get('tile')
        pattern = data.get('pattern', [])

        if player_idx is None or tile is None or not pattern:
            return jsonify({
                'success': False,
                'error': 'Missing required fields: player_idx, tile, pattern'
            }), 400

        game_state = game_manager.declare_chi(player_idx, tile, pattern)

        from app import socketio
        socketio.emit('game_state_update', game_state)

        return jsonify({
            'success': True,
            'game_state': game_state
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_bp.route('/game/kan', methods=['POST'])
def declare_kan():
    """
    Declare kan.

    Request JSON:
        {
            "player_idx": 0-3,
            "tile": "1m"
        }

    Returns:
        {
            "success": true,
            "game_state": {...}
        }
    """
    try:
        data = request.json
        player_idx = data.get('player_idx')
        tile = data.get('tile')

        if player_idx is None or tile is None:
            return jsonify({
                'success': False,
                'error': 'Missing required fields: player_idx, tile'
            }), 400

        game_state = game_manager.declare_kan(player_idx, tile)

        from app import socketio
        socketio.emit('game_state_update', game_state)

        return jsonify({
            'success': True,
            'game_state': game_state
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_bp.route('/game/pass', methods=['POST'])
def pass_on_calls():
    """
    Pass on all call opportunities.

    Returns:
        {
            "success": true,
            "game_state": {...}
        }
    """
    try:
        game_state = game_manager.pass_on_calls()

        from app import socketio
        socketio.emit('game_state_update', game_state)

        return jsonify({
            'success': True,
            'game_state': game_state
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_bp.route('/game/tenpai/<int:player_idx>', methods=['GET'])
def check_tenpai(player_idx):
    """
    Check tenpai status for player.

    Returns:
        {
            "is_tenpai": true|false,
            "waiting_tiles": [...]
        }
    """
    try:
        result = game_manager.check_tenpai(player_idx)
        return jsonify(result)

    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500


@api_bp.route('/game/continue', methods=['POST'])
def continue_after_draw():
    """
    Continue to next round after exhaustive draw.

    Returns:
        {
            "success": true,
            "game_state": {...}
        }
    """
    try:
        game_state = game_manager.continue_after_exhaustive_draw()

        from app import socketio
        socketio.emit('game_state_update', game_state)

        return jsonify({
            'success': True,
            'game_state': game_state
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
