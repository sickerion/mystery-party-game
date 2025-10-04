import type { MysteryScenario } from '@/types';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';

interface OverviewTabProps {
  scenario: MysteryScenario;
}

export function OverviewTab({ scenario }: OverviewTabProps) {
  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Game Information</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          <div>
            <span className="text-gold font-semibold">Theme: </span>
            <span className="text-offWhite">{scenario.theme}</span>
          </div>
          <div>
            <span className="text-gold font-semibold">Difficulty: </span>
            <span className="text-offWhite">{scenario.difficulty}</span>
          </div>
          <div>
            <span className="text-gold font-semibold">Players: </span>
            <span className="text-offWhite">{scenario.num_players}</span>
          </div>
          <div>
            <span className="text-gold font-semibold">Duration: </span>
            <span className="text-offWhite">{scenario.estimated_duration} minutes</span>
          </div>
          {scenario.introduction && (
            <div className="pt-4 border-t border-teal">
              <p className="text-offWhite whitespace-pre-wrap">{scenario.introduction}</p>
            </div>
          )}
        </CardContent>
      </Card>

      {scenario.game_instructions && (
        <Card>
          <CardHeader>
            <CardTitle>Game Instructions</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-offWhite whitespace-pre-wrap">{scenario.game_instructions}</p>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
