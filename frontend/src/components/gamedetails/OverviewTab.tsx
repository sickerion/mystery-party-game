import { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { useParams } from 'react-router-dom';
import type { MysteryScenario } from '@/types';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Spinner } from '@/components/ui/spinner';
import { AudioPlayer } from '@/components/AudioPlayer';
import { checkAudioStatus, generateAudio, getAudioUrl } from '@/services/api';
import { Volume2 } from 'lucide-react';

interface OverviewTabProps {
  scenario: MysteryScenario;
}

export function OverviewTab({ scenario }: OverviewTabProps) {
  const { t } = useTranslation();
  const { id } = useParams<{ id: string }>();
  const [generatingAudio, setGeneratingAudio] = useState(false);
  const [audioError, setAudioError] = useState<string | null>(null);
  const [hasAudio, setHasAudio] = useState(false);
  const [checkingAudio, setCheckingAudio] = useState(true);

  // Check if audio already exists on component mount
  useEffect(() => {
    const checkAudio = async () => {
      if (!id) return;

      try {
        const status = await checkAudioStatus(id);
        setHasAudio(status.has_audio);
      } catch (error) {
        console.error('Failed to check audio status:', error);
      } finally {
        setCheckingAudio(false);
      }
    };

    checkAudio();
  }, [id]);

  const handleGenerateAudio = async () => {
    if (!id) return;

    try {
      setGeneratingAudio(true);
      setAudioError(null);
      await generateAudio(id);
      setHasAudio(true);
    } catch (error) {
      setAudioError(error instanceof Error ? error.message : 'Failed to generate audio');
    } finally {
      setGeneratingAudio(false);
    }
  };

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>{t('gameDetails.overview.gameInfo')}</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          <div>
            <span className="text-gold font-semibold">{t('gameDetails.overview.theme')}: </span>
            <span className="text-darkText dark:text-offWhite">{scenario.theme}</span>
          </div>
          <div>
            <span className="text-gold font-semibold">{t('gameDetails.overview.difficulty')}: </span>
            <span className="text-darkText dark:text-offWhite">{t(`difficulty.${scenario.difficulty}`, scenario.difficulty)}</span>
          </div>
          <div>
            <span className="text-gold font-semibold">{t('gameDetails.overview.players')}: </span>
            <span className="text-darkText dark:text-offWhite">{scenario.num_players}</span>
          </div>
          <div>
            <span className="text-gold font-semibold">{t('gameDetails.overview.duration')}: </span>
            <span className="text-darkText dark:text-offWhite">{scenario.estimated_duration} {t('gameDetails.overview.minutes')}</span>
          </div>
        </CardContent>
      </Card>

      {scenario.introduction && (
        <Card>
          <CardHeader>
            <CardTitle>Introduction</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <p className="text-darkText dark:text-offWhite whitespace-pre-wrap">{scenario.introduction}</p>

            {checkingAudio ? (
              <div className="flex items-center justify-center py-4">
                <Spinner size="sm" className="mr-2" />
                <span className="text-sm text-gray-600 dark:text-lightGray">{t('audio.checkingStatus')}</span>
              </div>
            ) : !hasAudio ? (
              <div>
                <p className="text-sm text-gray-600 dark:text-lightGray mb-4">
                  {t('audio.generateDescription')}
                </p>
                <Button
                  onClick={handleGenerateAudio}
                  disabled={generatingAudio}
                  className="w-full sm:w-auto"
                >
                  {generatingAudio ? (
                    <>
                      <Spinner size="sm" className="mr-2" />
                      {t('audio.generating')}
                    </>
                  ) : (
                    <>
                      <Volume2 className="w-4 h-4 mr-2" />
                      {t('audio.generateButton')}
                    </>
                  )}
                </Button>
                {audioError && (
                  <p className="text-sm text-crimson mt-2">{audioError}</p>
                )}
              </div>
            ) : (
              <AudioPlayer
                audioUrl={getAudioUrl(id!, 'introduction')}
                label={t('audio.introductionLabel')}
              />
            )}
          </CardContent>
        </Card>
      )}

      {scenario.game_instructions && (
        <Card>
          <CardHeader>
            <CardTitle>{t('gameDetails.overview.instructions')}</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-darkText dark:text-offWhite whitespace-pre-wrap">{scenario.game_instructions}</p>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
