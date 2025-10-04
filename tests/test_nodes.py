"""Unit tests for individual graph nodes."""

import pytest
from src.graph.nodes.validation import validate_scenario_node
from src.models.state import MysteryGenerationState
from src.models.schema import Character, Plot, Clue, DifficultyLevel


def test_validate_scenario_node_success():
    """Test validation node with valid scenario."""
    state: MysteryGenerationState = {
        "theme": "film noir",
        "num_players": 3,
        "difficulty": DifficultyLevel.MEDIUM,
        "special_requests": None,
        "characters": [
            Character(
                name="Detective Smith",
                role="Detective",
                background="Experienced investigator",
                personality="Sharp and analytical",
                secret="Has gambling debts"
            ),
            Character(
                name="Lady Blackwood",
                role="Aristocrat",
                background="Wealthy widow",
                personality="Cold and calculating",
                secret="Poisoner"
            ),
            Character(
                name="Dr. Watson",
                role="Doctor",
                background="Family physician",
                personality="Loyal and honest",
                secret="Witnessed the crime"
            ),
        ],
        "plot": Plot(
            setting="Victorian mansion, 1895",
            victim="Detective Smith",
            crime="Murder by poisoning",
            culprit="Lady Blackwood",
            murder_method="Arsenic in tea",
            timeline=["5:00 PM - Tea time", "6:00 PM - Death"],
            resolution="Found poison in Lady's room"
        ),
        "clues": [
            Clue(
                clue_id="clue_001",
                description="Poison bottle",
                location="Lady's room",
                significance="Murder weapon",
                misleading=False
            ),
            Clue(
                clue_id="clue_002",
                description="Teacup",
                location="Library",
                significance="Delivery method",
                misleading=False
            ),
            Clue(
                clue_id="clue_003",
                description="Red herring note",
                location="Study",
                significance="Distraction",
                misleading=True
            ),
        ],
        "title": "Mystery at Blackwood Manor",
        "estimated_duration": 120,
        "game_instructions": "Instructions here",
        "introduction": "Welcome to the mystery",
        "validation_passed": False,
        "validation_errors": None,
        "iteration_count": 0,
    }

    result = validate_scenario_node(state)

    assert result["validation_passed"] is True
    assert result["validation_errors"] is None


def test_validate_scenario_node_missing_characters():
    """Test validation node with missing characters."""
    state: MysteryGenerationState = {
        "theme": "film noir",
        "num_players": 3,
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

    result = validate_scenario_node(state)

    assert result["validation_passed"] is False
    assert result["validation_errors"] is not None
    assert "No characters generated" in result["validation_errors"]


def test_validate_scenario_node_wrong_character_count():
    """Test validation node with wrong number of characters."""
    state: MysteryGenerationState = {
        "theme": "film noir",
        "num_players": 5,
        "difficulty": DifficultyLevel.MEDIUM,
        "special_requests": None,
        "characters": [
            Character(
                name="Detective Smith",
                role="Detective",
                background="Investigator",
                personality="Sharp",
                secret="Secret"
            ),
        ],
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

    result = validate_scenario_node(state)

    assert result["validation_passed"] is False
    assert "Expected 5 characters, got 1" in result["validation_errors"]


def test_validate_scenario_node_invalid_victim():
    """Test validation node with victim not in character list."""
    state: MysteryGenerationState = {
        "theme": "film noir",
        "num_players": 2,
        "difficulty": DifficultyLevel.MEDIUM,
        "special_requests": None,
        "characters": [
            Character(
                name="Detective Smith",
                role="Detective",
                background="Investigator",
                personality="Sharp",
                secret="Secret"
            ),
            Character(
                name="Lady Blackwood",
                role="Aristocrat",
                background="Wealthy",
                personality="Cold",
                secret="Killer"
            ),
        ],
        "plot": Plot(
            setting="Mansion",
            victim="Unknown Person",
            crime="Murder",
            culprit="Lady Blackwood",
            murder_method="Poison",
            timeline=["Event 1"],
            resolution="Solved"
        ),
        "clues": [
            Clue(
                clue_id="clue_001",
                description="Evidence",
                location="Room",
                significance="Important",
                misleading=False
            ),
            Clue(
                clue_id="clue_002",
                description="More evidence",
                location="Hall",
                significance="Key",
                misleading=False
            ),
            Clue(
                clue_id="clue_003",
                description="Red herring",
                location="Garden",
                significance="Distraction",
                misleading=True
            ),
        ],
        "title": "Mystery",
        "estimated_duration": 90,
        "game_instructions": "Instructions",
        "introduction": "Intro",
        "validation_passed": False,
        "validation_errors": None,
        "iteration_count": 0,
    }

    result = validate_scenario_node(state)

    assert result["validation_passed"] is False
    assert "Victim 'Unknown Person' is not in character list" in result["validation_errors"]


def test_validate_scenario_node_too_few_clues():
    """Test validation node with insufficient clues."""
    state: MysteryGenerationState = {
        "theme": "film noir",
        "num_players": 2,
        "difficulty": DifficultyLevel.MEDIUM,
        "special_requests": None,
        "characters": [
            Character(
                name="Detective Smith",
                role="Detective",
                background="Investigator",
                personality="Sharp",
                secret="Secret"
            ),
            Character(
                name="Lady Blackwood",
                role="Aristocrat",
                background="Wealthy",
                personality="Cold",
                secret="Killer"
            ),
        ],
        "plot": Plot(
            setting="Mansion",
            victim="Detective Smith",
            crime="Murder",
            culprit="Lady Blackwood",
            murder_method="Poison",
            timeline=["Event 1"],
            resolution="Solved"
        ),
        "clues": [
            Clue(
                clue_id="clue_001",
                description="Evidence",
                location="Room",
                significance="Important",
                misleading=False
            ),
        ],
        "title": "Mystery",
        "estimated_duration": 90,
        "game_instructions": "Instructions",
        "introduction": "Intro",
        "validation_passed": False,
        "validation_errors": None,
        "iteration_count": 0,
    }

    result = validate_scenario_node(state)

    assert result["validation_passed"] is False
    assert "Too few clues generated" in result["validation_errors"]
