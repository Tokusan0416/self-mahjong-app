/**
 * MahjongTable component - displays the mahjong table with 4 players in cross layout
 */
import Hand from './Hand';
import Tile from './Tile';
import { GameState } from '../types/game';

interface MahjongTableProps {
  gameState: GameState;
  onDiscardTile: (playerIdx: number, tile: string, isDrawn: boolean) => void;
  onDeclareRon: (playerIdx: number) => void;
  onDeclareTsumo: (playerIdx: number) => void;
  onDeclarePon: (playerIdx: number) => void;
  onDeclareChi: (playerIdx: number) => void;
  onDeclareKan: (playerIdx: number) => void;
  onPass: (playerIdx: number) => void;
}

/**
 * Get wind name in Japanese
 */
function getWindName(windIndex: number): string {
  const winds = ['東', '南', '西', '北'];
  return winds[windIndex] || '?';
}

/**
 * Get player's seat wind (relative to dealer)
 */
function getPlayerWind(playerIdx: number, dealer: number): string {
  const relativePosition = (playerIdx - dealer + 4) % 4;
  return getWindName(relativePosition);
}

/**
 * Player info component
 */
interface PlayerInfoProps {
  name: string;
  score: number;
  wind: string;
  isDealer: boolean;
  isCurrentPlayer: boolean;
  isRiichi: boolean;
  position: 'top' | 'right' | 'bottom' | 'left';
}

function PlayerInfo({ name, score, wind, isDealer, isCurrentPlayer, isRiichi, position }: PlayerInfoProps) {
  // Position-specific styling
  const positionClasses = {
    top: 'flex-col items-center',
    right: 'flex-row items-center',
    bottom: 'flex-col items-center',
    left: 'flex-row-reverse items-center',
  };

  return (
    <div className={`flex gap-2 ${positionClasses[position]}`}>
      <div className={`
        px-3 py-2 rounded-lg font-medium text-sm
        ${isCurrentPlayer ? 'bg-blue-500 text-white ring-2 ring-blue-300' : 'bg-white text-gray-800 border border-gray-300'}
      `}>
        <div className="flex items-center gap-2">
          <span className="text-lg font-bold">{wind}</span>
          <span>{name}</span>
          {isDealer && (
            <span className="text-xs bg-yellow-400 text-yellow-900 px-1.5 py-0.5 rounded">親</span>
          )}
          {isRiichi && (
            <span className="text-xs bg-red-500 text-white px-1.5 py-0.5 rounded">リーチ</span>
          )}
        </div>
        <div className="text-xs mt-1 opacity-90">
          {score.toLocaleString()}点
        </div>
      </div>
    </div>
  );
}

/**
 * Discard area component
 */
interface DiscardAreaProps {
  discards: string[];
  playerName: string;
  position: 'top' | 'right' | 'bottom' | 'left';
}

function DiscardArea({ discards, playerName, position }: DiscardAreaProps) {
  if (discards.length === 0) return null;

  // Layout based on position
  const layoutClasses = {
    top: 'flex-wrap justify-center',
    right: 'flex-col flex-wrap max-h-32',
    bottom: 'flex-wrap justify-center',
    left: 'flex-col flex-wrap max-h-32',
  };

  return (
    <div className={`flex gap-0.5 ${layoutClasses[position]}`}>
      {discards.map((tile, idx) => (
        <Tile
          key={`${playerName}-discard-${idx}-${tile}`}
          tile={tile}
          size="small"
        />
      ))}
    </div>
  );
}

