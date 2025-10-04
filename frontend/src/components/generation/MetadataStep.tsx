import { useTranslation } from 'react-i18next';
import type { Metadata } from '@/types';
import { Button } from '@/components/ui/button';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Spinner } from '@/components/ui/spinner';

interface MetadataStepProps {
  metadata: Metadata | null;
  loading: boolean;
  onGenerate: () => void;
  onContinue: () => void;
}

export function MetadataStep({ metadata, loading, onGenerate, onContinue }: MetadataStepProps) {
  const { t } = useTranslation();

  return (
    <Card>
      <CardHeader>
        <CardTitle>{t('wizard.metadataStep.title')}</CardTitle>
      </CardHeader>
      <CardContent>
        {!metadata ? (
          <div className="text-center py-8">
            <p className="text-gray-600 dark:text-lightGray mb-4">{t('wizard.metadataStep.ready')}</p>
            <Button onClick={onGenerate} disabled={loading}>
              {loading ? <Spinner size="sm" /> : t('wizard.metadataStep.generate')}
            </Button>
          </div>
        ) : (
          <div className="space-y-4">
            <div className="text-green-500 font-semibold mb-2">✓ {t('wizard.metadataStep.generated')}</div>
            <div>
              <p className="text-2xl font-bold text-gold">{metadata.title}</p>
              <p className="text-sm text-gray-600 dark:text-lightGray">{t('wizard.metadataStep.duration')}: {metadata.estimated_duration}</p>
            </div>
            <Button onClick={onContinue} disabled={loading} className="w-full">
              {loading ? <Spinner size="sm" /> : t('wizard.metadataStep.continue')}
            </Button>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
