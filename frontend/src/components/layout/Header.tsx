import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { ThemeToggle } from '../ThemeToggle';
import { LanguageSwitcher } from '../LanguageSwitcher';

export function Header() {
  const { t } = useTranslation();

  return (
    <header className="border-b border-teal dark:border-teal light:border-lightBorder bg-darkNavy dark:bg-darkNavy light:bg-white">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <Link to="/" className="flex items-center gap-2">
            <div className="text-2xl">🔍</div>
            <div>
              <h1 className="text-2xl font-bold text-gold">{t('header.title')}</h1>
              <p className="text-xs text-lightGray dark:text-lightGray light:text-gray-600">{t('header.subtitle')}</p>
            </div>
          </Link>
          <nav className="flex items-center gap-4">
            <Link
              to="/"
              className="text-offWhite dark:text-offWhite light:text-darkText hover:text-gold transition-colors"
            >
              {t('header.myGames')}
            </Link>
            <Link
              to="/games/new"
              className="text-offWhite dark:text-offWhite light:text-darkText hover:text-gold transition-colors"
            >
              {t('header.newGame')}
            </Link>
            <LanguageSwitcher />
            <ThemeToggle />
          </nav>
        </div>
      </div>
    </header>
  );
}
