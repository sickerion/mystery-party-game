# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Mystery Party Game Generator - AI-powered application that generates complete murder mystery party game scenarios using LangGraph and Anthropic Claude.

## Instructions
- Divide the code correctly (ex: one file per model not all models in the same file)
- Always commit and push after finishing a task
- Write tests for implemented logics
- Keep track of your progress in TASK.md
- Add translations when adding texts in ui

## Architecture

### Backend (Python)
- **LangGraph**: Orchestrates the mystery generation workflow with 5 nodes
- **LangChain + Anthropic**: LLM integration for content generation and prompt sanitization
- **FastAPI**: REST API with incremental generation endpoints
- **SQLAlchemy**: Database layer for persistent storage
- **Alembic**: Database migrations
- **Pydantic**: Data validation and settings management
- **OpenAI DALL-E 2**: Character portraits and cover image generation
- **OpenAI TTS**: Audio narration generation

### Two API Modes

#### 1. Legacy Mode - Single Request (POST /generate)
Complete mystery generation in one API call using LangGraph workflow.

#### 2. Incremental Mode - Step-by-Step (NEW)
Generate mystery components incrementally with database persistence:
1. POST `/games` - Create game
2. POST `/games/{id}/image` - Generate cover image (uses theme only)
3. POST `/games/{id}/characters` - Generate characters (portraits auto-generated in background)
4. POST `/games/{id}/plot` - Generate plot
5. POST `/games/{id}/clues` - Generate clues
6. POST `/games/{id}/metadata` - Generate metadata
7. POST `/games/{id}/audio` - Generate audio narration (optional)
8. POST `/games/{id}/validate` - Validate scenario
9. GET `/games/{id}` - Retrieve complete scenario

### Workflow Nodes
1. **Character Generation** (`src/graph/nodes/characters.py`): Creates diverse characters with backgrounds and secrets
2. **Plot Generation** (`src/graph/nodes/plot.py`): Generates main storyline, victim, culprit, and method
3. **Clues Generation** (`src/graph/nodes/clues.py`): Creates clues and red herrings
4. **Metadata Generation** (`src/graph/nodes/metadata.py`): Generates title, instructions, and introduction
5. **Validation** (`src/graph/nodes/validation.py`): Validates scenario coherence

### Database Schema

**Tables:**
- `games` - Main game state (id, theme, num_players, difficulty, language, status, cover_image_path, timestamps)
- `generated_characters` - Character data linked to games (includes character_image_path)
- `generated_plots` - Plot details with JSON timeline
- `generated_clues` - Clues with misleading flag
- `generated_metadata` - Game metadata (title, instructions, introduction, audio paths)
- `validation_results` - Validation history with iteration tracking

**Game Status Flow:**
```
initialized → characters_generated → plot_generated →
clues_generated → metadata_generated → validated/failed
```

### Project Structure
```
src/
├── models/          # Pydantic data models (Character, Plot, Clue, etc.)
├── database/        # SQLAlchemy models and database setup
│   ├── models.py    # DB models (Game, GeneratedCharacter, etc.)
│   └── base.py      # Database configuration
├── services/        # Database CRUD operations
│   ├── game_service.py
│   ├── character_service.py
│   ├── plot_service.py
│   ├── clue_service.py
│   ├── metadata_service.py
│   ├── validation_service.py
│   ├── audio_service.py
│   └── image_service.py
├── graph/
│   ├── nodes/       # Individual LangGraph nodes
│   └── workflow.py  # Graph definition and orchestration
├── api/
│   ├── main.py      # FastAPI app
│   └── routers/     # API routers
│       ├── games.py      # CRUD endpoints
│       ├── generation.py # Generation endpoints (includes background task for character portraits)
│       ├── images.py     # Image generation endpoints
│       └── audio.py      # Audio generation endpoints
└── config/          # Settings and configuration

alembic/             # Database migrations
audio/               # Generated MP3 audio files (gitignored)
images/              # Generated cover images and character portraits (gitignored)
tests/               # Comprehensive test suite (66 tests)
```

