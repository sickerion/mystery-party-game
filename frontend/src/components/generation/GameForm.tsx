import { useTranslation } from 'react-i18next';
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
  const { t } = useTranslation();

  return (
    <Card>
      <CardHeader>
        <CardTitle>{t('wizard.steps.details')}</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div>
          <Label htmlFor="theme">{t('wizard.form.theme')} *</Label>
          <Input
            id="theme"
            placeholder={t('wizard.form.themePlaceholder')}
            value={formData.theme}
            onChange={(e) => onChange({ ...formData, theme: e.target.value })}
          />
        </div>
        <div>
          <Label htmlFor="num_players">{t('wizard.form.numPlayers')}</Label>
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
          <Label htmlFor="difficulty">{t('wizard.form.difficulty')}</Label>
          <select
            id="difficulty"
            className="flex h-10 w-full rounded-md border px-3 py-2 text-sm border-gray-300 bg-white text-darkText dark:border-teal dark:bg-darkNavy dark:text-offWhite"
            value={formData.difficulty}
            onChange={(e) => onChange({ ...formData, difficulty: e.target.value as any })}
          >
            <option value="easy">{t('wizard.form.easy')}</option>
            <option value="medium">{t('wizard.form.medium')}</option>
            <option value="hard">{t('wizard.form.hard')}</option>
          </select>
        </div>
        <div>
          <Label htmlFor="special_requests">{t('wizard.form.specialRequests')}</Label>
          <Input
            id="special_requests"
            placeholder={t('wizard.form.specialRequestsPlaceholder')}
            value={formData.special_requests}
            onChange={(e) => onChange({ ...formData, special_requests: e.target.value })}
          />
        </div>
        <Button onClick={onSubmit} disabled={loading} className="w-full">
          {loading ? <Spinner size="sm" /> : t('wizard.startGeneration')}
        </Button>
      </CardContent>
    </Card>
  );
}
