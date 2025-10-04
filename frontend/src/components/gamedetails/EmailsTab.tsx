import { useState } from 'react';
import { useTranslation } from 'react-i18next';
import type { Character, EmailAssignment } from '@/types';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Spinner } from '@/components/ui/spinner';

interface EmailsTabProps {
  characters: Character[];
}

export function EmailsTab({ characters }: EmailsTabProps) {
  const { t } = useTranslation();
  const [emailAssignments, setEmailAssignments] = useState<EmailAssignment[]>(
    characters.map(c => ({ character_name: c.name, email: '' }))
  );
  const [sendingEmails, setSendingEmails] = useState(false);

  const handleSendEmails = async () => {
    try {
      setSendingEmails(true);
      // TODO: Implement email sending
      await new Promise(resolve => setTimeout(resolve, 1000)); // Simulate API call
      alert(t('gameDetails.emails.notImplemented') + ':\n' +
        emailAssignments.filter(a => a.email).map(a => `${a.character_name}: ${a.email}`).join('\n')
      );
    } finally {
      setSendingEmails(false);
    }
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>{t('gameDetails.emails.title')}</CardTitle>
        <p className="text-sm text-gray-600 dark:text-lightGray">
          {t('gameDetails.emails.description')}
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
                placeholder={t('gameDetails.emails.emailPlaceholder')}
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
          {sendingEmails ? <Spinner size="sm" /> : t('gameDetails.emails.send')}
        </Button>
      </CardContent>
    </Card>
  );
}
