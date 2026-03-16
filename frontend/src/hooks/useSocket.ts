/**
 * WebSocket hook for real-time game updates
 */
import { useEffect, useState } from 'react';
import { io, Socket } from 'socket.io-client';
import { GameState, WinInfo } from '../types/game';

interface SocketEvents {
  game_state_update: (state: GameState) => void;
  win_declared: (data: { type: 'ron' | 'tsumo'; game_state: GameState; win_info: WinInfo }) => void;
  connection_status: (data: { status: string }) => void;
}

interface UseSocketReturn {
  socket: Socket | null;
  gameState: GameState | null;
  isConnected: boolean;
  error: string | null;
  requestState: () => void;
  sendPing: () => void;
  updateGameState: (state: GameState) => void;
}

export const useSocket = (): UseSocketReturn => {
  const [socket, setSocket] = useState<Socket | null>(null);
  const [gameState, setGameState] = useState<GameState | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Connect to backend WebSocket
    const newSocket = io('http://localhost:5000', {
      transports: ['websocket', 'polling'],
      reconnection: true,
      reconnectionAttempts: 5,
      reconnectionDelay: 1000,
    });

    // Connection events
    newSocket.on('connect', () => {
      console.log('✅ Connected to server');
      setIsConnected(true);
      setError(null);
    });

    newSocket.on('disconnect', () => {
      console.log('❌ Disconnected from server');
      setIsConnected(false);
    });

    newSocket.on('connect_error', (err) => {
      console.error('Connection error:', err.message);
      setError(`Connection failed: ${err.message}`);
      setIsConnected(false);
    });

    // Game events
    newSocket.on('game_state_update', (state: GameState) => {
      console.log('📊 Game state updated:', state);
      setGameState(state);
    });

    newSocket.on('connection_status', (data: { status: string }) => {
      console.log('🔌 Connection status:', data.status);
    });

    newSocket.on('win_declared', (data) => {
      console.log('🎉 Win declared:', data);
      // Handle win notification
    });

    // Ping/pong for connection testing
    newSocket.on('pong', (data: { timestamp: number }) => {
      console.log('🏓 Pong received:', new Date(data.timestamp * 1000).toLocaleTimeString());
    });

    setSocket(newSocket);

    // Cleanup on unmount
    return () => {
      console.log('🔌 Closing WebSocket connection');
      newSocket.close();
    };
  }, []);

  // Helper function to request current game state
  const requestState = () => {
    if (socket) {
      socket.emit('request_state');
    }
  };

  // Helper function to send ping
  const sendPing = () => {
    if (socket) {
      socket.emit('ping');
    }
  };

  // Helper function to manually update game state (for API responses)
  const updateGameState = (state: GameState) => {
    setGameState(state);
  };

  return {
    socket,
    gameState,
    isConnected,
    error,
    requestState,
    sendPing,
    updateGameState,
  };
};
