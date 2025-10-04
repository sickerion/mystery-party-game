import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getGame } from '@/services/api';
import type { MysteryScenario, EmailAssignment } from '@/types';
import { Button } from '@/components/ui/button';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Spinner } from '@/components/ui/spinner';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';

export function GameDetails() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [scenario, setScenario] = useState<MysteryScenario | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<'overview' | 'characters' | 'plot' | 'clues' | 'emails'>('overview');
  const [emailAssignments, setEmailAssignments] = useState<EmailAssignment[]>([]);
  const [sendingEmails, setSendingEmails] = useState(false);

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
      // Initialize email assignments
      if (data.characters) {
        setEmailAssignments(
          data.characters.map(c => ({ character_name: c.name, email: '' }))
        );
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load game');
    } finally {
      setLoading(false);
    }
  };

  const handleSendEmails = async () => {
    try {
      setSendingEmails(true);
      // TODO: Implement email sending
      await new Promise(resolve => setTimeout(resolve, 1000)); // Simulate API call
      alert('Email sending not yet implemented. Will send to:\n' +
        emailAssignments.filter(a => a.email).map(a => `${a.character_name}: ${a.email}`).join('\n')
      );
    } finally {
      setSendingEmails(false);
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
    { id: 'overview' as const, label: 'Overview' },
    { id: 'characters' as const, label: 'Characters' },
    { id: 'plot' as const, label: 'Plot' },
    { id: 'clues' as const, label: 'Clues' },
    { id: 'emails' as const, label: 'Send Emails' },
  ];

  return (
    <div>
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-4xl font-bold text-gold mb-2">
            {scenario.title}
          </h1>
          <div className="flex items-center gap-4 text-lightGray">
            <span>{scenario.num_players} players</span>
            <span>•</span>
            <span>{scenario.difficulty}</span>
            <span>•</span>
            <span>{scenario.estimated_duration} minutes</span>
          </div>
        </div>
        <Button variant="outline" onClick={() => navigate('/')}>
          Back to Games
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
      {activeTab === 'overview' && (
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
      )}

      {activeTab === 'characters' && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {scenario.characters.map((char, i) => (
            <Card key={i}>
              <CardHeader>
                <CardTitle>{char.name}</CardTitle>
                <p className="text-sm text-lightGray">{char.role}</p>
              </CardHeader>
              <CardContent className="space-y-3">
                <div>
                  <p className="text-gold font-semibold text-sm">Background</p>
                  <p className="text-offWhite text-sm">{char.background}</p>
                </div>
                <div>
                  <p className="text-gold font-semibold text-sm">Personality</p>
                  <p className="text-offWhite text-sm">{char.personality}</p>
                </div>
                <div>
                  <p className="text-gold font-semibold text-sm">Secret</p>
                  <p className="text-crimson text-sm">{char.secret}</p>
                </div>
                {char.motive && (
                  <div>
                    <p className="text-gold font-semibold text-sm">Motive</p>
                    <p className="text-offWhite text-sm">{char.motive}</p>
                  </div>
                )}
              </CardContent>
            </Card>
          ))}
        </div>
      )}

      {activeTab === 'plot' && scenario.plot && (
        <Card>
          <CardHeader>
            <CardTitle>The Mystery</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <p className="text-gold font-semibold">Setting</p>
              <p className="text-offWhite">{scenario.plot.setting}</p>
            </div>
            <div>
              <p className="text-gold font-semibold">The Crime</p>
              <p className="text-offWhite">{scenario.plot.crime}</p>
            </div>
            <div>
              <p className="text-gold font-semibold">Victim</p>
              <p className="text-offWhite">{scenario.plot.victim}</p>
            </div>
            <div>
              <p className="text-gold font-semibold">The Culprit</p>
              <p className="text-crimson">{scenario.plot.culprit}</p>
            </div>
            <div>
              <p className="text-gold font-semibold">Method</p>
              <p className="text-offWhite">{scenario.plot.murder_method}</p>
            </div>
            <div>
              <p className="text-gold font-semibold">Timeline</p>
              <ul className="list-disc pl-5 space-y-1 text-offWhite">
                {scenario.plot.timeline.map((event, i) => (
                  <li key={i}>{event}</li>
                ))}
              </ul>
            </div>
            <div>
              <p className="text-gold font-semibold">Resolution</p>
              <p className="text-offWhite">{scenario.plot.resolution}</p>
            </div>
          </CardContent>
        </Card>
      )}

      {activeTab === 'clues' && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {scenario.clues.map((clue, i) => (
            <Card key={i}>
              <CardHeader>
                <div className="flex items-start justify-between">
                  <CardTitle className="text-lg">Clue #{clue.clue_id}</CardTitle>
                  {clue.misleading && (
                    <Badge variant="destructive">Red Herring</Badge>
                  )}
                </div>
              </CardHeader>
              <CardContent className="space-y-2">
                <p className="text-offWhite">{clue.description}</p>
                <div className="text-sm space-y-1">
                  <p><span className="text-gold">Location:</span> {clue.location}</p>
                  <p><span className="text-gold">Revealed by:</span> {clue.revealed_by}</p>
                  <p><span className="text-gold">Significance:</span> {clue.significance}</p>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}

      {activeTab === 'emails' && (
        <Card>
          <CardHeader>
            <CardTitle>Send Character Emails</CardTitle>
            <p className="text-sm text-lightGray">
              Assign emails to each character to send them their role information
            </p>
          </CardHeader>
          <CardContent className="space-y-4">
            {emailAssignments.map((assignment, i) => (
              <div key={i} className="flex items-center gap-4">
                <div className="flex-1">
                  <Label className="text-gold">{assignment.character_name}</Label>
                </div>
                <div className="flex-[2]">
                  <Input
                    type="email"
                    placeholder="player@example.com"
                    value={assignment.email}
                    onChange={(e) => {
                      const updated = [...emailAssignments];
                      updated[i].email = e.target.value;
                      setEmailAssignments(updated);
                    }}
                  />
                </div>
              </div>
            ))}
            <Button
              onClick={handleSendEmails}
              disabled={!emailAssignments.some(a => a.email) || sendingEmails}
              className="w-full"
            >
              {sendingEmails ? <Spinner size="sm" /> : 'Send Emails'}
            </Button>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
