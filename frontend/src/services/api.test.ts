import { describe, it, expect, vi, beforeEach } from 'vitest';
import { createGame, getGames, getGame, deleteGame } from './api';
import type { GameRequest, Game } from '@/types';

global.fetch = vi.fn();

describe('API Service', () => {
  beforeEach(() => {
    vi.resetAllMocks();
  });

  describe('createGame', () => {
    it('creates a new game', async () => {
      const mockGame: Game = {
        id: '123',
        theme: 'Film Noir',
        num_players: 6,
        difficulty: 'medium',
        special_requests: null,
        status: 'initialized',
        created_at: '2025-01-01T12:00:00Z',
        updated_at: '2025-01-01T12:00:00Z',
      };

      (global.fetch as any).mockResolvedValueOnce({
        ok: true,
        json: async () => mockGame,
      });

      const request: GameRequest = {
        theme: 'Film Noir',
        num_players: 6,
        difficulty: 'medium',
        special_requests: null,
      };

      const result = await createGame(request);
      expect(result).toEqual(mockGame);
      expect(global.fetch).toHaveBeenCalledWith(
        'http://localhost:8000/games',
        expect.objectContaining({
          method: 'POST',
          body: JSON.stringify(request),
        })
      );
    });

    it('throws error on failed request', async () => {
      (global.fetch as any).mockResolvedValueOnce({
        ok: false,
        status: 400,
        json: async () => ({ detail: 'Invalid request' }),
      });

      await expect(
        createGame({ theme: '', num_players: 6, difficulty: 'medium', special_requests: null })
      ).rejects.toThrow('Invalid request');
    });
  });

  describe('getGames', () => {
    it('fetches list of games', async () => {
      const mockGames: Game[] = [
        {
          id: '123',
          theme: 'Film Noir',
          num_players: 6,
          difficulty: 'medium',
          special_requests: null,
          status: 'completed',
          created_at: '2025-01-01T12:00:00Z',
          updated_at: '2025-01-01T13:00:00Z',
        },
      ];

      (global.fetch as any).mockResolvedValueOnce({
        ok: true,
        json: async () => mockGames,
      });

      const result = await getGames();
      expect(result).toEqual(mockGames);
    });
  });

  describe('getGame', () => {
    it('fetches a single game', async () => {
      const mockScenario = {
        title: 'Murder at Midnight',
        theme: 'Film Noir',
        difficulty: 'medium',
        num_players: 6,
        estimated_duration: 120,
        characters: [],
        plot: {} as any,
        clues: [],
        game_instructions: 'Test',
        introduction: 'Test intro',
      };

      (global.fetch as any).mockResolvedValueOnce({
        ok: true,
        json: async () => mockScenario,
      });

      const result = await getGame('123');
      expect(result).toEqual(mockScenario);
    });
  });

  describe('deleteGame', () => {
    it('deletes a game', async () => {
      (global.fetch as any).mockResolvedValueOnce({
        ok: true,
        json: async () => ({}),
      });

      await deleteGame('123');
      expect(global.fetch).toHaveBeenCalledWith(
        'http://localhost:8000/games/123',
        expect.objectContaining({ method: 'DELETE' })
      );
    });
  });
});
