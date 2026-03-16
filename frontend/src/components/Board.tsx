/**
 * Board component - displays game information (dora, wall, round info)
 */
import Tile from './Tile';

interface BoardProps {
  /** Dora indicator tiles */
  doraIndicators: string[];
  /** Number of tiles remaining in the wall */
  wallRemaining: number;
  /** Round wind (0=East, 1=South, 2=West, 3=North) */
  roundWind: number;
  /** Round number within the wind (0-3) */
  roundNumber: number;
  /** Number of honba sticks (連荘カウンター) */
  honbaSticks: number;
  /** Number of riichi sticks */
  riichiSticks: number;
  /** Current player index */
  currentPlayer: number;
  /** Player names */
  playerNames: string[];
  /** Game type */
  gameType: string;
  /** Turn count */
  turnCount: number;
}

/**
 * Get round name (e.g., "東1", "南3")
 */
function getRoundName(roundWind: number, roundNumber: number): string {
  const windNames = ['東', '南', '西', '北'];
  const windName = windNames[roundWind] || '?';
  const roundNum = roundNumber + 1;
  return `${windName}${roundNum}`;
}

/**
 * Check if this is oorasu (final round)
 */
function isOorasu(gameType: string, roundWind: number, roundNumber: number): boolean {
  if (gameType === 'tonpuu') {
    // 東風戦: Last round is 東4
    return roundWind === 0 && roundNumber === 3;
  } else {
    // 半荘: Last round is 南4
    return roundWind === 1 && roundNumber === 3;
  }
}

export default function Board({
  doraIndicators,
  wallRemaining,
  roundWind,
  roundNumber,
  honbaSticks,
  riichiSticks,
  currentPlayer,
  playerNames,
  gameType,
  turnCount,
}: BoardProps) {
  const roundName = getRoundName(roundWind, roundNumber);
  const oorasu = isOorasu(gameType, roundWind, roundNumber);

  return (
    <div className="bg-white rounded-lg shadow-lg p-6 border-2 border-gray-300">
      {/* Title */}
      <div className="text-center mb-4">
        <h2 className="text-2xl font-bold text-gray-800">
          {roundName}局 {honbaSticks > 0 && `${honbaSticks}本場`}
          {oorasu && <span className="ml-2 text-red-600">オーラス</span>}
        </h2>
        <div className="text-sm text-gray-600 mt-1">
          {gameType === 'hanchan' ? '半荘' : '東風戦'} | Turn {turnCount}
        </div>
      </div>

      {/* Main info grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
        {/* Current Player */}
        <div className="bg-blue-50 rounded-lg p-3 border border-blue-200">
          <div className="text-xs text-blue-700 font-medium mb-1">Current Player</div>
          <div className="text-lg font-bold text-blue-900">
            {playerNames[currentPlayer]}
          </div>
        </div>

        {/* Wall Remaining */}
        <div className="bg-green-50 rounded-lg p-3 border border-green-200">
          <div className="text-xs text-green-700 font-medium mb-1">Wall Remaining</div>
          <div className="text-lg font-bold text-green-900">
            {wallRemaining} tiles
          </div>
        </div>

        {/* Honba Sticks */}
        <div className="bg-yellow-50 rounded-lg p-3 border border-yellow-200">
          <div className="text-xs text-yellow-700 font-medium mb-1">本場 (Honba)</div>
          <div className="text-lg font-bold text-yellow-900">
            {honbaSticks} {honbaSticks === 1 ? 'stick' : 'sticks'}
          </div>
        </div>

        {/* Riichi Sticks */}
        <div className="bg-red-50 rounded-lg p-3 border border-red-200">
          <div className="text-xs text-red-700 font-medium mb-1">立直棒 (Riichi)</div>
          <div className="text-lg font-bold text-red-900">
            {riichiSticks} {riichiSticks === 1 ? 'stick' : 'sticks'}
          </div>
        </div>
      </div>

      {/* Dora Indicators */}
      <div className="bg-gradient-to-r from-purple-50 to-pink-50 rounded-lg p-4 border-2 border-purple-300">
        <div className="text-sm font-bold text-purple-900 mb-2 flex items-center gap-2">
          <span>ドラ表示牌 (Dora Indicators)</span>
          <span className="text-xs bg-purple-200 text-purple-800 px-2 py-0.5 rounded">
            {doraIndicators.length}
          </span>
        </div>
        <div className="flex flex-wrap gap-2 justify-center">
          {doraIndicators.map((dora, idx) => (
            <div key={`dora-${idx}`} className="relative">
              <Tile tile={dora} size="normal" />
              {idx === 0 && (
                <div className="absolute -top-1 -right-1 bg-yellow-400 text-yellow-900 text-xs font-bold rounded-full w-5 h-5 flex items-center justify-center border border-yellow-600">
                  1
                </div>
              )}
            </div>
          ))}
          {doraIndicators.length === 0 && (
            <div className="text-sm text-gray-500 italic">No dora indicators yet</div>
          )}
        </div>
        <div className="mt-2 text-xs text-center text-purple-700">
          💡 The actual dora is the next tile in sequence
        </div>
      </div>

      {/* Legend */}
      <div className="mt-4 pt-4 border-t border-gray-200">
        <details className="text-xs text-gray-600">
          <summary className="cursor-pointer font-medium hover:text-gray-900">
            📖 Game Info Legend
          </summary>
          <div className="mt-2 space-y-1 pl-4">
            <div>• <strong>本場 (Honba)</strong>: Bonus counters from consecutive dealer wins or draws</div>
            <div>• <strong>立直棒 (Riichi sticks)</strong>: 1000-point sticks from riichi declarations</div>
            <div>• <strong>ドラ (Dora)</strong>: Bonus tiles that increase hand value</div>
            <div>• <strong>オーラス (Oorasu)</strong>: Final round of the game</div>
          </div>
        </details>
      </div>
    </div>
  );
}
