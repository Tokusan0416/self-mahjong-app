/**
 * Hand component - displays a player's hand with tiles
 */
import { useMemo } from 'react';
import Tile from './Tile';
import { Meld } from '../types/game';

interface HandProps {
  /** Player's hand tiles (typically 13 or 14) */
  hand: string[];
  /** Last drawn tile (displayed separately) */
  lastDrawnTile: string;
  /** Player's melds (open sets) */
  melds: Meld[];
  /** Whether this is the current player (interactive mode) */
  isCurrentPlayer: boolean;
  /** Whether this hand is in tenpai */
  isTenpai?: boolean;
  /** Tile size */
  size?: 'small' | 'normal' | 'large';
  /** Call availability flags */
  canRon?: boolean;
  canTsumo?: boolean;
  canPon?: boolean;
  canChi?: boolean;
  canKan?: boolean;
  /** Callbacks */
  onDiscardTile?: (tile: string, isDrawn: boolean) => void;
  onDeclareRon?: () => void;
  onDeclareTsumo?: () => void;
  onDeclarePon?: () => void;
  onDeclareChi?: () => void;
  onDeclareKan?: () => void;
  onPass?: () => void;
}

/**
 * Sort tiles in traditional mahjong order
 * Order: 1m-9m, 1p-9p, 1s-9s, 1z-7z
 */
function sortTiles(tiles: string[]): string[] {
  const suitOrder: Record<string, number> = { m: 0, p: 1, s: 2, z: 3 };

  return [...tiles].sort((a, b) => {
    const suitA = a[1];
    const suitB = b[1];
    const numA = parseInt(a[0]);
    const numB = parseInt(b[0]);

    // Compare suits first
    const suitDiff = suitOrder[suitA] - suitOrder[suitB];
    if (suitDiff !== 0) return suitDiff;

    // Then compare numbers within same suit
    return numA - numB;
  });
}

export default function Hand({
  hand,
  lastDrawnTile,
  melds,
  isCurrentPlayer,
  isTenpai = false,
  size = 'normal',
  canRon = false,
  canTsumo = false,
  canPon = false,
  canChi = false,
  canKan = false,
  onDiscardTile,
  onDeclareRon,
  onDeclareTsumo,
  onDeclarePon,
  onDeclareChi,
  onDeclareKan,
  onPass,
}: HandProps) {
  // Separate main hand (13 tiles) from drawn tile
  const mainHand = useMemo(() => {
    if (!lastDrawnTile) return hand;

    // If there's a drawn tile, the main hand is all tiles except the last one
    const tiles = hand.filter(t => t !== lastDrawnTile || hand.indexOf(t) !== hand.lastIndexOf(t));
    return sortTiles(tiles.slice(0, 13));
  }, [hand, lastDrawnTile]);

  const drawnTile = lastDrawnTile || '';

  // Check if any call is available
  const hasCallAvailable = canRon || canTsumo || canPon || canChi || canKan;

  return (
    <div className="space-y-3">
      {/* Main hand (13 tiles) + Drawn tile */}
      <div className="flex items-center gap-2">
        {/* Main hand tiles */}
        <div className="flex flex-nowrap gap-1 items-center">
          {mainHand.map((tile, idx) => (
            <Tile
              key={`main-${idx}-${tile}`}
              tile={tile}
              size={size}
              clickable={isCurrentPlayer}
              onClick={() => isCurrentPlayer && onDiscardTile?.(tile, false)}
              className="bg-white"
            />
          ))}
        </div>

        {/* Separator */}
        {drawnTile && (
          <div className={`w-0.5 bg-gray-300 mx-1 ${size === 'small' ? 'h-10' : 'h-14'}`} />
        )}

        {/* Drawn tile (separate) */}
        {drawnTile && (
          <Tile
            tile={drawnTile}
            size={size}
            clickable={isCurrentPlayer}
            onClick={() => isCurrentPlayer && onDiscardTile?.(drawnTile, true)}
            highlighted={isCurrentPlayer}
            className="bg-yellow-50"
          />
        )}
      </div>

      {/* Melds (open sets) */}
      {melds.length > 0 && (
        <div className="flex gap-3 items-center">
          <span className="text-xs text-gray-500 font-medium">Melds:</span>
          <div className="flex gap-2">
            {melds.map((meld, idx) => (
              <div key={`meld-${idx}`} className="flex gap-0.5 p-1 bg-gray-50 rounded border border-gray-200">
                <span className="text-xs text-gray-600 font-medium mr-1">{meld.type.toUpperCase()}</span>
                {meld.tiles.map((tile, tileIdx) => (
                  <Tile
                    key={`meld-${idx}-tile-${tileIdx}`}
                    tile={tile}
                    size={size === 'small' ? 'small' : 'normal'}
                  />
                ))}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Action buttons (shown when calls are available) */}
      {hasCallAvailable && (
        <div className="flex gap-2 pt-2 border-t border-gray-200">
          {canRon && (
            <button
              onClick={onDeclareRon}
              className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700 font-medium transition-colors"
            >
              Ron (ロン)
            </button>
          )}

          {canTsumo && isCurrentPlayer && (
            <button
              onClick={onDeclareTsumo}
              className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700 font-medium transition-colors"
            >
              Tsumo (ツモ)
            </button>
          )}

          {canKan && (
            <button
              onClick={onDeclareKan}
              className="px-4 py-2 bg-purple-600 text-white rounded hover:bg-purple-700 font-medium transition-colors"
            >
              Kan (カン)
            </button>
          )}

          {canPon && (
            <button
              onClick={onDeclarePon}
              className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 font-medium transition-colors"
            >
              Pon (ポン)
            </button>
          )}

          {canChi && (
            <button
              onClick={onDeclareChi}
              className="px-4 py-2 bg-indigo-600 text-white rounded hover:bg-indigo-700 font-medium transition-colors"
            >
              Chi (チー)
            </button>
          )}

          {(canRon || canPon || canChi || canKan) && (
            <button
              onClick={onPass}
              className="px-4 py-2 bg-gray-400 text-white rounded hover:bg-gray-500 font-medium transition-colors"
            >
              Pass (パス)
            </button>
          )}
        </div>
      )}

      {/* Tenpai indicator */}
      {isTenpai && (
        <div className="text-xs text-orange-600 font-medium">
          ⚠️ Tenpai (聴牌)
        </div>
      )}
    </div>
  );
}
