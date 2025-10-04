"""Tests for database services."""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.base import Base
from src.database.models import GameStatus
from src.models.schema import Character, Plot, Clue
from src.services import game_service, character_service, plot_service, clue_service, metadata_service, validation_service
import tempfile
import os


@pytest.fixture
def db_session():
    """Create a temporary database for testing."""
    fd, db_path = tempfile.mkstemp(suffix=".db")
    os.close(fd)

    db_url = f"sqlite:///{db_path}"
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    yield session

    session.close()
    engine.dispose()
    try:
        os.remove(db_path)
    except:
        pass


# Game Service Tests
def test_create_game(db_session):
    """Test creating a game."""
    game = game_service.create_game(
        db_session,
        theme="film noir",
        num_players=6,
        difficulty="medium",
        special_requests="Include detective",
    )

    assert game.id is not None
    assert game.theme == "film noir"
    assert game.num_players == 6
    assert game.difficulty == "medium"
    assert game.status == GameStatus.INITIALIZED


def test_get_game(db_session):
    """Test getting a game by ID."""
    game = game_service.create_game(db_session, "test", 4, "easy")
    retrieved = game_service.get_game(db_session, game.id)

    assert retrieved is not None
    assert retrieved.id == game.id
    assert retrieved.theme == "test"


def test_update_game_status(db_session):
    """Test updating game status."""
    game = game_service.create_game(db_session, "test", 4, "easy")
    updated = game_service.update_game_status(db_session, game.id, GameStatus.CHARACTERS_GENERATED)

    assert updated is not None
    assert updated.status == GameStatus.CHARACTERS_GENERATED


def test_list_games(db_session):
    """Test listing games."""
    game_service.create_game(db_session, "test1", 4, "easy")
    game_service.create_game(db_session, "test2", 6, "medium")

    games = game_service.list_games(db_session, limit=10)
    assert len(games) == 2


def test_list_games_with_status_filter(db_session):
    """Test listing games with status filter."""
    game1 = game_service.create_game(db_session, "test1", 4, "easy")
    game2 = game_service.create_game(db_session, "test2", 6, "medium")
    game_service.update_game_status(db_session, game1.id, GameStatus.COMPLETED)

    completed_games = game_service.list_games(db_session, status=GameStatus.COMPLETED)
    assert len(completed_games) == 1
    assert completed_games[0].id == game1.id


def test_delete_game(db_session):
    """Test deleting a game."""
    game = game_service.create_game(db_session, "test", 4, "easy")
    result = game_service.delete_game(db_session, game.id)

    assert result is True
    assert game_service.get_game(db_session, game.id) is None


# Character Service Tests
def test_save_characters(db_session):
    """Test saving characters."""
    game = game_service.create_game(db_session, "test", 4, "easy")
    characters = [
        Character(
            name="Detective Smith",
            role="Detective",
            background="Ex-cop",
            personality="Analytical",
            secret="Hidden past",
        ),
        Character(
            name="Lady Ashford",
            role="Aristocrat",
            background="Wealthy",
            personality="Cunning",
            secret="Gambling debts",
        ),
    ]

    saved = character_service.save_characters(db_session, game.id, characters)

    assert len(saved) == 2
    assert saved[0].name == "Detective Smith"
    assert saved[1].name == "Lady Ashford"


def test_get_characters_by_game(db_session):
    """Test getting characters by game."""
    game = game_service.create_game(db_session, "test", 4, "easy")
    characters = [
        Character(
            name="Test Char",
            role="Role",
            background="BG",
            personality="Pers",
            secret="Secret",
        )
    ]
    character_service.save_characters(db_session, game.id, characters)

    retrieved = character_service.get_characters_by_game(db_session, game.id)
    assert len(retrieved) == 1
    assert retrieved[0].name == "Test Char"


# Plot Service Tests
def test_save_plot(db_session):
    """Test saving a plot."""
    game = game_service.create_game(db_session, "test", 4, "easy")
    plot = Plot(
        setting="Mansion, 1920s",
        victim="Lord Blackwood",
        crime="Murder",
        culprit="Butler",
        murder_method="Poison",
        timeline=["Event 1", "Event 2"],
        resolution="Detective solves",
    )

    saved = plot_service.save_plot(db_session, game.id, plot)

    assert saved.victim == "Lord Blackwood"
    assert saved.culprit == "Butler"
    assert len(saved.timeline) == 2


def test_get_plot_by_game(db_session):
    """Test getting plot by game."""
    game = game_service.create_game(db_session, "test", 4, "easy")
    plot = Plot(
        setting="Test",
        victim="Victim",
        crime="Crime",
        culprit="Culprit",
        murder_method="Method",
        timeline=["T1"],
        resolution="Res",
    )
    plot_service.save_plot(db_session, game.id, plot)

    retrieved = plot_service.get_plot_by_game(db_session, game.id)
    assert retrieved is not None
    assert retrieved.victim == "Victim"


def test_update_existing_plot(db_session):
    """Test updating an existing plot."""
    game = game_service.create_game(db_session, "test", 4, "easy")
    plot1 = Plot(
        setting="Setting1",
        victim="Victim1",
        crime="Crime1",
        culprit="Culprit1",
        murder_method="Method1",
        timeline=["T1"],
        resolution="Res1",
    )
    plot_service.save_plot(db_session, game.id, plot1)

    plot2 = Plot(
        setting="Setting2",
        victim="Victim2",
        crime="Crime2",
        culprit="Culprit2",
        murder_method="Method2",
        timeline=["T2"],
        resolution="Res2",
    )
    plot_service.save_plot(db_session, game.id, plot2)

    retrieved = plot_service.get_plot_by_game(db_session, game.id)
    assert retrieved.victim == "Victim2"  # Should be updated, not created new


