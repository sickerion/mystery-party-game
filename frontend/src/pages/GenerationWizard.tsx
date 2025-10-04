import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import {
  createGame,
  generateCharacters,
  generatePlot,
  generateClues,
  generateMetadata,
  validateScenario,
  generateImage,
  generateCharacterImage,
} from '@/services/api';
import type { GameRequest, Character, Plot, Clue, Metadata, ValidationResult, GenerationStep } from '@/types';
import { StepIndicator } from '@/components/generation/StepIndicator';
import { GameForm } from '@/components/generation/GameForm';
import { CharactersStep } from '@/components/generation/CharactersStep';
import { PlotStep } from '@/components/generation/PlotStep';
import { CluesStep } from '@/components/generation/CluesStep';
import { MetadataStep } from '@/components/generation/MetadataStep';
import { ValidationStep } from '@/components/generation/ValidationStep';

export function GenerationWizard() {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const [currentStep, setCurrentStep] = useState<GenerationStep>('initial');
  const [gameId, setGameId] = useState<string>('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Form data
  const [formData, setFormData] = useState<GameRequest>({
    theme: '',
    num_players: 6,
    difficulty: 'medium',
    special_requests: '',
  });

  // Generated data
  const [characters, setCharacters] = useState<Character[]>([]);
  const [plot, setPlot] = useState<Plot | null>(null);
  const [clues, setClues] = useState<Clue[]>([]);
  const [metadata, setMetadata] = useState<Metadata | null>(null);
  const [validation, setValidation] = useState<ValidationResult | null>(null);

  const handleCreateGame = async () => {
    if (!formData.theme.trim()) {
      setError(t('wizard.form.theme') + ' ' + t('common.error'));
      return;
    }

    try {
      setLoading(true);
      setError(null);
      const game = await createGame(formData);
      setGameId(game.id);
      setCurrentStep('characters');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create game');
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateCharacters = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await generateCharacters(gameId);
      setCharacters(data);
      setCurrentStep('plot');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to generate characters');
    } finally {
      setLoading(false);
    }
  };

  const handleGeneratePlot = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await generatePlot(gameId);
      setPlot(data);
      setCurrentStep('clues');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to generate plot');
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateClues = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await generateClues(gameId);
      setClues(data);
      setCurrentStep('metadata');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to generate clues');
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateMetadata = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await generateMetadata(gameId);
      setMetadata(data);
      setCurrentStep('validation');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to generate metadata');
    } finally {
      setLoading(false);
    }
  };

  const handleValidate = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await validateScenario(gameId);
      setValidation(data);
      if (data.validation_passed) {
        // Generate cover image in background (don't wait for it)
        generateImage(gameId).catch(err => {
          console.error('Failed to generate cover image:', err);
          // Don't show error to user, image generation is optional
        });

        // Generate character portrait images in background
        characters.forEach(character => {
          if (character.id) {
            generateCharacterImage(gameId, character.id).catch(err => {
              console.error(`Failed to generate portrait for ${character.name}:`, err);
              // Don't show error to user, image generation is optional
            });
          }
        });

        setTimeout(() => navigate(`/games/${gameId}`), 2000);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to validate scenario');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-4xl font-bold text-gold mb-8">{t('wizard.title')}</h1>

      <StepIndicator currentStep={currentStep} />

      {error && (
        <div className="bg-crimson/10 border border-crimson text-crimson px-4 py-3 rounded mb-6">
          {error}
        </div>
      )}

      {currentStep === 'initial' && (
        <GameForm
          formData={formData}
          loading={loading}
          onChange={setFormData}
          onSubmit={handleCreateGame}
        />
      )}

      {currentStep === 'characters' && (
        <CharactersStep
          characters={characters}
          loading={loading}
          onGenerate={handleGenerateCharacters}
          onContinue={handleGeneratePlot}
        />
      )}

      {currentStep === 'plot' && (
        <PlotStep
          plot={plot}
          loading={loading}
          onGenerate={handleGeneratePlot}
          onContinue={handleGenerateClues}
        />
      )}

      {currentStep === 'clues' && (
        <CluesStep
          clues={clues}
          loading={loading}
          onGenerate={handleGenerateClues}
          onContinue={handleGenerateMetadata}
        />
      )}

      {currentStep === 'metadata' && (
        <MetadataStep
          metadata={metadata}
          loading={loading}
          onGenerate={handleGenerateMetadata}
          onContinue={handleValidate}
        />
      )}

      {currentStep === 'validation' && (
        <ValidationStep
          validation={validation}
          loading={loading}
          gameId={gameId}
          onValidate={handleValidate}
          onViewGame={() => navigate(`/games/${gameId}`)}
        />
      )}
    </div>
  );
}
