# Mystery Party Game Generator

AI-powered mystery party game generator using LangGraph and Anthropic Claude.

Generate complete murder mystery party game scenarios with characters, plots, clues, and game instructions - all powered by AI.

## Features

- 🎭 Generate diverse characters with backgrounds, personalities, and secrets
- 🖼️ AI-generated character portraits using DALL-E 2
- 🎨 AI-generated cover images for each mystery game
- 🔊 Text-to-speech audio narration with OpenAI TTS
- 📖 Create compelling murder mystery plots with victims, culprits, and methods
- 🔍 Generate clues and red herrings for investigation
- 🎮 Complete game instructions and atmospheric introductions
- ✅ Automatic validation for scenario coherence
- 🔄 Retry mechanism for quality assurance
- 🌐 Full internationalization support (English/French)
- 🌓 Dark/Light theme support
- 🚀 RESTful API for easy integration
- 💾 Database persistence with incremental generation

## Setup

### Prerequisites
- Python 3.11+
- Node.js 18+ (for frontend)
- Anthropic API key (for content generation)
- OpenAI API key (for image generation and TTS)

### Backend Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your API keys:
# - ANTHROPIC_API_KEY (required)
# - OPENAI_API_KEY (required for images and audio)

# Run database migrations
alembic upgrade head
```

### Frontend Installation

```bash
cd frontend
npm install
```

## Usage

### Start the Backend Server

```bash
uvicorn src.api.main:app --reload
```

The API will be available at `http://localhost:8000`

### Start the Frontend Development Server

```bash
cd frontend
npm run dev
```

The frontend will be available at `http://localhost:5173`

### API Documentation

Visit `http://localhost:8000/docs` for interactive API documentation (Swagger UI).

### Two Generation Modes

#### 1. Incremental Mode (Recommended)
Generate mystery components step-by-step with database persistence:

```bash
# 1. Create a new game
GAME_ID=$(curl -X POST http://localhost:8000/games \
  -H "Content-Type: application/json" \
  -d '{"theme": "film noir", "num_players": 6, "difficulty": "medium", "language": "en"}' \
  | jq -r '.id')

# 2. Generate cover image (happens automatically in background)
curl -X POST http://localhost:8000/games/$GAME_ID/image

# 3. Generate characters (portraits generated automatically in background)
curl -X POST http://localhost:8000/games/$GAME_ID/characters

# 4. Generate plot
curl -X POST http://localhost:8000/games/$GAME_ID/plot

# 5. Generate clues
curl -X POST http://localhost:8000/games/$GAME_ID/clues

# 6. Generate metadata
curl -X POST http://localhost:8000/games/$GAME_ID/metadata

# 7. Generate audio narration (optional)
curl -X POST http://localhost:8000/games/$GAME_ID/audio

# 8. Validate scenario
curl -X POST http://localhost:8000/games/$GAME_ID/validate

# 9. Get complete scenario
curl http://localhost:8000/games/$GAME_ID
```

#### 2. Legacy Mode (Single Request)
Generate complete mystery in one API call:

```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "theme": "film noir",
    "num_players": 6,
    "difficulty": "medium",
    "language": "en"
  }'
```

**Parameters:**
- `theme`: Mystery theme (e.g., "film noir", "victorian mansion", "luxury cruise")
- `num_players`: Number of players (3-12)
- `difficulty`: Difficulty level ("easy", "medium", "hard")
- `language`: Content language ("en" or "fr")
- `special_requests` (optional): Any special requests or constraints

## Development

### Running Tests

```bash
# Run all tests
pytest -v

# Run specific test file
pytest tests/test_models.py -v
pytest tests/test_nodes.py -v
pytest tests/test_api.py -v

# Run with coverage
pytest --cov=src tests/
```

### Project Structure

