import { useTranslation } from 'react-i18next';
import type { Clue } from '@/types';
import { Button } from '@/components/ui/button';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Spinner } from '@/components/ui/spinner';

interface CluesStepProps {
  clues: Clue[];
  loading: boolean;
  onGenerate: () => void;
  onContinue: () => void;
}

export function CluesStep({ clues, loading, onGenerate, onContinue }: CluesStepProps) {
  const { t } = useTranslation();

  return (
    <Card>
      <CardHeader>
        <CardTitle>{t('wizard.cluesStep.title')}</CardTitle>
      </CardHeader>
      <CardContent>
        {clues.length === 0 ? (
          <div className="text-center py-8">
            <p className="text-gray-600 dark:text-lightGray mb-4">{t('wizard.cluesStep.ready')}</p>
            <Button onClick={onGenerate} disabled={loading}>
              {loading ? <Spinner size="sm" /> : t('wizard.cluesStep.generate')}
            </Button>
          </div>
        ) : (
          <div className="space-y-4">
            <div className="text-green-500 font-semibold mb-2">✓ {clues.length} {t('wizard.cluesStep.generated')}</div>
            <Button onClick={onContinue} disabled={loading} className="w-full">
              {loading ? <Spinner size="sm" /> : t('wizard.cluesStep.continue')}
            </Button>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
