import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { getGames, deleteGame } from '@/services/api';
import type { Game } from '@/types';
import { Button } from '@/components/ui/button';
import { GameCard } from '@/components/GameCard';
import { Spinner } from '@/components/ui/spinner';

export function Landing() {
  const { t } = useTranslation();
  const [games, setGames] = useState<Game[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [deletingId, setDeletingId] = useState<string | null>(null);
  const navigate = useNavigate();

  const loadGames = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await getGames();
      setGames(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load games');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadGames();
  }, []);

  const handleDelete = async (gameId: string) => {
    if (!confirm(t('landing.deleteConfirm'))) return;

    try {
      setDeletingId(gameId);
      await deleteGame(gameId);
      setGames(games.filter(g => g.id !== gameId));
    } catch (err) {
      alert(err instanceof Error ? err.message : t('common.error'));
    } finally {
      setDeletingId(null);
    }
  };

  return (
    <div>
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-4xl font-bold text-gold mb-2">{t('landing.title')}</h1>
          <p className="text-lightGray dark:text-lightGray light:text-gray-600">
            {t('header.subtitle')}
          </p>
        </div>
        <Button
          size="lg"
          onClick={() => navigate('/games/new')}
        >
          {t('landing.createNew')}
        </Button>
      </div>

      {loading && (
        <div className="flex justify-center items-center py-12">
          <Spinner size="lg" />
        </div>
      )}

      {error && (
        <div className="bg-crimson/10 border border-crimson text-crimson px-4 py-3 rounded">
          {error}
        </div>
      )}

      {!loading && !error && games.length === 0 && (
        <div className="text-center py-12">
          <div className="text-6xl mb-4">🕵️</div>
          <h2 className="text-2xl font-semibold text-offWhite dark:text-offWhite light:text-darkText mb-2">
            {t('landing.noGames')}
          </h2>
          <p className="text-lightGray dark:text-lightGray light:text-gray-600 mb-6">
            {t('landing.noGames')}
          </p>
          <Button onClick={() => navigate('/games/new')}>
            {t('landing.createNew')}
          </Button>
        </div>
      )}

      {!loading && !error && games.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {games.map((game) => (
            <GameCard
              key={game.id}
              game={game}
              onDelete={handleDelete}
              isDeleting={deletingId === game.id}
            />
          ))}
        </div>
      )}
    </div>
  );
}
