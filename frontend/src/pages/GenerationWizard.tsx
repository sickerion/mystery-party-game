import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  createGame,
  generateCharacters,
  generatePlot,
  generateClues,
  generateMetadata,
  validateScenario,
} from '@/services/api';
import type { GameRequest, Character, Plot, Clue, Metadata, ValidationResult, GenerationStep } from '@/types';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Spinner } from '@/components/ui/spinner';

const steps: { id: GenerationStep; label: string }[] = [
  { id: 'initial', label: 'Game Details' },
  { id: 'characters', label: 'Characters' },
  { id: 'plot', label: 'Plot' },
  { id: 'clues', label: 'Clues' },
  { id: 'metadata', label: 'Metadata' },
  { id: 'validation', label: 'Validation' },
];

export function GenerationWizard() {
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
      setError('Theme is required');
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
        setTimeout(() => navigate(`/games/${gameId}`), 2000);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to validate scenario');
    } finally {
      setLoading(false);
    }
  };

  const currentStepIndex = steps.findIndex(s => s.id === currentStep);

  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-4xl font-bold text-gold mb-8">Create New Mystery Game</h1>

      {/* Progress Indicator */}
      <div className="mb-8">
        <div className="flex items-center justify-between">
          {steps.map((step, index) => (
            <div key={step.id} className="flex-1 relative">
              <div className="flex flex-col items-center">
                <div
                  className={`w-10 h-10 rounded-full flex items-center justify-center font-semibold ${
                    index < currentStepIndex
                      ? 'bg-gold text-navy'
                      : index === currentStepIndex
                      ? 'bg-teal text-offWhite'
                      : 'bg-darkGray text-lightGray'
                  }`}
                >
                  {index + 1}
                </div>
                <p className={`text-xs mt-2 ${index <= currentStepIndex ? 'text-offWhite' : 'text-lightGray'}`}>
                  {step.label}
                </p>
              </div>
              {index < steps.length - 1 && (
                <div
                  className={`absolute top-5 left-1/2 w-full h-0.5 ${
                    index < currentStepIndex ? 'bg-gold' : 'bg-darkGray'
                  }`}
                />
              )}
            </div>
          ))}
        </div>
      </div>

      {error && (
        <div className="bg-crimson/10 border border-crimson text-crimson px-4 py-3 rounded mb-6">
          {error}
        </div>
      )}

      {/* Step Content */}
      {currentStep === 'initial' && (
        <Card>
          <CardHeader>
            <CardTitle>Game Details</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <Label htmlFor="theme">Theme *</Label>
              <Input
                id="theme"
                placeholder="e.g., Film Noir, Victorian Era, Sci-Fi Space Station"
                value={formData.theme}
                onChange={(e) => setFormData({ ...formData, theme: e.target.value })}
              />
            </div>
            <div>
              <Label htmlFor="num_players">Number of Players</Label>
              <Input
                id="num_players"
                type="number"
                min="4"
                max="12"
                value={formData.num_players}
                onChange={(e) => setFormData({ ...formData, num_players: parseInt(e.target.value) })}
              />
            </div>
            <div>
              <Label htmlFor="difficulty">Difficulty</Label>
              <select
                id="difficulty"
                className="flex h-10 w-full rounded-md border border-teal bg-darkNavy px-3 py-2 text-sm text-offWhite"
                value={formData.difficulty}
                onChange={(e) => setFormData({ ...formData, difficulty: e.target.value as any })}
              >
                <option value="easy">Easy</option>
                <option value="medium">Medium</option>
                <option value="hard">Hard</option>
              </select>
            </div>
            <div>
              <Label htmlFor="special_requests">Special Requests (Optional)</Label>
              <Input
                id="special_requests"
                placeholder="Any specific requirements or preferences"
                value={formData.special_requests}
                onChange={(e) => setFormData({ ...formData, special_requests: e.target.value })}
              />
            </div>
            <Button onClick={handleCreateGame} disabled={loading} className="w-full">
              {loading ? <Spinner size="sm" /> : 'Start Generation'}
            </Button>
          </CardContent>
        </Card>
      )}

      {currentStep === 'characters' && (
        <Card>
          <CardHeader>
            <CardTitle>Generate Characters</CardTitle>
          </CardHeader>
          <CardContent>
            {characters.length === 0 ? (
              <div className="text-center py-8">
                <p className="text-lightGray mb-4">Ready to generate characters for your mystery</p>
                <Button onClick={handleGenerateCharacters} disabled={loading}>
                  {loading ? <Spinner size="sm" /> : 'Generate Characters'}
                </Button>
              </div>
            ) : (
              <div className="space-y-4">
                <div className="text-green-500 font-semibold mb-2">
                  ✓ {characters.length} characters generated!
                </div>
                {characters.map((char, i) => (
                  <div key={i} className="border border-teal rounded p-3">
                    <h4 className="font-semibold text-gold">{char.name}</h4>
                    <p className="text-sm text-lightGray">{char.role}</p>
                  </div>
                ))}
                <Button onClick={handleGeneratePlot} disabled={loading} className="w-full">
                  Continue to Plot
                </Button>
              </div>
            )}
          </CardContent>
        </Card>
      )}

      {currentStep === 'plot' && (
        <Card>
          <CardHeader>
            <CardTitle>Generate Plot</CardTitle>
          </CardHeader>
          <CardContent>
            {!plot ? (
              <div className="text-center py-8">
                <p className="text-lightGray mb-4">Create the main storyline and mystery</p>
                <Button onClick={handleGeneratePlot} disabled={loading}>
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
                <Button onClick={handleGenerateClues} disabled={loading} className="w-full">
                  Continue to Clues
                </Button>
              </div>
            )}
          </CardContent>
        </Card>
      )}

      {currentStep === 'clues' && (
        <Card>
          <CardHeader>
            <CardTitle>Generate Clues</CardTitle>
          </CardHeader>
          <CardContent>
            {clues.length === 0 ? (
              <div className="text-center py-8">
                <p className="text-lightGray mb-4">Create clues and red herrings</p>
                <Button onClick={handleGenerateClues} disabled={loading}>
                  {loading ? <Spinner size="sm" /> : 'Generate Clues'}
                </Button>
              </div>
            ) : (
              <div className="space-y-4">
                <div className="text-green-500 font-semibold mb-2">✓ {clues.length} clues generated!</div>
                <Button onClick={handleGenerateMetadata} disabled={loading} className="w-full">
                  Continue to Metadata
                </Button>
              </div>
            )}
          </CardContent>
        </Card>
      )}

      {currentStep === 'metadata' && (
        <Card>
          <CardHeader>
            <CardTitle>Generate Metadata</CardTitle>
          </CardHeader>
          <CardContent>
            {!metadata ? (
              <div className="text-center py-8">
                <p className="text-lightGray mb-4">Generate title and game instructions</p>
                <Button onClick={handleGenerateMetadata} disabled={loading}>
                  {loading ? <Spinner size="sm" /> : 'Generate Metadata'}
                </Button>
              </div>
            ) : (
              <div className="space-y-4">
                <div className="text-green-500 font-semibold mb-2">✓ Metadata generated!</div>
                <div>
                  <p className="text-2xl font-bold text-gold">{metadata.title}</p>
                  <p className="text-sm text-lightGray">Duration: {metadata.estimated_duration}</p>
                </div>
                <Button onClick={handleValidate} disabled={loading} className="w-full">
                  Validate Scenario
                </Button>
              </div>
            )}
          </CardContent>
        </Card>
      )}

      {currentStep === 'validation' && (
        <Card>
          <CardHeader>
            <CardTitle>Validation</CardTitle>
          </CardHeader>
          <CardContent>
            {!validation ? (
              <div className="text-center py-8">
                <p className="text-lightGray mb-4">Validate the complete scenario</p>
                <Button onClick={handleValidate} disabled={loading}>
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
                    <Button onClick={() => navigate(`/games/${gameId}`)} className="w-full mt-4">
                      View Game Anyway
                    </Button>
                  </div>
                )}
              </div>
            )}
          </CardContent>
        </Card>
      )}
    </div>
  );
}
