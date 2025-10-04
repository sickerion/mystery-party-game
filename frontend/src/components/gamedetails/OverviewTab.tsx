import { useTranslation } from 'react-i18next';
import type { MysteryScenario } from '@/types';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';

interface OverviewTabProps {
  scenario: MysteryScenario;
}

export function OverviewTab({ scenario }: OverviewTabProps) {
  const { t } = useTranslation();

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>{t('gameDetails.overview.gameInfo')}</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          <div>
            <span className="text-gold font-semibold">{t('gameDetails.overview.theme')}: </span>
            <span className="text-offWhite dark:text-offWhite light:text-darkText">{scenario.theme}</span>
          </div>
          <div>
            <span className="text-gold font-semibold">{t('gameDetails.overview.difficulty')}: </span>
            <span className="text-offWhite dark:text-offWhite light:text-darkText">{scenario.difficulty}</span>
          </div>
          <div>
            <span className="text-gold font-semibold">{t('gameDetails.overview.players')}: </span>
            <span className="text-offWhite dark:text-offWhite light:text-darkText">{scenario.num_players}</span>
          </div>
          <div>
            <span className="text-gold font-semibold">{t('gameDetails.overview.duration')}: </span>
            <span className="text-offWhite dark:text-offWhite light:text-darkText">{scenario.estimated_duration} {t('gameDetails.overview.minutes')}</span>
          </div>
          {scenario.introduction && (
            <div className="pt-4 border-t border-teal dark:border-teal light:border-lightBorder">
              <p className="text-offWhite dark:text-offWhite light:text-darkText whitespace-pre-wrap">{scenario.introduction}</p>
            </div>
          )}
        </CardContent>
      </Card>

      {scenario.game_instructions && (
        <Card>
          <CardHeader>
            <CardTitle>{t('gameDetails.overview.instructions')}</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-offWhite dark:text-offWhite light:text-darkText whitespace-pre-wrap">{scenario.game_instructions}</p>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
