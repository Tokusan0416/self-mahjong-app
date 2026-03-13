"""Flask application factory for Mahjong Self-Play Simulator."""
from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_socketio import SocketIO
import os

socketio = SocketIO()


def create_app():
    """Create and configure Flask application."""
    app = Flask(__name__)

    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', 'True') == 'True'

    # Enable CORS for development
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Initialize SocketIO with CORS support
    socketio.init_app(
        app,
        cors_allowed_origins="*",
        async_mode='eventlet',
        logger=True,
        engineio_logger=True
    )

    # Register blueprints
    from app.routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    # Serve static files (tile images)
    @app.route('/static/tiles/<path:filename>')
    def serve_tile(filename):
        """Serve tile SVG images."""
        static_dir = os.path.join(app.root_path, '..', 'static', 'tiles')
        return send_from_directory(static_dir, filename)

    # Root endpoint - API information
    @app.route('/')
    def index():
        """Root endpoint with API information."""
        return {
            'service': 'Mahjong Self-Play Simulator API',
            'version': '1.0.0',
            'status': 'running',
            'endpoints': {
                'health': '/health',
                'game_api': '/api/game/*',
                'tile_images': '/static/tiles/<filename>.svg',
                'documentation': 'See /api/game/state for current game state'
            },
            'websocket': {
                'url': 'ws://localhost:5000',
                'events': ['game_state_update', 'win_declared', 'connection_status']
            }
        }

    # Health check endpoint
    @app.route('/health')
    def health_check():
        """Health check endpoint."""
        return {'status': 'healthy', 'service': 'mahjong-api'}

    # Register SocketIO events
    from app import socketio_events
    socketio_events.register_events(socketio)

    return app
