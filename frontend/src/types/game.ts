/**
 * TypeScript type definitions for Mahjong game state
 */

export interface Meld {
  type: string; // "pon", "chi", "kan"
  tiles: string[];
  from_player: number | null;
}

export interface Player {
  hand: string[];
  discards: string[];
  melds: Meld[];
  score: number;
  is_riichi: boolean;
  last_drawn_tile: string;
  riichi_turn: number;
}

export interface GameState {
  players: Player[];
  player_names: string[];
  current_player: number;
  wall_remaining: number;
  dora_indicators: string[];
  round_wind: number;
  round_number: number;
  honba_sticks: number;
  riichi_sticks: number;
  game_type: string;
  dealer: number;
  turn_count: number;
  is_game_over: boolean;
  is_exhaustive_draw: boolean;
  last_discard: string | null;
  last_discard_player: number;
  // Call availability
  can_ron: boolean[];
  can_pon: boolean[];
  can_chi: boolean[];
  can_kan: boolean[];
  can_tsumo: boolean;
}

export interface WinInfo {
  winner_idx: number;
  loser_idx?: number;
  yaku_list: Array<{ name: string; han: number }>;
  han: number;
  fu: number;
  points: number;
  is_dealer: boolean;
  is_tsumo: boolean;
}

export interface ExhaustiveDrawInfo {
  tenpai_players: number[];
  noten_players: number[];
  point_changes: number[];
}

export interface GameEndInfo {
  final_scores: number[];
  rankings: number[];
}

export type GameType = 'hanchan' | 'tonpuu';

export interface ApiResponse<T = unknown> {
  success: boolean;
  error?: string;
  data?: T;
}

export interface NewGameResponse {
  success: boolean;
  game_state: GameState;
}

export interface DiscardResponse {
  success: boolean;
  game_state: GameState;
}

export interface WinResponse {
  success: boolean;
  game_state: GameState;
  win_info: WinInfo;
}

export interface TenpaiCheckResponse {
  is_tenpai: boolean;
  waiting_tiles: string[];
}
