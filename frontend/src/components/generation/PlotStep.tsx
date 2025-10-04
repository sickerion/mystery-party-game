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
  return (
    <Card>
      <CardHeader>
        <CardTitle>Generate Plot</CardTitle>
      </CardHeader>
      <CardContent>
        {!plot ? (
          <div className="text-center py-8">
            <p className="text-lightGray mb-4">Create the main storyline and mystery</p>
            <Button onClick={onGenerate} disabled={loading}>
              {loading ? <Spinner size="sm" /> : 'Generate Plot'}
            </Button>
          </div>
        ) : (
          <div className="space-y-4">
            <div className="text-green-500 font-semibold mb-2">✓ Plot generated!</div>
            <div className="space-y-2">
              <p><span className="text-gold">Crime:</span> {plot.crime}</p>
              <p><span className="text-gold">Victim:</span> {plot.victim}</p>
              <p><span className="text-gold">Setting:</span> {plot.setting}</p>
            </div>
            <Button onClick={onContinue} disabled={loading} className="w-full">
              {loading ? <Spinner size="sm" /> : 'Continue to Clues'}
            </Button>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
