import { useTranslation } from 'react-i18next';
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
  const { t } = useTranslation();

  return (
    <Card>
      <CardHeader>
        <CardTitle>{t('wizard.validationStep.title')}</CardTitle>
      </CardHeader>
      <CardContent>
        {!validation ? (
          <div className="text-center py-8">
            <p className="text-gray-600 dark:text-lightGray mb-4">{t('wizard.validationStep.ready')}</p>
            <Button onClick={onValidate} disabled={loading}>
              {loading ? <Spinner size="sm" /> : t('wizard.validationStep.validate')}
            </Button>
          </div>
        ) : (
          <div className="space-y-4">
            {validation.validation_passed ? (
              <div className="text-green-500 font-semibold text-center">
                ✓ {t('wizard.validationStep.passed')}
              </div>
            ) : (
              <div className="text-crimson">
                <p className="font-semibold mb-2">{t('wizard.validationStep.failed')}</p>
                <ul className="list-disc pl-5 space-y-1">
                  {validation.validation_errors.map((err, i) => (
                    <li key={i}>{err}</li>
                  ))}
                </ul>
                <Button onClick={onViewGame} className="w-full mt-4">
                  {t('wizard.validationStep.viewAnyway')}
                </Button>
              </div>
            )}
          </div>
        )}
      </CardContent>
    </Card>
  );
}
