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
  return (
    <Card>
      <CardHeader>
        <CardTitle>Generate Clues</CardTitle>
      </CardHeader>
      <CardContent>
        {clues.length === 0 ? (
          <div className="text-center py-8">
            <p className="text-lightGray mb-4">Create clues and red herrings</p>
            <Button onClick={onGenerate} disabled={loading}>
              {loading ? <Spinner size="sm" /> : 'Generate Clues'}
            </Button>
          </div>
        ) : (
          <div className="space-y-4">
            <div className="text-green-500 font-semibold mb-2">✓ {clues.length} clues generated!</div>
            <Button onClick={onContinue} disabled={loading} className="w-full">
              {loading ? <Spinner size="sm" /> : 'Continue to Metadata'}
            </Button>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
