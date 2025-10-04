import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import type { Game } from '@/types';
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Spinner } from '@/components/ui/spinner';
import { getImageUrl } from '@/services/api';

interface GameCardProps {
  game: Game;
  onDelete?: (gameId: string) => void;
  isDeleting?: boolean;
}

const statusColors: Record<string, "default" | "secondary" | "destructive" | "outline"> = {
  initialized: 'outline',
  characters_generated: 'secondary',
  plot_generated: 'secondary',
  clues_generated: 'secondary',
  metadata_generated: 'secondary',
  validated: 'default',
  completed: 'default',
  failed: 'destructive',
};

export function GameCard({ game, onDelete, isDeleting = false }: GameCardProps) {
  const { t, i18n } = useTranslation();
  const getStatusLabel = (status: string) => {
    const statusKey = status.replace(/_/g, '');
    return t(`status.${status}`, status);
  };

  const getDifficultyLabel = (difficulty: string) => {
    return t(`difficulty.${difficulty}`, difficulty);
  };

  return (
    <Card>
      {/* Cover Image */}
      <div className="w-full h-48 overflow-hidden rounded-t-lg bg-gray-200 dark:bg-darkGray">
        <img
          src={getImageUrl(game.id)}
          alt={game.theme}
          className="w-full h-full object-cover"
          onError={(e) => {
            // Hide image if it fails to load (not generated yet)
            e.currentTarget.style.display = 'none';
            e.currentTarget.parentElement!.style.display = 'none';
          }}
        />
      </div>

      <CardHeader>
        <div className="flex items-start justify-between">
          <div>
            <CardTitle>{game.theme}</CardTitle>
            <CardDescription>
              {game.num_players} {t('landing.players')} • {getDifficultyLabel(game.difficulty)}
            </CardDescription>
          </div>
          <Badge variant={statusColors[game.status] || 'outline'}>
            {getStatusLabel(game.status)}
          </Badge>
        </div>
      </CardHeader>
      <CardContent>
        <div className="text-sm text-gray-600 dark:text-lightGray space-y-1">
          <p>{t('landing.created')}: {new Date(game.created_at).toLocaleDateString(i18n.language)}</p>
          {game.special_requests && (
            <p className="text-xs mt-2 text-darkText dark:text-offWhite italic">
              "{game.special_requests}"
            </p>
          )}
        </div>
      </CardContent>
      <CardFooter className="gap-2">
        <Link to={`/games/${game.id}`} className="flex-1">
          <Button variant="default" className="w-full" disabled={isDeleting}>
            {t('landing.viewDetails')}
          </Button>
        </Link>
        {onDelete && (
          <Button
            variant="destructive"
            onClick={() => onDelete(game.id)}
            disabled={isDeleting}
          >
            {isDeleting ? <Spinner size="sm" /> : t('common.delete')}
          </Button>
        )}
      </CardFooter>
    </Card>
  );
}
