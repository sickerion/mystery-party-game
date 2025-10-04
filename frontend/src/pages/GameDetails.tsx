import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { getGame, getImageUrl } from '@/services/api';
import type { MysteryScenario } from '@/types';
import { Button } from '@/components/ui/button';
import { Spinner } from '@/components/ui/spinner';
import { OverviewTab } from '@/components/gamedetails/OverviewTab';
import { CharactersTab } from '@/components/gamedetails/CharactersTab';
import { PlotTab } from '@/components/gamedetails/PlotTab';
import { CluesTab } from '@/components/gamedetails/CluesTab';
import { EmailsTab } from '@/components/gamedetails/EmailsTab';

export function GameDetails() {
  const { t } = useTranslation();
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [scenario, setScenario] = useState<MysteryScenario | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<'overview' | 'characters' | 'plot' | 'clues' | 'emails'>('overview');

  useEffect(() => {
    if (!id) return;
    loadGame();
  }, [id]);

  const loadGame = async () => {
    if (!id) return;
    try {
      setLoading(true);
      setError(null);
      const data = await getGame(id);
      setScenario(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load game');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center py-12">
        <Spinner size="lg" />
      </div>
    );
  }

  if (error || !scenario) {
    return (
      <div className="bg-crimson/10 border border-crimson text-crimson px-4 py-3 rounded">
        {error || 'Game not found'}
      </div>
    );
  }

  const tabs = [
    { id: 'overview' as const, label: t('gameDetails.tabs.overview') },
    { id: 'characters' as const, label: t('gameDetails.tabs.characters') },
    { id: 'plot' as const, label: t('gameDetails.tabs.plot') },
    { id: 'clues' as const, label: t('gameDetails.tabs.clues') },
    { id: 'emails' as const, label: t('gameDetails.tabs.emails') },
  ];

  return (
    <div>
      {/* Cover Image Banner */}
      <div className="w-full h-64 overflow-hidden rounded-lg mb-8 bg-gray-200 dark:bg-darkGray">
        <img
          src={getImageUrl(id!)}
          alt={scenario.title}
          className="w-full h-full object-cover"
          onError={(e) => {
            // Hide image if it fails to load (not generated yet)
            e.currentTarget.style.display = 'none';
            e.currentTarget.parentElement!.style.display = 'none';
          }}
        />
      </div>

      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-4xl font-bold text-gold mb-2">
            {scenario.title}
          </h1>
          <div className="flex items-center gap-4 text-gray-600 dark:text-lightGray">
            <span>{scenario.num_players} {t('landing.players')}</span>
            <span>•</span>
            <span>{t(`difficulty.${scenario.difficulty}`, scenario.difficulty)}</span>
            <span>•</span>
            <span>{scenario.estimated_duration} {t('gameDetails.overview.minutes')}</span>
          </div>
        </div>
        <Button variant="outline" onClick={() => navigate('/')}>
          {t('common.back')}
        </Button>
      </div>

      {/* Tabs */}
      <div className="flex gap-2 mb-6 border-b border-teal">
        {tabs.map(tab => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`px-4 py-2 font-medium transition-colors ${
              activeTab === tab.id
                ? 'text-gold border-b-2 border-gold'
                : 'text-lightGray hover:text-offWhite'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Tab Content */}
      {activeTab === 'overview' && <OverviewTab scenario={scenario} />}
      {activeTab === 'characters' && <CharactersTab characters={scenario.characters} gameId={id!} />}
      {activeTab === 'plot' && <PlotTab plot={scenario.plot} />}
      {activeTab === 'clues' && <CluesTab clues={scenario.clues} />}
      {activeTab === 'emails' && <EmailsTab characters={scenario.characters} />}
    </div>
  );
}
