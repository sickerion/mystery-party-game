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
- **LangChain + Anthropic**: LLM integration for content generation
- **FastAPI**: REST API with incremental generation endpoints
- **SQLAlchemy**: Database layer for persistent storage
- **Alembic**: Database migrations
- **Pydantic**: Data validation and settings management

### Two API Modes

#### 1. Legacy Mode - Single Request (POST /generate)
Complete mystery generation in one API call using LangGraph workflow.

#### 2. Incremental Mode - Step-by-Step (NEW)
Generate mystery components incrementally with database persistence:
1. POST `/games` - Create game
2. POST `/games/{id}/characters` - Generate characters
3. POST `/games/{id}/plot` - Generate plot
4. POST `/games/{id}/clues` - Generate clues
5. POST `/games/{id}/metadata` - Generate metadata
6. POST `/games/{id}/validate` - Validate scenario
7. GET `/games/{id}` - Retrieve complete scenario

### Workflow Nodes
1. **Character Generation** (`src/graph/nodes/characters.py`): Creates diverse characters with backgrounds and secrets
2. **Plot Generation** (`src/graph/nodes/plot.py`): Generates main storyline, victim, culprit, and method
3. **Clues Generation** (`src/graph/nodes/clues.py`): Creates clues and red herrings
4. **Metadata Generation** (`src/graph/nodes/metadata.py`): Generates title, instructions, and introduction
5. **Validation** (`src/graph/nodes/validation.py`): Validates scenario coherence

### Database Schema

**Tables:**
- `games` - Main game state (id, theme, num_players, difficulty, status, timestamps)
- `generated_characters` - Character data linked to games
- `generated_plots` - Plot details with JSON timeline
- `generated_clues` - Clues with misleading flag
- `generated_metadata` - Game metadata (title, instructions, introduction)
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
│   └── validation_service.py
├── graph/
│   ├── nodes/       # Individual LangGraph nodes
│   └── workflow.py  # Graph definition and orchestration
├── api/
│   ├── main.py      # FastAPI app
│   └── routers/     # API routers
│       ├── games.py      # CRUD endpoints
│       └── generation.py # Generation endpoints
└── config/          # Settings and configuration

alembic/             # Database migrations
tests/               # Comprehensive test suite (66 tests)
```

## Development Commands

### Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY

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
  -d '{"theme": "film noir", "num_players": 6, "difficulty": "medium"}' \
  | jq -r '.id')

# 2. Generate characters
curl -X POST http://localhost:8000/games/$GAME_ID/characters

# 3. Generate plot
curl -X POST http://localhost:8000/games/$GAME_ID/plot

# 4. Generate clues
curl -X POST http://localhost:8000/games/$GAME_ID/clues

# 5. Generate metadata (title, instructions, introduction)
curl -X POST http://localhost:8000/games/$GAME_ID/metadata

# 6. Validate the complete scenario
curl -X POST http://localhost:8000/games/$GAME_ID/validate

# 7. Get complete scenario
curl http://localhost:8000/games/$GAME_ID

# List all games with filtering
curl "http://localhost:8000/games?status=validated&limit=10"

# Delete a game
curl -X DELETE http://localhost:8000/games/$GAME_ID
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
- `ANTHROPIC_API_KEY`: Your Anthropic API key (required)
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
- **Cascade deletes**: Deleting a game automatically removes all related data
- **Status tracking**: Game status tracks progress through generation pipeline