# Clue Service Tests
def test_save_clues(db_session):
    """Test saving clues."""
    game = game_service.create_game(db_session, "test", 4, "easy")
    clues = [
        Clue(
            clue_id="C1",
            description="Bloody knife",
            location="Kitchen",
            significance="Murder weapon",
            misleading=False,
        ),
        Clue(
            clue_id="C2",
            description="Red herring",
            location="Study",
            significance="Distraction",
            misleading=True,
        ),
    ]

    saved = clue_service.save_clues(db_session, game.id, clues)

    assert len(saved) == 2
    assert saved[0].clue_id == "C1"
    assert saved[1].misleading is True


def test_get_clues_by_game(db_session):
    """Test getting clues by game."""
    game = game_service.create_game(db_session, "test", 4, "easy")
    clues = [
        Clue(
            clue_id="C1",
            description="Test clue",
            location="Location",
            significance="Sig",
            misleading=False,
        )
    ]
    clue_service.save_clues(db_session, game.id, clues)

    retrieved = clue_service.get_clues_by_game(db_session, game.id)
    assert len(retrieved) == 1
    assert retrieved[0].clue_id == "C1"


# Metadata Service Tests
def test_save_metadata(db_session):
    """Test saving metadata."""
    game = game_service.create_game(db_session, "test", 4, "easy")

    saved = metadata_service.save_metadata(
        db_session,
        game.id,
        title="Murder at the Mansion",
        estimated_duration=120,
        game_instructions="Instructions here",
        introduction="Intro text",
    )

    assert saved.title == "Murder at the Mansion"
    assert saved.estimated_duration == 120


def test_get_metadata_by_game(db_session):
    """Test getting metadata by game."""
    game = game_service.create_game(db_session, "test", 4, "easy")
    metadata_service.save_metadata(
        db_session, game.id, "Title", 90, "Instructions", "Intro"
    )

    retrieved = metadata_service.get_metadata_by_game(db_session, game.id)
    assert retrieved is not None
    assert retrieved.title == "Title"


def test_update_existing_metadata(db_session):
    """Test updating existing metadata."""
    game = game_service.create_game(db_session, "test", 4, "easy")
    metadata_service.save_metadata(
        db_session, game.id, "Title1", 90, "Instructions1", "Intro1"
    )
    metadata_service.save_metadata(
        db_session, game.id, "Title2", 120, "Instructions2", "Intro2"
    )

    retrieved = metadata_service.get_metadata_by_game(db_session, game.id)
    assert retrieved.title == "Title2"  # Should be updated


# Validation Service Tests
def test_save_validation(db_session):
    """Test saving validation result."""
    game = game_service.create_game(db_session, "test", 4, "easy")

    saved = validation_service.save_validation(
        db_session,
        game.id,
        iteration=1,
        validation_passed=True,
        validation_errors=None,
    )

    assert saved.iteration == 1
    assert saved.validation_passed is True


def test_get_validations_by_game(db_session):
    """Test getting validations by game."""
    game = game_service.create_game(db_session, "test", 4, "easy")
    validation_service.save_validation(db_session, game.id, 1, False, ["Error 1"])
    validation_service.save_validation(db_session, game.id, 2, True, None)

    validations = validation_service.get_validations_by_game(db_session, game.id)
    assert len(validations) == 2
    assert validations[0].iteration == 1
    assert validations[1].iteration == 2


def test_get_latest_validation(db_session):
    """Test getting latest validation."""
    game = game_service.create_game(db_session, "test", 4, "easy")
    validation_service.save_validation(db_session, game.id, 1, False, ["Error"])
    validation_service.save_validation(db_session, game.id, 2, True, None)

    latest = validation_service.get_latest_validation(db_session, game.id)
    assert latest is not None
    assert latest.iteration == 2
    assert latest.validation_passed is True


# Cascade Delete Test
def test_cascade_delete_all_related_data(db_session):
    """Test that deleting a game cascades to all related data."""
    game = game_service.create_game(db_session, "test", 4, "easy")

    # Add related data
    characters = [
        Character(name="C1", role="R", background="B", personality="P", secret="S")
    ]
    character_service.save_characters(db_session, game.id, characters)

    plot = Plot(
        setting="S", victim="V", crime="C", culprit="Cu",
        murder_method="M", timeline=["T"], resolution="R"
    )
    plot_service.save_plot(db_session, game.id, plot)

    clues = [Clue(clue_id="CL1", description="D", location="L", significance="S", misleading=False)]
    clue_service.save_clues(db_session, game.id, clues)

    metadata_service.save_metadata(db_session, game.id, "T", 90, "I", "In")
    validation_service.save_validation(db_session, game.id, 1, True, None)

    # Delete game
    game_service.delete_game(db_session, game.id)

    # Verify all related data is deleted
    assert len(character_service.get_characters_by_game(db_session, game.id)) == 0
    assert plot_service.get_plot_by_game(db_session, game.id) is None
    assert len(clue_service.get_clues_by_game(db_session, game.id)) == 0
    assert metadata_service.get_metadata_by_game(db_session, game.id) is None
    assert len(validation_service.get_validations_by_game(db_session, game.id)) == 0
