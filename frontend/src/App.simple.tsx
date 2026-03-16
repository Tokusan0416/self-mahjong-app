/**
 * Simple test App component without WebSocket
 */

function App() {
  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold text-center text-gray-900 mb-8">
          🀄 Mahjong Self-Play Simulator
        </h1>

        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <h2 className="text-xl font-semibold mb-4">Test Status</h2>
          <div className="space-y-2">
            <p className="text-green-600">✓ React is working</p>
            <p className="text-green-600">✓ TailwindCSS is working</p>
            <p className="text-green-600">✓ TypeScript is compiling</p>
          </div>
        </div>

        <div className="bg-blue-50 border border-blue-200 rounded p-4">
          <p className="text-sm text-blue-800">
            If you can see this, the basic setup is working! Check the browser console (F12) for any errors.
          </p>
        </div>

        <div className="mt-6 text-center">
          <button
            onClick={() => alert('Button works!')}
            className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium"
          >
            Test Button
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;
