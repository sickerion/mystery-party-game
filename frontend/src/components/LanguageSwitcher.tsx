import { useTranslation } from 'react-i18next';
import { Button } from './ui/button';
import enFlag from '../assets/en.png';
import frFlag from '../assets/fr.png';

export function LanguageSwitcher() {
  const { i18n } = useTranslation();

  const toggleLanguage = () => {
    const newLang = i18n.language === 'en' ? 'fr' : 'en';
    i18n.changeLanguage(newLang);
  };

  return (
    <Button
      variant="outline"
      size="icon"
      onClick={toggleLanguage}
      aria-label="Toggle language"
      className="relative overflow-hidden"
    >
      <img
        src={i18n.language === 'en' ? enFlag : frFlag}
        alt={i18n.language === 'en' ? 'English' : 'Français'}
        className="h-5 w-5 object-cover rounded-sm"
      />
    </Button>
  );
}
