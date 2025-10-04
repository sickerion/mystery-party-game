# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Mystery Party Game Generator - AI-powered application that generates complete murder mystery party game scenarios using LangGraph and Anthropic Claude.

## Architecture

### Backend (Python)
- **LangGraph**: Orchestrates the mystery generation workflow with 5 nodes
- **LangChain + Anthropic**: LLM integration for content generation
- **FastAPI**: REST API for serving mystery generation requests
- **Pydantic**: Data validation and settings management

### Workflow Nodes
1. **Character Generation** (`src/graph/nodes/characters.py`): Creates diverse characters with backgrounds and secrets
2. **Plot Generation** (`src/graph/nodes/plot.py`): Generates main storyline, victim, culprit, and method
3. **Clues Generation** (`src/graph/nodes/clues.py`): Creates clues and red herrings
4. **Metadata Generation** (`src/graph/nodes/metadata.py`): Generates title, instructions, and introduction
5. **Validation** (`src/graph/nodes/validation.py`): Validates scenario coherence

### Project Structure
```
src/
├── models/          # Pydantic data models (Character, Plot, Clue, etc.)
├── graph/
│   ├── nodes/       # Individual LangGraph nodes
│   └── workflow.py  # Graph definition and orchestration
├── api/             # FastAPI endpoints
└── config/          # Settings and configuration

tests/               # Unit tests for all modules
```

## Development Commands

### Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

### Development
```bash
# Run tests
pytest -v

# Run API server
uvicorn src.api.main:app --reload

# Check specific tests
pytest tests/test_models.py -v
pytest tests/test_nodes.py -v
pytest tests/test_api.py -v
```

### API Usage
```bash
# Health check
curl http://localhost:8000/health

# Generate mystery
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"theme": "film noir", "num_players": 6, "difficulty": "medium"}'
```

## Testing Guidelines

- Write unit tests for every file with logic
- Run all tests after each change: `pytest -v`
- Verify compilation after each step: `python -m py_compile <file>`
- Current test coverage: 17 tests across models, nodes, graph, and API

## Configuration

Environment variables (`.env`):
- `ANTHROPIC_API_KEY`: Your Anthropic API key (required)
- `LLM_MODEL`: Model to use (default: claude-3-5-sonnet-20241022)
- `LLM_TEMPERATURE`: Temperature for generation (default: 0.7)
- `API_HOST`: API host (default: 0.0.0.0)
- `API_PORT`: API port (default: 8000)

## Key Design Decisions

- **Separate node files**: Each LangGraph node has its own file for maintainability
- **State-based workflow**: Uses TypedDict for state management through the graph
- **Validation with retry**: Can retry generation if validation fails (max 2 iterations)
- **Type safety**: Pydantic models ensure data validation throughout


