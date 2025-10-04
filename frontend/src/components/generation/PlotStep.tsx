import { useTranslation } from 'react-i18next';
import type { Plot } from '@/types';
import { Button } from '@/components/ui/button';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Spinner } from '@/components/ui/spinner';

interface PlotStepProps {
  plot: Plot | null;
  loading: boolean;
  onGenerate: () => void;
  onContinue: () => void;
}

export function PlotStep({ plot, loading, onGenerate, onContinue }: PlotStepProps) {
  const { t } = useTranslation();

  return (
    <Card>
      <CardHeader>
        <CardTitle>{t('wizard.plotStep.title')}</CardTitle>
      </CardHeader>
      <CardContent>
        {!plot ? (
          <div className="text-center py-8">
            <p className="text-gray-600 dark:text-lightGray mb-4">{t('wizard.plotStep.ready')}</p>
            <Button onClick={onGenerate} disabled={loading}>
              {loading ? <Spinner size="sm" /> : t('wizard.plotStep.generate')}
            </Button>
          </div>
        ) : (
          <div className="space-y-4">
            <div className="text-green-500 font-semibold mb-2">✓ {t('wizard.plotStep.generated')}</div>
            <div className="space-y-2 text-darkText dark:text-offWhite">
              <p><span className="text-gold">{t('wizard.plotStep.crime')}:</span> {plot.crime}</p>
              <p><span className="text-gold">{t('wizard.plotStep.victim')}:</span> {plot.victim}</p>
              <p><span className="text-gold">{t('wizard.plotStep.setting')}:</span> {plot.setting}</p>
            </div>
            <Button onClick={onContinue} disabled={loading} className="w-full">
              {loading ? <Spinner size="sm" /> : t('wizard.plotStep.continue')}
            </Button>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
