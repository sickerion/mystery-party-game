import { useTranslation } from 'react-i18next';
import type { Clue } from '@/types';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';

interface CluesTabProps {
  clues: Clue[];
}

export function CluesTab({ clues }: CluesTabProps) {
  const { t } = useTranslation();

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      {clues.map((clue, i) => (
        <Card key={i}>
          <CardHeader>
            <div className="flex items-start justify-between">
              <CardTitle className="text-lg">{t('gameDetails.clues.title')} #{clue.clue_id}</CardTitle>
              {clue.misleading && (
                <Badge variant="destructive">{t('gameDetails.clues.redHerring')}</Badge>
              )}
            </div>
          </CardHeader>
          <CardContent className="space-y-2">
            <p className="text-darkText dark:text-offWhite">{clue.description}</p>
            <div className="text-sm space-y-1 text-darkText dark:text-offWhite">
              <p><span className="text-gold">{t('gameDetails.clues.location')}:</span> {clue.location}</p>
              <p><span className="text-gold">{t('gameDetails.clues.revealedBy')}:</span> {clue.revealed_by}</p>
              <p><span className="text-gold">{t('gameDetails.clues.significance')}:</span> {clue.significance}</p>
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}
