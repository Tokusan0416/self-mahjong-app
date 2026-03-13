"""WebSocket event handlers for real-time game updates."""
from flask_socketio import emit, join_room, leave_room
from app.game_manager import game_manager


def register_events(socketio):
    """Register all SocketIO event handlers."""

    @socketio.on('connect')
    def handle_connect():
        """Handle client connection."""
        print('Client connected')
        emit('connection_status', {'status': 'connected'})

        # Send current game state if available
        game_state = game_manager.get_game_state()
        if game_state:
            emit('game_state_update', game_state)

    @socketio.on('disconnect')
    def handle_disconnect():
        """Handle client disconnection."""
        print('Client disconnected')

    @socketio.on('join_game')
    def handle_join_game(data):
        """Join game room for updates."""
        room = data.get('game_id', 'default_game')
        join_room(room)
        emit('joined_game', {'room': room})

    @socketio.on('leave_game')
    def handle_leave_game(data):
        """Leave game room."""
        room = data.get('game_id', 'default_game')
        leave_room(room)
        emit('left_game', {'room': room})

    @socketio.on('request_state')
    def handle_request_state():
        """Request current game state."""
        game_state = game_manager.get_game_state()
        emit('game_state_update', game_state)

    @socketio.on('ping')
    def handle_ping():
        """Handle ping for connection testing."""
        emit('pong', {'timestamp': __import__('time').time()})

    return socketio
