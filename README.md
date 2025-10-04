# Mystery Party Game Generator

AI-powered mystery party game generator using LangGraph and Anthropic Claude.

## Setup

### Prerequisites
- Python 3.11+
- Poetry (optional, or use pip with requirements.txt)

### Installation

#### Option 1: Using pip
```bash
pip install -r requirements.txt
```

#### Option 2: Using Poetry
```bash
poetry install
```

### Configuration

1. Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

2. Add your Anthropic API key to `.env`:
```
ANTHROPIC_API_KEY=your_actual_api_key
```

## Development

### Running Tests
```bash
pytest
```

### Starting the API Server
```bash
uvicorn src.api.main:app --reload
```

## Project Structure

```
mystery-party-generator/
├── src/
│   ├── models/          # Pydantic data models
│   ├── graph/           # LangGraph workflow
│   ├── api/             # FastAPI endpoints
│   └── config/          # Configuration management
├── tests/               # Unit tests
├── requirements.txt     # Python dependencies
├── pyproject.toml       # Poetry configuration
└── .env.example         # Environment variables template
```
