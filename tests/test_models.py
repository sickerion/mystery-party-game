"""Unit tests for data models."""

import pytest
from src.models import (
    Character,
    Clue,
    Plot,
    MysteryScenario,
    GameRequest,
    DifficultyLevel,
)


def test_character_creation():
    """Test creating a Character instance."""
    character = Character(
        name="Detective Smith",
        role="Private Investigator",
        background="Former police officer with 20 years experience",
        personality="Analytical, methodical, slightly cynical",
        secret="Has a gambling debt",
        motive="Needs money to pay off debt",
        relationship_to_victim="Former colleague"
    )
    assert character.name == "Detective Smith"
    assert character.role == "Private Investigator"


def test_clue_creation():
    """Test creating a Clue instance."""
    clue = Clue(
        clue_id="clue_001",
        description="A bloody knife found under the couch",
        location="Living room",
        revealed_by="Detective Smith",
        significance="Murder weapon",
        misleading=False
    )
    assert clue.clue_id == "clue_001"
    assert clue.misleading is False


def test_plot_creation():
    """Test creating a Plot instance."""
    plot = Plot(
        setting="Victorian mansion, 1895",
        victim="Lord Blackwood",
        crime="Murder by poisoning",
        culprit="Lady Blackwood",
        murder_method="Arsenic in the evening tea",
        timeline=[
            "5:00 PM - Tea served",
            "5:30 PM - Victim collapses",
            "6:00 PM - Doctor declares death"
        ],
        resolution="The poison was traced to Lady Blackwood's private collection"
    )
    assert plot.victim == "Lord Blackwood"
    assert len(plot.timeline) == 3


def test_game_request_validation():
    """Test GameRequest validation."""
    request = GameRequest(
        theme="film noir",
        num_players=6,
        difficulty=DifficultyLevel.MEDIUM
    )
    assert request.num_players == 6
    assert request.difficulty == DifficultyLevel.MEDIUM

    # Test that num_players must be between 3 and 12
    with pytest.raises(Exception):
        GameRequest(theme="test", num_players=2, difficulty=DifficultyLevel.EASY)


def test_difficulty_enum():
    """Test DifficultyLevel enum."""
    assert DifficultyLevel.EASY == "easy"
    assert DifficultyLevel.MEDIUM == "medium"
    assert DifficultyLevel.HARD == "hard"
