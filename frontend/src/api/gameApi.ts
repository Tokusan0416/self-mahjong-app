/**
 * API client for game actions
 */
import axios from 'axios';
import {
  GameState,
  GameType,
  NewGameResponse,
  DiscardResponse,
  WinResponse,
  TenpaiCheckResponse,
} from '../types/game';

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
});

export const gameApi = {
  /**
   * Start a new game
   */
  startNewGame: async (gameType: GameType): Promise<NewGameResponse> => {
    const response = await api.post<NewGameResponse>('/game/new', {
      game_type: gameType,
    });
    return response.data;
  },

  /**
   * Get current game state
   */
  getGameState: async (): Promise<{ game_state: GameState | null }> => {
    const response = await api.get<{ game_state: GameState | null }>('/game/state');
    return response.data;
  },

  /**
   * Discard a tile
   */
  discardTile: async (
    playerIdx: number,
    tile: string,
    isDrawn: boolean
  ): Promise<DiscardResponse> => {
    const response = await api.post<DiscardResponse>('/game/discard', {
      player_idx: playerIdx,
      tile,
      is_drawn: isDrawn,
    });
    return response.data;
  },

  /**
   * Declare riichi
   */
  declareRiichi: async (playerIdx: number): Promise<DiscardResponse> => {
    const response = await api.post<DiscardResponse>('/game/riichi', {
      player_idx: playerIdx,
    });
    return response.data;
  },

  /**
   * Declare tsumo win
   */
  declareTsumo: async (playerIdx: number): Promise<WinResponse> => {
    const response = await api.post<WinResponse>('/game/tsumo', {
      player_idx: playerIdx,
    });
    return response.data;
  },

  /**
   * Declare ron win
   */
  declareRon: async (playerIdx: number): Promise<WinResponse> => {
    const response = await api.post<WinResponse>('/game/ron', {
      player_idx: playerIdx,
    });
    return response.data;
  },

  /**
   * Declare pon
   */
  declarePon: async (playerIdx: number, tile: string): Promise<DiscardResponse> => {
    const response = await api.post<DiscardResponse>('/game/pon', {
      player_idx: playerIdx,
      tile,
    });
    return response.data;
  },

  /**
   * Declare chi
   */
  declareChi: async (
    playerIdx: number,
    tile: string,
    pattern: string[]
  ): Promise<DiscardResponse> => {
    const response = await api.post<DiscardResponse>('/game/chi', {
      player_idx: playerIdx,
      tile,
      pattern,
    });
    return response.data;
  },

  /**
   * Declare kan
   */
  declareKan: async (playerIdx: number, tile: string): Promise<DiscardResponse> => {
    const response = await api.post<DiscardResponse>('/game/kan', {
      player_idx: playerIdx,
      tile,
    });
    return response.data;
  },

  /**
   * Pass on all calls
   */
  passOnCalls: async (): Promise<DiscardResponse> => {
    const response = await api.post<DiscardResponse>('/game/pass');
    return response.data;
  },

  /**
   * Check tenpai status for player
   */
  checkTenpai: async (playerIdx: number): Promise<TenpaiCheckResponse> => {
    const response = await api.get<TenpaiCheckResponse>(`/game/tenpai/${playerIdx}`);
    return response.data;
  },

  /**
   * Continue after exhaustive draw
   */
  continueAfterDraw: async (): Promise<DiscardResponse> => {
    const response = await api.post<DiscardResponse>('/game/continue');
    return response.data;
  },
};
