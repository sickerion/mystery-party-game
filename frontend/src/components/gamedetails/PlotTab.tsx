import type { Plot } from '@/types';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';

interface PlotTabProps {
  plot: Plot;
}

export function PlotTab({ plot }: PlotTabProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>The Mystery</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div>
          <p className="text-gold font-semibold">Setting</p>
          <p className="text-darkText dark:text-offWhite">{plot.setting}</p>
        </div>
        <div>
          <p className="text-gold font-semibold">The Crime</p>
          <p className="text-darkText dark:text-offWhite">{plot.crime}</p>
        </div>
        <div>
          <p className="text-gold font-semibold">Victim</p>
          <p className="text-darkText dark:text-offWhite">{plot.victim}</p>
        </div>
        <div>
          <p className="text-gold font-semibold">The Culprit</p>
          <p className="text-crimson">{plot.culprit}</p>
        </div>
        <div>
          <p className="text-gold font-semibold">Method</p>
          <p className="text-darkText dark:text-offWhite">{plot.murder_method}</p>
        </div>
        <div>
          <p className="text-gold font-semibold">Timeline</p>
          <ul className="list-disc pl-5 space-y-1 text-darkText dark:text-offWhite">
            {plot.timeline.map((event, i) => (
              <li key={i}>{event}</li>
            ))}
          </ul>
        </div>
        <div>
          <p className="text-gold font-semibold">Resolution</p>
          <p className="text-darkText dark:text-offWhite">{plot.resolution}</p>
        </div>
      </CardContent>
    </Card>
  );
}
