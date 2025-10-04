import type { Character } from '@/types';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';

interface CharactersTabProps {
  characters: Character[];
}

export function CharactersTab({ characters }: CharactersTabProps) {
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
              <p className="text-gold font-semibold text-sm">Background</p>
              <p className="text-darkText dark:text-offWhite text-sm">{char.background}</p>
            </div>
            <div>
              <p className="text-gold font-semibold text-sm">Personality</p>
              <p className="text-darkText dark:text-offWhite text-sm">{char.personality}</p>
            </div>
            <div>
              <p className="text-gold font-semibold text-sm">Secret</p>
              <p className="text-crimson text-sm">{char.secret}</p>
            </div>
            {char.motive && (
              <div>
                <p className="text-gold font-semibold text-sm">Motive</p>
                <p className="text-darkText dark:text-offWhite text-sm">{char.motive}</p>
              </div>
            )}
          </CardContent>
        </Card>
      ))}
    </div>
  );
}
