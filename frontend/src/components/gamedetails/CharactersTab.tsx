import { useTranslation } from 'react-i18next';
import type { Character } from '@/types';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';

interface CharactersTabProps {
  characters: Character[];
}

export function CharactersTab({ characters }: CharactersTabProps) {
  const { t } = useTranslation();

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      {characters.map((char, i) => (
        <Card key={i}>
          <CardHeader>
            <CardTitle>{char.name}</CardTitle>
            <p className="text-sm text-gray-600 dark:text-lightGray">{char.role}</p>
          </CardHeader>
          <CardContent className="space-y-3">
            <div>
              <p className="text-gold font-semibold text-sm">{t('gameDetails.characters.background')}</p>
              <p className="text-darkText dark:text-offWhite text-sm">{char.background}</p>
            </div>
            <div>
              <p className="text-gold font-semibold text-sm">{t('gameDetails.characters.personality')}</p>
              <p className="text-darkText dark:text-offWhite text-sm">{char.personality}</p>
            </div>
            <div>
              <p className="text-gold font-semibold text-sm">{t('gameDetails.characters.secret')}</p>
              <p className="text-crimson text-sm">{char.secret}</p>
            </div>
            {char.motive && (
              <div>
                <p className="text-gold font-semibold text-sm">{t('gameDetails.characters.motive')}</p>
                <p className="text-darkText dark:text-offWhite text-sm">{char.motive}</p>
              </div>
            )}
          </CardContent>
        </Card>
      ))}
    </div>
  );
}