## Development Commands

### Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your API keys:
# - ANTHROPIC_API_KEY (required for content generation)
# - OPENAI_API_KEY (required for images and audio)

# Run database migrations
alembic upgrade head
```

### Development
```bash
# Run all tests (66 tests)
pytest -v

# Run specific test suites
pytest tests/test_database_models.py -v  # Database models (9 tests)
pytest tests/test_services.py -v         # Services layer (20 tests)
pytest tests/test_api_incremental.py -v  # Incremental API (14 tests)
pytest tests/test_alembic_migrations.py -v  # Migrations (6 tests)

# Run API server
uvicorn src.api.main:app --reload

# Create new migration after model changes
alembic revision --autogenerate -m "Description of changes"
alembic upgrade head
```

### API Usage

#### Legacy Mode (Single Request)
```bash
# Health check
curl http://localhost:8000/health

# Generate complete mystery in one call
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"theme": "film noir", "num_players": 6, "difficulty": "medium"}'
```

#### Incremental Mode (Step-by-Step)
```bash
# 1. Create a new game
GAME_ID=$(curl -X POST http://localhost:8000/games \
  -H "Content-Type: application/json" \
  -d '{"theme": "film noir", "num_players": 6, "difficulty": "medium", "language": "en"}' \
  | jq -r '.id')

# 2. Generate cover image (uses theme only)
curl -X POST http://localhost:8000/games/$GAME_ID/image

# 3. Generate characters (character portraits generated automatically in background)
curl -X POST http://localhost:8000/games/$GAME_ID/characters

# 4. Generate plot
curl -X POST http://localhost:8000/games/$GAME_ID/plot

# 5. Generate clues
curl -X POST http://localhost:8000/games/$GAME_ID/clues

# 6. Generate metadata (title, instructions, introduction)
curl -X POST http://localhost:8000/games/$GAME_ID/metadata

# 7. Generate audio files for introduction and instructions (optional)
curl -X POST http://localhost:8000/games/$GAME_ID/metadata/audio

# 8. Validate the complete scenario
curl -X POST http://localhost:8000/games/$GAME_ID/validate

# 9. Get complete scenario
curl http://localhost:8000/games/$GAME_ID

# Get cover image
curl http://localhost:8000/images/$GAME_ID/cover > cover.png

# Get character portrait (requires character_id)
curl http://localhost:8000/images/$GAME_ID/characters/1 > character_1.png

# Get audio files
curl http://localhost:8000/games/$GAME_ID/audio/introduction > introduction.mp3
curl http://localhost:8000/games/$GAME_ID/audio/instructions > instructions.mp3

# List all games with filtering
curl "http://localhost:8000/games?status=validated&limit=10"

# Delete a game (also deletes all associated images and audio)
curl -X DELETE http://localhost:8000/games/$GAME_ID
```

### Image Generation (DALL-E 2)

The application generates AI-powered images using OpenAI's DALL-E 2 API.

**Cover Images:**
- Generated immediately after game creation
- Uses game theme to create atmospheric mystery cover art
- 512x512 PNG images saved to `images/` directory
- Claude AI sanitizes prompts to avoid DALL-E content policy violations

**Character Portraits:**
- Generated automatically in background after character creation
- Uses character name, role, personality, and game theme
- 512x512 PNG images optimized for character cards
- Ultra-safe prompt sanitization to ensure DALL-E compliance

**Prompt Sanitization Strategy:**
All prompts are pre-processed through Claude AI to:
- Remove ALL sensitive words (crime, violence, weapons, death, murder, etc.)
- Replace problematic terms with neutral visual descriptions
- Focus ONLY on visual elements: clothing, facial expression, lighting, artistic style
- Keep mysterious atmosphere while making content policy-safe
- Limit character portrait descriptions to max 15 words

**API Endpoints:**
- POST `/games/{id}/image` - Generate cover image
- GET `/images/{id}/cover` - Serve cover image
- GET `/images/{id}/characters/{character_id}` - Serve character portrait

**Background Task Implementation:**
Character portraits are generated using FastAPI's `BackgroundTasks` to avoid blocking the API response. Images are generated server-side after characters are saved to the database, and the frontend can retry loading images that are still being generated.

**Setup:**
1. Add `OPENAI_API_KEY` to your `.env` file

### Audio Generation (Text-to-Speech)

The application supports generating audio versions of the introduction and instructions using OpenAI's TTS API.

**Features:**
- Generates MP3 files for introduction and instructions
- Language-aware voices (English/French)
- Stores audio files locally in `audio/` directory
- Serves audio via REST API

**API Endpoints:**
- POST `/games/{id}/metadata/audio` - Generate audio files
- GET `/games/{id}/audio/introduction` - Download introduction audio
- GET `/games/{id}/audio/instructions` - Download instructions audio

**Setup:**
1. Add `OPENAI_API_KEY` to your `.env` file
2. Audio files are automatically generated when requested
3. Files are stored in `audio_files/{game_id}_{type}.mp3`

**Frontend:**
- Audio generation button in Game Details page
- HTML5 audio player with controls
- Dark/light mode support
```

