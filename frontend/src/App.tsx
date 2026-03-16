/**
 * Main App component
 */
import { useState } from 'react';
import { useSocket } from './hooks/useSocket';
import { gameApi } from './api/gameApi';

function App() {
  const { gameState, isConnected, error, sendPing, updateGameState } = useSocket();
  const [isLoading, setIsLoading] = useState(false);
  const [apiError, setApiError] = useState<string | null>(null);

  const handleStartGame = async (gameType: 'hanchan' | 'tonpuu') => {
    setIsLoading(true);
    setApiError(null);
    try {
      const response = await gameApi.startNewGame(gameType);
      console.log('Game started:', response);
      // Update game state immediately from API response
      if (response.game_state) {
        updateGameState(response.game_state);
      }
    } catch (err) {
      console.error('Failed to start game:', err);
      setApiError(err instanceof Error ? err.message : 'Failed to start game');
    } finally {
      setIsLoading(false);
    }
  };

  const handleTestConnection = () => {
    sendPing();
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <h1 className="text-3xl font-bold text-center text-gray-900">
            🀄 Mahjong Self-Play Simulator
          </h1>
          <p className="text-center text-sm text-gray-500 mt-1">
            Flask + React Migration (Phase M2)
          </p>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-8">
        {/* Connection Status */}
        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <h2 className="text-xl font-semibold mb-4">Connection Status</h2>

          <div className="space-y-3">
            {/* WebSocket Status */}
            <div className="flex items-center justify-between">
              <span className="text-gray-700">WebSocket:</span>
              <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${
                isConnected
                  ? 'bg-green-100 text-green-800'
                  : 'bg-red-100 text-red-800'
              }`}>
                {isConnected ? '✓ Connected' : '✗ Disconnected'}
              </span>
            </div>

            {/* Error Display */}
            {error && (
              <div className="bg-red-50 border border-red-200 rounded p-3">
                <p className="text-sm text-red-700">
                  <strong>Error:</strong> {error}
                </p>
              </div>
            )}

            {/* Test Connection Button */}
            <button
              onClick={handleTestConnection}
              disabled={!isConnected}
              className="w-full px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
            >
              Send Ping (Test Connection)
            </button>
          </div>
        </div>

        {/* Game Controls */}
        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <h2 className="text-xl font-semibold mb-4">Game Controls</h2>

          <div className="space-y-3">
            {apiError && (
              <div className="bg-red-50 border border-red-200 rounded p-3">
                <p className="text-sm text-red-700">
                  <strong>API Error:</strong> {apiError}
                </p>
              </div>
            )}

            <div className="grid grid-cols-2 gap-4">
              <button
                onClick={() => handleStartGame('hanchan')}
                disabled={!isConnected || isLoading}
                className="px-6 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors font-medium"
              >
                {isLoading ? 'Starting...' : 'New Game (半荘)'}
              </button>

              <button
                onClick={() => handleStartGame('tonpuu')}
                disabled={!isConnected || isLoading}
                className="px-6 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors font-medium"
              >
                {isLoading ? 'Starting...' : 'New Game (東風戦)'}
              </button>
            </div>
          </div>
        </div>

        {/* Game State Display */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Game State</h2>

          {gameState ? (
            <div className="space-y-4">
              {/* Basic Info */}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                <div>
                  <div className="text-gray-500">Game Type</div>
                  <div className="font-medium">{gameState.game_type}</div>
                </div>
                <div>
                  <div className="text-gray-500">Current Player</div>
                  <div className="font-medium">{gameState.player_names[gameState.current_player]}</div>
                </div>
                <div>
                  <div className="text-gray-500">Wall Remaining</div>
                  <div className="font-medium">{gameState.wall_remaining} tiles</div>
                </div>
                <div>
                  <div className="text-gray-500">Turn</div>
                  <div className="font-medium">{gameState.turn_count}</div>
                </div>
              </div>

              {/* Players Info */}
              <div>
                <h3 className="font-medium mb-2">Players</h3>
                <div className="space-y-2">
                  {gameState.players.map((player, idx) => (
                    <div
                      key={idx}
                      className={`p-3 rounded border ${
                        idx === gameState.current_player
                          ? 'border-primary-500 bg-primary-50'
                          : 'border-gray-200'
                      }`}
                    >
                      <div className="flex justify-between items-center">
                        <div>
                          <span className="font-medium">{gameState.player_names[idx]}</span>
                          {idx === gameState.dealer && (
                            <span className="ml-2 text-xs bg-yellow-100 text-yellow-800 px-2 py-1 rounded">
                              Dealer
                            </span>
                          )}
                          {player.is_riichi && (
                            <span className="ml-2 text-xs bg-red-100 text-red-800 px-2 py-1 rounded">
                              Riichi
                            </span>
                          )}
                        </div>
                        <div className="text-right">
                          <div className="text-sm text-gray-500">Score</div>
                          <div className="font-medium">{player.score}</div>
                        </div>
                      </div>
                      <div className="mt-2 text-sm text-gray-600">
                        Hand: {player.hand.length} tiles | Discards: {player.discards.length}
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Raw JSON (for debugging) */}
              <details className="mt-4">
                <summary className="cursor-pointer text-sm text-gray-600 hover:text-gray-900">
                  View Raw JSON
                </summary>
                <pre className="mt-2 p-4 bg-gray-100 rounded overflow-auto text-xs">
                  {JSON.stringify(gameState, null, 2)}
                </pre>
              </details>
            </div>
          ) : (
            <div className="text-center text-gray-500 py-8">
              No game in progress. Start a new game to begin.
            </div>
          )}
        </div>
      </main>

      {/* Footer */}
      <footer className="mt-12 py-6 text-center text-sm text-gray-500">
        <p>Phase M2: Frontend Setup Complete ✓</p>
        <p className="mt-1">
          Backend: <code className="text-xs bg-gray-100 px-2 py-1 rounded">http://localhost:5000</code>
          {' | '}
          Frontend: <code className="text-xs bg-gray-100 px-2 py-1 rounded">http://localhost:5173</code>
        </p>
      </footer>
    </div>
  );
}

export default App;
