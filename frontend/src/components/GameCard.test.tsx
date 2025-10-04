import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { BrowserRouter } from 'react-router-dom';
import { GameCard } from './GameCard';
import type { Game } from '@/types';

const mockGame: Game = {
  id: '123',
  theme: 'Film Noir',
  num_players: 6,
  difficulty: 'medium',
  special_requests: null,
  status: 'completed',
  created_at: '2025-01-01T12:00:00Z',
  updated_at: '2025-01-01T13:00:00Z',
};

describe('GameCard', () => {
  it('renders game information', () => {
    render(
      <BrowserRouter>
        <GameCard game={mockGame} />
      </BrowserRouter>
    );

    expect(screen.getByText('Film Noir')).toBeInTheDocument();
    expect(screen.getByText(/6/)).toBeInTheDocument();
    expect(screen.getByText(/medium/)).toBeInTheDocument();
  });

  it('calls onDelete when delete button clicked', async () => {
    const handleDelete = vi.fn();
    render(
      <BrowserRouter>
        <GameCard game={mockGame} onDelete={handleDelete} />
      </BrowserRouter>
    );

    await userEvent.click(screen.getByText('Delete'));
    expect(handleDelete).toHaveBeenCalledWith('123');
  });

  it('shows spinner when deleting', () => {
    render(
      <BrowserRouter>
        <GameCard game={mockGame} onDelete={vi.fn()} isDeleting />
      </BrowserRouter>
    );

    expect(screen.getByTestId('spinner')).toBeInTheDocument();
  });

  it('disables buttons when deleting', () => {
    render(
      <BrowserRouter>
        <GameCard game={mockGame} onDelete={vi.fn()} isDeleting />
      </BrowserRouter>
    );

    const buttons = screen.getAllByRole('button');
    buttons.forEach(button => expect(button).toBeDisabled());
  });
});
