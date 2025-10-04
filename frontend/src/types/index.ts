// Game Status
export type GameStatus =
  | 'initialized'
  | 'characters_generated'
  | 'plot_generated'
  | 'clues_generated'
  | 'metadata_generated'
  | 'validated'
  | 'completed'
  | 'failed';

// Difficulty
export type Difficulty = 'easy' | 'medium' | 'hard';

// Game Request
export interface GameRequest {
  theme: string;
  num_players: number;
  difficulty: Difficulty;
  special_requests?: string;
  language?: string;
}

// Game
export interface Game {
  id: string;
  theme: string;
  num_players: number;
  difficulty: Difficulty;
  special_requests?: string;
  language: string;
  status: GameStatus;
  created_at: string;
  updated_at: string;
}

// Character
export interface Character {
  id?: number;
  name: string;
  role: string;
  background: string;
  personality: string;
  secret: string;
  motive?: string;
  relationship_to_victim?: string;
}

// Plot
export interface Plot {
  setting: string;
  victim: string;
  crime: string;
  culprit: string;
  murder_method: string;
  timeline: string[];
  resolution: string;
}

// Clue
export interface Clue {
  clue_id: string;
  description: string;
  location: string;
  revealed_by: string;
  significance: string;
  misleading: boolean;
}

// Metadata
export interface Metadata {
  title: string;
  estimated_duration: string;
  game_instructions: string;
  introduction: string;
  audio_introduction_url?: string;
  audio_instructions_url?: string;
}

// Validation Result
export interface ValidationResult {
  id?: string;
  game_id: string;
  iteration: number;
  validation_passed: boolean;
  validation_errors: string[];
  created_at?: string;
}

// Mystery Scenario (complete) - matches backend MysteryScenario model
export interface MysteryScenario {
  title: string;
  theme: string;
  difficulty: Difficulty;
  num_players: number;
  estimated_duration: number; // in minutes
  plot: Plot;
  characters: Character[];
  clues: Clue[];
  game_instructions: string;
  introduction: string;
}

// Generation Step
export type GenerationStep =
  | 'initial'
  | 'characters'
  | 'plot'
  | 'clues'
  | 'metadata'
  | 'validation';

// Email Assignment
export interface EmailAssignment {
  character_name: string;
  email: string;
}
