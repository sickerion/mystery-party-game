import { useTranslation } from 'react-i18next';
import type { Plot } from '@/types';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';

interface PlotTabProps {
  plot: Plot;
}

export function PlotTab({ plot }: PlotTabProps) {
  const { t } = useTranslation();

  return (
    <Card>
      <CardHeader>
        <CardTitle>{t('gameDetails.plot.title')}</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div>
          <p className="text-gold font-semibold">{t('gameDetails.plot.setting')}</p>
          <p className="text-darkText dark:text-offWhite">{plot.setting}</p>
        </div>
        <div>
          <p className="text-gold font-semibold">{t('gameDetails.plot.crime')}</p>
          <p className="text-darkText dark:text-offWhite">{plot.crime}</p>
        </div>
        <div>
          <p className="text-gold font-semibold">{t('gameDetails.plot.victim')}</p>
          <p className="text-darkText dark:text-offWhite">{plot.victim}</p>
        </div>
        <div>
          <p className="text-gold font-semibold">{t('gameDetails.plot.culprit')}</p>
          <p className="text-crimson">{plot.culprit}</p>
        </div>
        <div>
          <p className="text-gold font-semibold">{t('gameDetails.plot.method')}</p>
          <p className="text-darkText dark:text-offWhite">{plot.murder_method}</p>
        </div>
        <div>
          <p className="text-gold font-semibold">{t('gameDetails.plot.timeline')}</p>
          <ul className="list-disc pl-5 space-y-1 text-darkText dark:text-offWhite">
            {plot.timeline.map((event, i) => (
              <li key={i}>{event}</li>
            ))}
          </ul>
        </div>
        <div>
          <p className="text-gold font-semibold">{t('gameDetails.plot.resolution')}</p>
          <p className="text-darkText dark:text-offWhite">{plot.resolution}</p>
        </div>
      </CardContent>
    </Card>
  );
}