## Testing Guidelines

- Write unit tests for every file with logic
- Run all tests after each change: `pytest -v`
- Current test coverage: **66 tests** across all modules:
  - Database models: 9 tests
  - Services layer: 20 tests
  - API endpoints: 14 incremental + 5 legacy tests
  - Migrations: 6 tests
  - Graph/nodes: 7 tests
  - Pydantic models: 5 tests

## Configuration

Environment variables (`.env`):
- `ANTHROPIC_API_KEY`: Your Anthropic API key (required for content generation)
- `OPENAI_API_KEY`: Your OpenAI API key (required for images and audio)
- `LLM_MODEL`: Model to use (default: claude-sonnet-4-5-20250929)
- `LLM_TEMPERATURE`: Temperature for generation (default: 0.7)
- `API_HOST`: API host (default: 0.0.0.0)
- `API_PORT`: API port (default: 8000)
- `DATABASE_URL`: Database connection string (default: sqlite:///./mystery_party.db)
- `DEBUG`: Debug mode for SQLAlchemy (default: False)

## Key Design Decisions

- **Separate node files**: Each LangGraph node has its own file for maintainability
- **State-based workflow**: Uses TypedDict for state management through the graph
- **Validation with retry**: Can retry generation if validation fails (max 2 iterations)
- **Type safety**: Pydantic models ensure data validation throughout
- **Database persistence**: SQLAlchemy with Alembic migrations for incremental generation
- **Service layer**: Clean separation between API, business logic, and data access
- **Cascade deletes**: Deleting a game automatically removes all related data (including images and audio)
- **Status tracking**: Game status tracks progress through generation pipeline
- **Background tasks**: Character portraits generated server-side without blocking API response
- **Prompt sanitization**: Claude AI pre-processes all image prompts to avoid DALL-E content policy violations
- **Image retry mechanism**: Frontend automatically retries loading images that may still be generating
- **Dark/Light Mode**: Theme switching with localStorage persistence
- **Internationalization**: Full i18n support for English and French

## Frontend Features

### Theme System
- **Dark Mode** (default): Navy, teal, and gold color palette
- **Light Mode**: Clean white backgrounds with adjusted contrast
- **ThemeToggle**: Sun/Moon icon button in header
- **Persistence**: Theme preference saved to localStorage
- **Implementation**: Custom ThemeContext with Tailwind dark: classes

### Internationalization (i18n)
- **Languages**: English and French
- **Detection**: Automatic browser language detection
- **Persistence**: Language preference saved to localStorage
- **LanguageSwitcher**: Flag icons (EN/FR) in header
- **Translations**: Complete coverage of UI elements in:
  * Header and navigation
  * Landing page
  * Game details pages
  * Status labels and common actions
- **Date Localization**: Dates formatted according to selected locale