export default function MahjongTable({
  gameState,
  onDiscardTile,
  onDeclareRon,
  onDeclareTsumo,
  onDeclarePon,
  onDeclareChi,
  onDeclareKan,
  onPass,
}: MahjongTableProps) {
  const { players, player_names, current_player, dealer } = gameState;

  // For simplicity, assume player 0 is always at the bottom (self)
  // In a real game, you'd want to rotate based on user's seat
  const bottomPlayer = 0;
  const rightPlayer = 1;
  const topPlayer = 2;
  const leftPlayer = 3;

  return (
    <div className="bg-gradient-to-br from-green-800 to-green-900 rounded-xl shadow-2xl p-8 max-w-[1100px] mx-auto">
      {/* Container with cross layout */}
      <div className="grid grid-cols-[auto_minmax(600px,1fr)_auto] grid-rows-[auto_1fr_auto] gap-4 min-h-[700px] justify-items-center items-center">
        {/* Top Player - Row 1, Col 2 */}
        <div className="col-start-2 flex flex-col items-center gap-3">
          <PlayerInfo
            name={player_names[topPlayer]}
            score={players[topPlayer].score}
            wind={getPlayerWind(topPlayer, dealer)}
            isDealer={topPlayer === dealer}
            isCurrentPlayer={topPlayer === current_player}
            isRiichi={players[topPlayer].is_riichi}
            position="top"
          />
          <div className="transform rotate-180">
            <Hand
              hand={players[topPlayer].hand}
              lastDrawnTile={players[topPlayer].last_drawn_tile}
              melds={players[topPlayer].melds}
              isCurrentPlayer={topPlayer === current_player}
              isTenpai={false}
              size="normal"
              canRon={gameState.can_ron[topPlayer]}
              canTsumo={gameState.can_tsumo && topPlayer === current_player}
              canPon={gameState.can_pon[topPlayer]}
              canChi={gameState.can_chi[topPlayer]}
              canKan={gameState.can_kan[topPlayer]}
              onDiscardTile={(tile, isDrawn) => onDiscardTile(topPlayer, tile, isDrawn)}
              onDeclareRon={() => onDeclareRon(topPlayer)}
              onDeclareTsumo={() => onDeclareTsumo(topPlayer)}
              onDeclarePon={() => onDeclarePon(topPlayer)}
              onDeclareChi={() => onDeclareChi(topPlayer)}
              onDeclareKan={() => onDeclareKan(topPlayer)}
              onPass={() => onPass(topPlayer)}
            />
          </div>
        </div>

        {/* Left Player - Row 2, Col 1 */}
        <div className="row-start-2 flex flex-row items-center gap-3">
          <PlayerInfo
            name={player_names[leftPlayer]}
            score={players[leftPlayer].score}
            wind={getPlayerWind(leftPlayer, dealer)}
            isDealer={leftPlayer === dealer}
            isCurrentPlayer={leftPlayer === current_player}
            isRiichi={players[leftPlayer].is_riichi}
            position="left"
          />
          <div className="transform rotate-90" style={{ transformOrigin: 'center center' }}>
            <Hand
              hand={players[leftPlayer].hand}
              lastDrawnTile={players[leftPlayer].last_drawn_tile}
              melds={players[leftPlayer].melds}
              isCurrentPlayer={leftPlayer === current_player}
              isTenpai={false}
              size="small"
              canRon={gameState.can_ron[leftPlayer]}
              canTsumo={gameState.can_tsumo && leftPlayer === current_player}
              canPon={gameState.can_pon[leftPlayer]}
              canChi={gameState.can_chi[leftPlayer]}
              canKan={gameState.can_kan[leftPlayer]}
              onDiscardTile={(tile, isDrawn) => onDiscardTile(leftPlayer, tile, isDrawn)}
              onDeclareRon={() => onDeclareRon(leftPlayer)}
              onDeclareTsumo={() => onDeclareTsumo(leftPlayer)}
              onDeclarePon={() => onDeclarePon(leftPlayer)}
              onDeclareChi={() => onDeclareChi(leftPlayer)}
              onDeclareKan={() => onDeclareKan(leftPlayer)}
              onPass={() => onPass(leftPlayer)}
            />
          </div>
        </div>

        {/* Center - Discard area - Row 2, Col 2 */}
        <div className="row-start-2 col-start-2 bg-green-700 rounded-lg p-4 flex items-center justify-center">
          <div className="grid grid-cols-3 grid-rows-3 gap-4 w-full h-full">
            {/* Top discards */}
            <div className="col-start-2 row-start-1 flex justify-center items-start">
              <DiscardArea
                discards={players[topPlayer].discards}
                playerName={player_names[topPlayer]}
                position="top"
              />
            </div>

            {/* Right discards */}
            <div className="col-start-3 row-start-2 flex justify-end items-center">
              <DiscardArea
                discards={players[rightPlayer].discards}
                playerName={player_names[rightPlayer]}
                position="right"
              />
            </div>

            {/* Bottom discards */}
            <div className="col-start-2 row-start-3 flex justify-center items-end">
              <DiscardArea
                discards={players[bottomPlayer].discards}
                playerName={player_names[bottomPlayer]}
                position="bottom"
              />
            </div>

            {/* Left discards */}
            <div className="col-start-1 row-start-2 flex justify-start items-center">
              <DiscardArea
                discards={players[leftPlayer].discards}
                playerName={player_names[leftPlayer]}
                position="left"
              />
            </div>

            {/* Center - Game info */}
            <div className="col-start-2 row-start-2 flex items-center justify-center">
              <div className="text-center text-white bg-green-800 bg-opacity-50 rounded-lg px-4 py-2">
                <div className="text-xs opacity-75">Turn</div>
                <div className="text-2xl font-bold">{gameState.turn_count}</div>
              </div>
            </div>
          </div>
        </div>

        {/* Right Player - Row 2, Col 3 */}
        <div className="row-start-2 col-start-3 flex flex-row items-center gap-3">
          <div className="transform -rotate-90" style={{ transformOrigin: 'center center' }}>
            <Hand
              hand={players[rightPlayer].hand}
              lastDrawnTile={players[rightPlayer].last_drawn_tile}
              melds={players[rightPlayer].melds}
              isCurrentPlayer={rightPlayer === current_player}
              isTenpai={false}
              size="small"
              canRon={gameState.can_ron[rightPlayer]}
              canTsumo={gameState.can_tsumo && rightPlayer === current_player}
              canPon={gameState.can_pon[rightPlayer]}
              canChi={gameState.can_chi[rightPlayer]}
              canKan={gameState.can_kan[rightPlayer]}
              onDiscardTile={(tile, isDrawn) => onDiscardTile(rightPlayer, tile, isDrawn)}
              onDeclareRon={() => onDeclareRon(rightPlayer)}
              onDeclareTsumo={() => onDeclareTsumo(rightPlayer)}
              onDeclarePon={() => onDeclarePon(rightPlayer)}
              onDeclareChi={() => onDeclareChi(rightPlayer)}
              onDeclareKan={() => onDeclareKan(rightPlayer)}
              onPass={() => onPass(rightPlayer)}
            />
          </div>
          <PlayerInfo
            name={player_names[rightPlayer]}
            score={players[rightPlayer].score}
            wind={getPlayerWind(rightPlayer, dealer)}
            isDealer={rightPlayer === dealer}
            isCurrentPlayer={rightPlayer === current_player}
            isRiichi={players[rightPlayer].is_riichi}
            position="right"
          />
        </div>

        {/* Bottom Player (Self) - Row 3, Col 2 */}
        <div className="row-start-3 col-start-2 flex flex-col items-center gap-3">
          <Hand
            hand={players[bottomPlayer].hand}
            lastDrawnTile={players[bottomPlayer].last_drawn_tile}
            melds={players[bottomPlayer].melds}
            isCurrentPlayer={bottomPlayer === current_player}
            isTenpai={false}
            size="normal"
            canRon={gameState.can_ron[bottomPlayer]}
            canTsumo={gameState.can_tsumo && bottomPlayer === current_player}
            canPon={gameState.can_pon[bottomPlayer]}
            canChi={gameState.can_chi[bottomPlayer]}
            canKan={gameState.can_kan[bottomPlayer]}
            onDiscardTile={(tile, isDrawn) => onDiscardTile(bottomPlayer, tile, isDrawn)}
            onDeclareRon={() => onDeclareRon(bottomPlayer)}
            onDeclareTsumo={() => onDeclareTsumo(bottomPlayer)}
            onDeclarePon={() => onDeclarePon(bottomPlayer)}
            onDeclareChi={() => onDeclareChi(bottomPlayer)}
            onDeclareKan={() => onDeclareKan(bottomPlayer)}
            onPass={() => onPass(bottomPlayer)}
          />
          <PlayerInfo
            name={player_names[bottomPlayer]}
            score={players[bottomPlayer].score}
            wind={getPlayerWind(bottomPlayer, dealer)}
            isDealer={bottomPlayer === dealer}
            isCurrentPlayer={bottomPlayer === current_player}
            isRiichi={players[bottomPlayer].is_riichi}
            position="bottom"
          />
        </div>
      </div>
    </div>
  );
}