```
mystery-party-game/
├── src/                     # Backend (Python)
│   ├── models/              # Pydantic data models
│   │   ├── schema.py        # Character, Plot, Clue, MysteryScenario
│   │   └── state.py         # LangGraph state definition
│   ├── database/            # SQLAlchemy models and database
│   │   ├── models.py        # DB models (Game, Character, etc.)
│   │   └── base.py          # Database configuration
│   ├── services/            # Database CRUD operations
│   │   ├── game_service.py
│   │   ├── character_service.py
│   │   ├── plot_service.py
│   │   ├── clue_service.py
│   │   ├── metadata_service.py
│   │   ├── validation_service.py
│   │   ├── audio_service.py
│   │   └── image_service.py
│   ├── graph/
│   │   ├── nodes/           # Individual workflow nodes
│   │   │   ├── characters.py
│   │   │   ├── plot.py
│   │   │   ├── clues.py
│   │   │   ├── metadata.py
│   │   │   └── validation.py
│   │   └── workflow.py      # LangGraph orchestration
│   ├── api/
│   │   ├── main.py          # FastAPI application
│   │   └── routers/         # API routers
│   │       ├── games.py     # CRUD endpoints
│   │       ├── generation.py # Generation endpoints
│   │       ├── images.py    # Image endpoints
│   │       └── audio.py     # Audio endpoints
│   └── config/
│       └── settings.py      # Configuration management
├── frontend/                # Frontend (React + TypeScript)
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── pages/           # Page components
│   │   ├── services/        # API client
│   │   ├── contexts/        # React contexts (theme)
│   │   └── locales/         # i18n translations
│   ├── public/              # Static assets
│   └── package.json
├── alembic/                 # Database migrations
├── tests/                   # Unit tests (66 tests)
├── images/                  # Generated images
├── audio/                   # Generated audio files
├── requirements.txt
└── .env.example
```

## Architecture

### Backend Architecture

- **LangGraph**: Orchestrates the mystery generation workflow with 5 nodes
- **LangChain + Anthropic**: Claude AI for content generation and prompt sanitization
- **FastAPI**: RESTful API with incremental generation endpoints
- **SQLAlchemy**: Database layer for persistent storage
- **Alembic**: Database migrations
- **OpenAI DALL-E 2**: Character portraits and cover image generation
- **OpenAI TTS**: Audio narration generation

### LangGraph Workflow

The mystery generation follows a sequential workflow:

1. **Character Generation**: Creates diverse characters based on theme and player count
2. **Plot Generation**: Develops the main storyline, victim, and culprit
3. **Clues Generation**: Creates evidence and red herrings
4. **Metadata Generation**: Adds title, instructions, and introduction
5. **Validation**: Ensures all components are coherent

If validation fails, the workflow can retry up to 2 times.

### Image Generation

**Cover Images:**
- Generated immediately after game creation
- Uses theme to create atmospheric cover art
- Claude AI sanitizes prompts to avoid DALL-E content policy violations

**Character Portraits:**
- Generated in background after character creation
- Uses character name, role, personality, and game theme
- Ultra-safe prompt sanitization to ensure DALL-E compliance
- 512x512 images optimized for character cards

**Prompt Sanitization:**
All prompts are processed through Claude AI to:
- Remove sensitive words (crime, violence, weapons, death, etc.)
- Focus on neutral visual elements (clothing, expression, lighting, artistic style)
- Keep mysterious atmosphere while making content policy-safe
- Limit to concise descriptions (max 15 words for portraits)

### Frontend Architecture

- **React + TypeScript**: Modern component-based UI
- **Tailwind CSS**: Utility-first styling with custom theme
- **i18next**: Internationalization for English and French
- **React Router**: Client-side routing
- **Vite**: Fast development and build tooling

**Key Features:**
- Dark/Light theme toggle with localStorage persistence
- Language switcher (EN/FR) with automatic browser detection
- Incremental wizard for game generation with progress tracking
- Responsive design for desktop and mobile

## Configuration

Environment variables (`.env`):

```bash
# Required
ANTHROPIC_API_KEY=your_anthropic_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

# Optional
LLM_MODEL=claude-sonnet-4-5-20250929
LLM_TEMPERATURE=0.7
API_HOST=0.0.0.0
API_PORT=8000
DATABASE_URL=sqlite:///./mystery_party.db
DEBUG=False
```

## Testing

The project includes comprehensive unit tests:
- **Database models**: SQLAlchemy models and relationships (9 tests)
- **Services layer**: CRUD operations for all entities (20 tests)
- **API endpoints**: Incremental and legacy generation (19 tests)
- **Migrations**: Alembic migration integrity (6 tests)
- **Graph nodes**: LangGraph workflow nodes (7 tests)
- **Pydantic models**: Data validation (5 tests)

**Total: 66 tests** - All passing ✅

## License

[Your License Here]

## Contributing

[Your Contributing Guidelines Here]
