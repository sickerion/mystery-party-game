# Mystery Party Game Generator - Frontend

Modern web interface for generating AI-powered murder mystery party game scenarios.

## Tech Stack

- **React 19** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool and dev server
- **React Router** - Navigation
- **shadcn/ui** - UI component library
- **Tailwind CSS v3** - Styling
- **Vitest** - Testing framework

## Features

- **Multi-step Generation Wizard**: Create mystery games through a guided 6-step process
- **Game Management**: View, filter, and manage generated mystery scenarios
- **Detailed Game View**: Explore characters, plots, clues, and game instructions
- **Email Assignment**: Assign player emails to characters for automated distribution
- **Mystery Theme**: Custom color palette with navy, gold, crimson, and purple accents
- **Responsive Design**: Works on desktop and mobile devices

## Getting Started

### Prerequisites

- Node.js 18+ and npm

### Installation

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install
```

### Development

```bash
# Start dev server (default: http://localhost:5173)
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Run tests
npm run test

# Run tests with UI
npm run test:ui

# Run tests once
npm run test:run

# Lint code
npm run lint
```

### Backend Connection

The frontend expects the backend API to be running at `http://localhost:8000`.

To start the backend:
```bash
# From project root
uvicorn src.api.main:app --reload
```

## Project Structure

```
frontend/
├── src/
│   ├── components/          # React components
│   │   ├── ui/             # Base UI components (Button, Card, Input, etc.)
│   │   ├── generation/     # Generation wizard components
│   │   ├── gamedetails/    # Game details tab components
│   │   └── GameCard.tsx    # Game list card component
│   ├── pages/              # Page components
│   │   ├── Landing.tsx     # Game list page
│   │   ├── GameDetails.tsx # Game details page
│   │   └── GenerationWizard.tsx # Multi-step generation wizard
│   ├── services/           # API client and services
│   │   └── api.ts          # Backend API client
│   ├── types/              # TypeScript type definitions
│   │   └── index.ts        # Shared types
│   ├── lib/                # Utility functions
│   │   └── utils.ts        # Helper functions
│   ├── test/               # Test configuration
│   │   └── setup.ts        # Vitest setup
│   ├── App.tsx             # Root component
│   └── main.tsx            # Entry point
├── public/                 # Static assets
├── package.json            # Dependencies and scripts
├── vite.config.ts          # Vite configuration
├── tailwind.config.js      # Tailwind CSS configuration
└── tsconfig.json           # TypeScript configuration
```

## Key Pages

### Landing Page (/)
- Lists all generated mystery party games
- Filter games by status
- Delete existing games
- Navigate to game details or create new game

### Generation Wizard (/games/new)
6-step process to create a mystery:
1. **Game Details**: Theme, players, difficulty, special requests
2. **Characters**: AI-generated character profiles
3. **Plot**: Crime details, victim, culprit, timeline
4. **Clues**: Evidence and red herrings
5. **Metadata**: Title, duration, instructions
6. **Validation**: Scenario coherence check

### Game Details (/games/:id)
Tabbed interface showing:
- **Overview**: Game info, instructions, introduction
- **Characters**: Character profiles with backgrounds and secrets
- **Plot**: Crime details and timeline
- **Clues**: Evidence distribution
- **Send Emails**: Assign emails to characters (backend integration pending)

## API Integration

All API calls go through `src/services/api.ts`:

```typescript
// Create new game
const game = await createGame({
  theme: "Film Noir",
  num_players: 6,
  difficulty: "medium",
  special_requests: null
});

// Generate components step-by-step
await generateCharacters(gameId);
await generatePlot(gameId);
await generateClues(gameId);
await generateMetadata(gameId);
await validateScenario(gameId);

// Retrieve complete scenario
const scenario = await getGame(gameId);
```

## Color Palette

Custom mystery-themed colors defined in `tailwind.config.js`:

```javascript
colors: {
  // Primary
  navy: '#1a1a2e',        // Main background
  darkNavy: '#16213e',    // Sections
  teal: '#0f3460',        // Accents

  // Accent
  gold: '#d4af37',        // CTA, important elements
  crimson: '#8b0000',     // Alerts, mystery theme
  purple: '#9b59b6',      // Links, hover

  // Neutral
  offWhite: '#e8e8e8',    // Primary text
  lightGray: '#a8a8a8',   // Secondary text
  darkGray: '#2d2d2d',    // Cards, panels
}
```

## Testing

Test suite includes:
- **UI Component Tests**: Button, Card, Spinner
- **Feature Component Tests**: GameCard with loading states
- **API Service Tests**: All backend integration methods

Run tests with:
```bash
npm run test        # Watch mode
npm run test:ui     # Interactive UI
npm run test:run    # Single run
```

## Building for Production

```bash
# Build optimized production bundle
npm run build

# Output will be in dist/ directory
# Deploy dist/ to your hosting service
```

## Environment Configuration

Create `.env` file in frontend directory if needed:

```bash
VITE_API_URL=http://localhost:8000  # Backend API URL
```

Access in code:
```typescript
const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
```

## Troubleshooting

### Backend Connection Issues
- Ensure backend is running at `http://localhost:8000`
- Check CORS settings in backend if running on different ports
- Verify API endpoints match backend routes

### Build Errors
- Clear node_modules and reinstall: `rm -rf node_modules && npm install`
- Clear Vite cache: `rm -rf node_modules/.vite`

### Tailwind CSS Issues
- Ensure Tailwind v3 is installed (v4 has different PostCSS plugin)
- Rebuild: `npm run build`

## Contributing

When adding new components:
1. Create component in appropriate directory
2. Add TypeScript types
3. Write tests in `.test.tsx` file
4. Update this README if adding major features

## License

Part of the Mystery Party Game Generator project.
