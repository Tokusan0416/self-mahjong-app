"""Development server entry point for Mahjong Self-Play Simulator backend."""
from app import create_app, socketio

# Create Flask application
app = create_app()

if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("🀄 Mahjong Self-Play Simulator - Backend Server")
    print("=" * 60)
    print(f"Server: http://localhost:5000")
    print(f"Health Check: http://localhost:5000/health")
    print(f"API Base: http://localhost:5000/api")
    print(f"Tile Images: http://localhost:5000/static/tiles/")
    print("=" * 60 + "\n")

    # Run with SocketIO support
    socketio.run(
        app,
        debug=True,
        host='0.0.0.0',
        port=5000,
        use_reloader=True,
        log_output=True
    )
