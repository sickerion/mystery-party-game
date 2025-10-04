import { Link } from 'react-router-dom';

export function Header() {
  return (
    <header className="border-b border-teal bg-darkNavy">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <Link to="/" className="flex items-center gap-2">
            <div className="text-2xl">🔍</div>
            <div>
              <h1 className="text-2xl font-bold text-gold">Mystery Party Generator</h1>
              <p className="text-xs text-lightGray">AI-Powered Murder Mystery Games</p>
            </div>
          </Link>
          <nav className="flex items-center gap-4">
            <Link
              to="/"
              className="text-offWhite hover:text-gold transition-colors"
            >
              My Games
            </Link>
            <Link
              to="/games/new"
              className="text-offWhite hover:text-gold transition-colors"
            >
              New Game
            </Link>
          </nav>
        </div>
      </div>
    </header>
  );
}
