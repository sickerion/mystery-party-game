import { Link } from 'react-router-dom';
import { ThemeToggle } from '../ThemeToggle';

export function Header() {
  return (
    <header className="border-b border-teal dark:border-teal light:border-lightBorder bg-darkNavy dark:bg-darkNavy light:bg-white">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <Link to="/" className="flex items-center gap-2">
            <div className="text-2xl">🔍</div>
            <div>
              <h1 className="text-2xl font-bold text-gold">Mystery Party Generator</h1>
              <p className="text-xs text-lightGray dark:text-lightGray light:text-gray-600">AI-Powered Murder Mystery Games</p>
            </div>
          </Link>
          <nav className="flex items-center gap-4">
            <Link
              to="/"
              className="text-offWhite dark:text-offWhite light:text-darkText hover:text-gold transition-colors"
            >
              My Games
            </Link>
            <Link
              to="/games/new"
              className="text-offWhite dark:text-offWhite light:text-darkText hover:text-gold transition-colors"
            >
              New Game
            </Link>
            <ThemeToggle />
          </nav>
        </div>
      </div>
    </header>
  );
}
