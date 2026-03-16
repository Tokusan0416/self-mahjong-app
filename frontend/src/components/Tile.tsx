/**
 * Tile component - displays a single mahjong tile
 */
import { useState } from 'react';

interface TileProps {
  /** Tile code (e.g., "1m", "2p", "3s", "1z") */
  tile: string;
  /** Size variant */
  size?: 'small' | 'normal' | 'large';
  /** Whether the tile is clickable */
  clickable?: boolean;
  /** Click handler */
  onClick?: () => void;
  /** Whether to highlight the tile */
  highlighted?: boolean;
  /** Additional CSS classes */
  className?: string;
}

/**
 * Map tile code to image filename
 * Examples:
 * - "1m" -> "Man1.svg"
 * - "5p" -> "Pin5.svg"
 * - "9s" -> "Sou9.svg"
 * - "1z" -> "Ton.svg" (East)
 * - "5z" -> "Haku.svg" (White)
 */
function getTileImagePath(tile: string): string {
  if (!tile || tile.length < 2) return '';

  const number = tile[0];
  const suit = tile[1];

  // Manzu (萬子)
  if (suit === 'm') {
    return `/static/tiles/Man${number}.svg`;
  }

  // Pinzu (筒子)
  if (suit === 'p') {
    return `/static/tiles/Pin${number}.svg`;
  }

  // Souzu (索子)
  if (suit === 's') {
    return `/static/tiles/Sou${number}.svg`;
  }

  // Jihai (字牌 - honor tiles)
  if (suit === 'z') {
    const honorMap: Record<string, string> = {
      '1': 'Ton',    // 東 (East)
      '2': 'Nan',    // 南 (South)
      '3': 'Shaa',   // 西 (West)
      '4': 'Pei',    // 北 (North)
      '5': 'Haku',   // 白 (White)
      '6': 'Hatsu',  // 發 (Green)
      '7': 'Chun',   // 中 (Red)
    };
    const honorName = honorMap[number];
    return honorName ? `/static/tiles/${honorName}.svg` : '';
  }

  return '';
}

/**
 * Get display text for tile (fallback when image fails)
 */
function getTileDisplayText(tile: string): string {
  if (!tile || tile.length < 2) return '?';

  const number = tile[0];
  const suit = tile[1];

  const suitNames: Record<string, string> = {
    'm': '萬',
    'p': '筒',
    's': '索',
  };

  if (suit in suitNames) {
    return `${number}${suitNames[suit]}`;
  }

  // Honor tiles
  if (suit === 'z') {
    const honorNames: Record<string, string> = {
      '1': '東',
      '2': '南',
      '3': '西',
      '4': '北',
      '5': '白',
      '6': '發',
      '7': '中',
    };
    return honorNames[number] || '?';
  }

  return tile;
}

export default function Tile({
  tile,
  size = 'normal',
  clickable = false,
  onClick,
  highlighted = false,
  className = '',
}: TileProps) {
  const [imageError, setImageError] = useState(false);

  // Size configurations
  const sizeConfig = {
    small: { width: 30, height: 42, fontSize: 'text-xs' },
    normal: { width: 40, height: 56, fontSize: 'text-sm' },
    large: { width: 50, height: 70, fontSize: 'text-base' },
  };

  const { width, height, fontSize } = sizeConfig[size];
  const imagePath = getTileImagePath(tile);
  const displayText = getTileDisplayText(tile);

  // Base classes
  const baseClasses = `
    inline-flex items-center justify-center
    border-2 rounded shadow-sm
    transition-all duration-200
    ${highlighted ? 'border-yellow-500 ring-2 ring-yellow-300' : 'border-gray-700'}
    ${clickable ? 'cursor-pointer hover:scale-105 hover:shadow-md hover:border-blue-500' : ''}
    ${className}
  `;

  const handleClick = () => {
    if (clickable && onClick) {
      onClick();
    }
  };

  return (
    <div
      className={baseClasses}
      style={{ width: `${width}px`, height: `${height}px` }}
      onClick={handleClick}
      title={tile}
    >
      {!imageError && imagePath ? (
        <img
          src={imagePath}
          alt={tile}
          className="w-full h-full object-contain"
          onError={() => setImageError(true)}
        />
      ) : (
        // Fallback: text display
        <div className={`font-bold text-gray-900 ${fontSize}`}>
          {displayText}
        </div>
      )}
    </div>
  );
}
