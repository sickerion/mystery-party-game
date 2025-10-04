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
  return (
    <Card>
      <CardHeader>
        <CardTitle>Generate Metadata</CardTitle>
      </CardHeader>
      <CardContent>
        {!metadata ? (
          <div className="text-center py-8">
            <p className="text-gray-600 dark:text-lightGray mb-4">Generate title and game instructions</p>
            <Button onClick={onGenerate} disabled={loading}>
              {loading ? <Spinner size="sm" /> : 'Generate Metadata'}
            </Button>
          </div>
        ) : (
          <div className="space-y-4">
            <div className="text-green-500 font-semibold mb-2">✓ Metadata generated!</div>
            <div>
              <p className="text-2xl font-bold text-gold">{metadata.title}</p>
              <p className="text-sm text-gray-600 dark:text-lightGray">Duration: {metadata.estimated_duration}</p>
            </div>
            <Button onClick={onContinue} disabled={loading} className="w-full">
              {loading ? <Spinner size="sm" /> : 'Validate Scenario'}
            </Button>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
