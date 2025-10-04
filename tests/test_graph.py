"""Unit tests for LangGraph workflow."""

import pytest
from src.graph.workflow import create_mystery_graph
from src.models.state import MysteryGenerationState
from src.models.schema import DifficultyLevel


def test_create_mystery_graph():
    """Test that the graph can be created."""
    graph = create_mystery_graph()
    assert graph is not None


def test_initial_state():
    """Test creating an initial state."""
    state: MysteryGenerationState = {
        "theme": "film noir",
        "num_players": 6,
        "difficulty": DifficultyLevel.MEDIUM,
        "special_requests": None,
        "characters": None,
        "plot": None,
        "clues": None,
        "title": None,
        "estimated_duration": None,
        "game_instructions": None,
        "introduction": None,
        "validation_passed": False,
        "validation_errors": None,
        "iteration_count": 0,
    }
    assert state["theme"] == "film noir"
    assert state["num_players"] == 6
    assert state["validation_passed"] is False
