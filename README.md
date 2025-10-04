# Mystery Party Game Generator

AI-powered mystery party game generator using LangGraph and Anthropic Claude.

Generate complete murder mystery party game scenarios with characters, plots, clues, and game instructions - all powered by AI.

## Features

- 🎭 Generate diverse characters with backgrounds, personalities, and secrets
- 📖 Create compelling murder mystery plots with victims, culprits, and methods
- 🔍 Generate clues and red herrings for investigation
- 🎮 Complete game instructions and atmospheric introductions
- ✅ Automatic validation for scenario coherence
- 🔄 Retry mechanism for quality assurance
- 🚀 RESTful API for easy integration

## Setup

### Prerequisites
- Python 3.11+
- Anthropic API key

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

## Usage

### Start the API Server

```bash
uvicorn src.api.main:app --reload
```

The API will be available at `http://localhost:8000`

### API Documentation

Visit `http://localhost:8000/docs` for interactive API documentation (Swagger UI).

### Generate a Mystery

```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "theme": "film noir",
    "num_players": 6,
    "difficulty": "medium"
  }'
```

**Parameters:**
- `theme`: Mystery theme (e.g., "film noir", "victorian mansion", "luxury cruise")
- `num_players`: Number of players (3-12)
- `difficulty`: Difficulty level ("easy", "medium", "hard")
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
mystery-party-generator/
├── src/
│   ├── models/              # Pydantic data models
│   │   ├── schema.py        # Character, Plot, Clue, MysteryScenario
│   │   └── state.py         # LangGraph state definition
│   ├── graph/
│   │   ├── nodes/           # Individual workflow nodes
│   │   │   ├── characters.py
│   │   │   ├── plot.py
│   │   │   ├── clues.py
│   │   │   ├── metadata.py
│   │   │   └── validation.py
│   │   └── workflow.py      # LangGraph orchestration
│   ├── api/
│   │   └── main.py          # FastAPI application
│   └── config/
│       └── settings.py      # Configuration management
├── tests/                   # Unit tests (17 tests)
├── requirements.txt
└── .env.example
```

## Architecture

### LangGraph Workflow

The mystery generation follows a sequential workflow:

1. **Character Generation**: Creates diverse characters based on theme and player count
2. **Plot Generation**: Develops the main storyline, victim, and culprit
3. **Clues Generation**: Creates evidence and red herrings
4. **Metadata Generation**: Adds title, instructions, and introduction
5. **Validation**: Ensures all components are coherent

If validation fails, the workflow can retry up to 2 times.

## Configuration

Environment variables (`.env`):

```bash
# Required
ANTHROPIC_API_KEY=your_api_key_here

# Optional
LLM_MODEL=claude-sonnet-4-5-20250929
LLM_TEMPERATURE=0.7
API_HOST=0.0.0.0
API_PORT=8000
```

## Testing

The project includes comprehensive unit tests:
- **Models tests**: Pydantic model validation (5 tests)
- **Graph tests**: Workflow creation and state (2 tests)
- **Node tests**: Validation logic (5 tests)
- **API tests**: Endpoint functionality (5 tests)

**Total: 17 tests** - All passing ✅

## License

[Your License Here]

## Contributing

[Your Contributing Guidelines Here]
