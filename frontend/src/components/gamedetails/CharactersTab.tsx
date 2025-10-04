import { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import type { Character } from '@/types';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { getCharacterImageUrl } from '@/services/api';

interface CharactersTabProps {
  characters: Character[];
  gameId: string;
}

function CharacterPortrait({ gameId, character }: { gameId: string; character: Character }) {
  const [imageError, setImageError] = useState(false);
  const [retryCount, setRetryCount] = useState(0);

  useEffect(() => {
    // Reset when character changes
    setImageError(false);
    setRetryCount(0);
  }, [character.id]);

  useEffect(() => {
    // Retry loading image after error (images might still be generating)
    if (imageError && retryCount < 3) {
      const timeout = setTimeout(() => {
        console.log(`Retrying image load for ${character.name} (attempt ${retryCount + 1})`);
        setImageError(false);
        setRetryCount(prev => prev + 1);
      }, 5000); // Retry after 5 seconds

      return () => clearTimeout(timeout);
    }
  }, [imageError, retryCount, character.name]);

  if (!character.id) {
    return null;
  }

  if (imageError && retryCount >= 3) {
    // After 3 retries, hide the image container
    return null;
  }

  return (
    <div className="w-full h-48 overflow-hidden rounded-t-lg bg-gray-200 dark:bg-darkGray flex items-center justify-center">
      {imageError ? (
        <div className="text-gray-500 text-sm">Loading portrait...</div>
      ) : (
        <img
          key={retryCount} // Force re-render on retry
          src={getCharacterImageUrl(gameId, character.id)}
          alt={character.name}
          className="w-full h-full object-cover"
          onError={() => {
            console.log(`Failed to load image for ${character.name}`);
            setImageError(true);
          }}
          onLoad={() => {
            console.log(`Successfully loaded image for ${character.name}`);
          }}
        />
      )}
    </div>
  );
}

export function CharactersTab({ characters, gameId }: CharactersTabProps) {
  const { t } = useTranslation();

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      {characters.map((char, i) => (
        <Card key={i}>
          <CharacterPortrait gameId={gameId} character={char} />
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
