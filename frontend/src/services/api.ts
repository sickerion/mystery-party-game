import type {
  Game,
  GameRequest,
  Character,
  Plot,
  Clue,
  Metadata,
  ValidationResult,
  MysteryScenario,
} from '../types';
import i18n from '../i18n/config';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message);
    this.name = 'ApiError';
  }
}

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
    throw new ApiError(response.status, error.detail || 'Request failed');
  }
  return response.json();
}

// Games
export async function createGame(request: GameRequest): Promise<Game> {
  // Add current language to the request
  const requestWithLanguage = {
    ...request,
    language: i18n.language || 'en',
  };

  const response = await fetch(`${API_BASE_URL}/games`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(requestWithLanguage),
  });
  return handleResponse<Game>(response);
}

export async function getGames(params?: {
  status?: string;
  limit?: number;
  offset?: number;
}): Promise<Game[]> {
  const queryParams = new URLSearchParams();
  if (params?.status) queryParams.append('status', params.status);
  if (params?.limit) queryParams.append('limit', params.limit.toString());
  if (params?.offset) queryParams.append('offset', params.offset.toString());

  const url = `${API_BASE_URL}/games${queryParams.toString() ? `?${queryParams}` : ''}`;
  const response = await fetch(url);
  return handleResponse<Game[]>(response);
}

export async function getGame(gameId: string): Promise<MysteryScenario> {
  const response = await fetch(`${API_BASE_URL}/games/${gameId}`);
  return handleResponse<MysteryScenario>(response);
}

export async function deleteGame(gameId: string): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/games/${gameId}`, {
    method: 'DELETE',
  });
  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Failed to delete game' }));
    throw new ApiError(response.status, error.detail);
  }
}

// Generation endpoints
export async function generateCharacters(gameId: string): Promise<Character[]> {
  const response = await fetch(`${API_BASE_URL}/games/${gameId}/characters`, {
    method: 'POST',
  });
  return handleResponse<Character[]>(response);
}

export async function generatePlot(gameId: string): Promise<Plot> {
  const response = await fetch(`${API_BASE_URL}/games/${gameId}/plot`, {
    method: 'POST',
  });
  return handleResponse<Plot>(response);
}

export async function generateClues(gameId: string): Promise<Clue[]> {
  const response = await fetch(`${API_BASE_URL}/games/${gameId}/clues`, {
    method: 'POST',
  });
  return handleResponse<Clue[]>(response);
}

export async function generateMetadata(gameId: string): Promise<Metadata> {
  const response = await fetch(`${API_BASE_URL}/games/${gameId}/metadata`, {
    method: 'POST',
  });
  return handleResponse<Metadata>(response);
}

export async function validateScenario(gameId: string): Promise<ValidationResult> {
  const response = await fetch(`${API_BASE_URL}/games/${gameId}/validate`, {
    method: 'POST',
  });
  return handleResponse<ValidationResult>(response);
}

// Audio generation
export async function generateAudio(gameId: string): Promise<{ audio_introduction_url: string; audio_instructions_url: string; message: string }> {
  const response = await fetch(`${API_BASE_URL}/games/${gameId}/metadata/audio`, {
    method: 'POST',
  });
  return handleResponse(response);
}

export function getAudioUrl(gameId: string, audioType: 'introduction' | 'instructions'): string {
  return `${API_BASE_URL}/games/${gameId}/audio/${audioType}`;
}

export { ApiError };
