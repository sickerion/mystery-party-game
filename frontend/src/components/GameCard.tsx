import { Link } from 'react-router-dom';
import type { Game } from '@/types';
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Spinner } from '@/components/ui/spinner';

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

const statusLabels: Record<string, string> = {
  initialized: 'Initialized',
  characters_generated: 'Characters Ready',
  plot_generated: 'Plot Ready',
  clues_generated: 'Clues Ready',
  metadata_generated: 'Metadata Ready',
  validated: 'Validated',
  completed: 'Completed',
  failed: 'Failed',
};

export function GameCard({ game, onDelete, isDeleting = false }: GameCardProps) {
  return (
    <Card>
      <CardHeader>
        <div className="flex items-start justify-between">
          <div>
            <CardTitle>{game.theme}</CardTitle>
            <CardDescription>
              {game.num_players} players • {game.difficulty}
            </CardDescription>
          </div>
          <Badge variant={statusColors[game.status] || 'outline'}>
            {statusLabels[game.status] || game.status}
          </Badge>
        </div>
      </CardHeader>
      <CardContent>
        <div className="text-sm text-lightGray space-y-1">
          <p>Created: {new Date(game.created_at).toLocaleDateString()}</p>
          {game.special_requests && (
            <p className="text-xs mt-2 text-offWhite italic">
              "{game.special_requests}"
            </p>
          )}
        </div>
      </CardContent>
      <CardFooter className="gap-2">
        <Link to={`/games/${game.id}`} className="flex-1">
          <Button variant="default" className="w-full" disabled={isDeleting}>
            View Details
          </Button>
        </Link>
        {onDelete && (
          <Button
            variant="destructive"
            onClick={() => onDelete(game.id)}
            disabled={isDeleting}
          >
            {isDeleting ? <Spinner size="sm" /> : 'Delete'}
          </Button>
        )}
      </CardFooter>
    </Card>
  );
}
