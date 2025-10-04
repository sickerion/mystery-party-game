import type { ValidationResult } from '@/types';
import { Button } from '@/components/ui/button';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Spinner } from '@/components/ui/spinner';

interface ValidationStepProps {
  validation: ValidationResult | null;
  loading: boolean;
  gameId: string;
  onValidate: () => void;
  onViewGame: () => void;
}

export function ValidationStep({ validation, loading, onValidate, onViewGame }: ValidationStepProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Validation</CardTitle>
      </CardHeader>
      <CardContent>
        {!validation ? (
          <div className="text-center py-8">
            <p className="text-lightGray mb-4">Validate the complete scenario</p>
            <Button onClick={onValidate} disabled={loading}>
              {loading ? <Spinner size="sm" /> : 'Validate'}
            </Button>
          </div>
        ) : (
          <div className="space-y-4">
            {validation.validation_passed ? (
              <div className="text-green-500 font-semibold text-center">
                ✓ Validation passed! Redirecting...
              </div>
            ) : (
              <div className="text-crimson">
                <p className="font-semibold mb-2">Validation failed:</p>
                <ul className="list-disc pl-5 space-y-1">
                  {validation.validation_errors.map((err, i) => (
                    <li key={i}>{err}</li>
                  ))}
                </ul>
                <Button onClick={onViewGame} className="w-full mt-4">
                  View Game Anyway
                </Button>
              </div>
            )}
          </div>
        )}
      </CardContent>
    </Card>
  );
}
