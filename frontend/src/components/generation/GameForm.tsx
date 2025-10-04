import type { GameRequest } from '@/types';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Spinner } from '@/components/ui/spinner';

interface GameFormProps {
  formData: GameRequest;
  loading: boolean;
  onChange: (data: GameRequest) => void;
  onSubmit: () => void;
}

export function GameForm({ formData, loading, onChange, onSubmit }: GameFormProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Game Details</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div>
          <Label htmlFor="theme">Theme *</Label>
          <Input
            id="theme"
            placeholder="e.g., Film Noir, Victorian Era, Sci-Fi Space Station"
            value={formData.theme}
            onChange={(e) => onChange({ ...formData, theme: e.target.value })}
          />
        </div>
        <div>
          <Label htmlFor="num_players">Number of Players</Label>
          <Input
            id="num_players"
            type="number"
            min="4"
            max="12"
            value={formData.num_players}
            onChange={(e) => onChange({ ...formData, num_players: parseInt(e.target.value) })}
          />
        </div>
        <div>
          <Label htmlFor="difficulty">Difficulty</Label>
          <select
            id="difficulty"
            className="flex h-10 w-full rounded-md border border-teal bg-darkNavy px-3 py-2 text-sm text-offWhite"
            value={formData.difficulty}
            onChange={(e) => onChange({ ...formData, difficulty: e.target.value as any })}
          >
            <option value="easy">Easy</option>
            <option value="medium">Medium</option>
            <option value="hard">Hard</option>
          </select>
        </div>
        <div>
          <Label htmlFor="special_requests">Special Requests (Optional)</Label>
          <Input
            id="special_requests"
            placeholder="Any specific requirements or preferences"
            value={formData.special_requests}
            onChange={(e) => onChange({ ...formData, special_requests: e.target.value })}
          />
        </div>
        <Button onClick={onSubmit} disabled={loading} className="w-full">
          {loading ? <Spinner size="sm" /> : 'Start Generation'}
        </Button>
      </CardContent>
    </Card>
  );
}
