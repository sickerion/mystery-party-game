import type { Character } from '@/types';
import { Button } from '@/components/ui/button';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Spinner } from '@/components/ui/spinner';

interface CharactersStepProps {
  characters: Character[];
  loading: boolean;
  onGenerate: () => void;
  onContinue: () => void;
}

export function CharactersStep({ characters, loading, onGenerate, onContinue }: CharactersStepProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Generate Characters</CardTitle>
      </CardHeader>
      <CardContent>
        {characters.length === 0 ? (
          <div className="text-center py-8">
            <p className="text-gray-600 dark:text-lightGray mb-4">Ready to generate characters for your mystery</p>
            <Button onClick={onGenerate} disabled={loading}>
              {loading ? <Spinner size="sm" /> : 'Generate Characters'}
            </Button>
          </div>
        ) : (
          <div className="space-y-4">
            <div className="text-green-500 font-semibold mb-2">
              ✓ {characters.length} characters generated!
            </div>
            {characters.map((char, i) => (
              <div key={i} className="border border-gray-300 dark:border-teal rounded p-3">
                <h4 className="font-semibold text-gold">{char.name}</h4>
                <p className="text-sm text-gray-600 dark:text-lightGray">{char.role}</p>
              </div>
            ))}
            <Button onClick={onContinue} disabled={loading} className="w-full">
              {loading ? <Spinner size="sm" /> : 'Continue to Plot'}
            </Button>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
