import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { ThemeToggle } from '../ThemeToggle';
import { LanguageSwitcher } from '../LanguageSwitcher';

export function Header() {
  const { t } = useTranslation();

  return (
    <header className="border-b border-lightBorder dark:border-teal bg-white dark:bg-darkNavy">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <Link to="/" className="flex items-center gap-2">
            <div className="text-2xl">🔍</div>
            <div>
              <h1 className="text-2xl font-bold text-gold">{t('header.title')}</h1>
              <p className="text-xs text-gray-600 dark:text-lightGray">{t('header.subtitle')}</p>
            </div>
          </Link>
          <nav className="flex items-center gap-4">
            <Link
              to="/"
              className="text-darkText dark:text-offWhite hover:text-gold transition-colors"
            >
              {t('header.myGames')}
            </Link>
            <Link
              to="/games/new"
              className="text-darkText dark:text-offWhite hover:text-gold transition-colors"
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
