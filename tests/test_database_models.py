"""Tests for database models."""

import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.base import Base
from src.database.models import (
    Game,
    GameStatus,
    GeneratedCharacter,
    GeneratedPlot,
    GeneratedClue,
    GeneratedMetadata,
    ValidationResult,
)


@pytest.fixture
def db_session():
    """Create an in-memory SQLite database for testing."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


def test_create_game(db_session):
    """Test creating a Game."""
    game = Game(
        theme="film noir",
        num_players=6,
        difficulty="medium",
        special_requests="Include a detective character",
    )
    db_session.add(game)
    db_session.commit()

    assert game.id is not None
    assert game.theme == "film noir"
    assert game.num_players == 6
    assert game.difficulty == "medium"
    assert game.status == GameStatus.INITIALIZED
    assert isinstance(game.created_at, datetime)
    assert isinstance(game.updated_at, datetime)


def test_create_character(db_session):
    """Test creating a GeneratedCharacter."""
    game = Game(theme="victorian", num_players=4, difficulty="easy")
    db_session.add(game)
    db_session.commit()

    character = GeneratedCharacter(
        game_id=game.id,
        name="Lady Ashford",
        role="Aristocrat",
        background="Wealthy heiress",
        personality="Cunning and manipulative",
        secret="Secret gambling debts",
        motive="Financial gain",
        relationship_to_victim="Former business partner",
    )
    db_session.add(character)
    db_session.commit()

    assert character.id is not None
    assert character.game_id == game.id
    assert character.name == "Lady Ashford"
    assert character.game == game


def test_create_plot(db_session):
    """Test creating a GeneratedPlot."""
    game = Game(theme="mansion", num_players=5, difficulty="hard")
    db_session.add(game)
    db_session.commit()

    plot = GeneratedPlot(
        game_id=game.id,
        setting="A grand mansion in the countryside, 1920s",
        victim="Lord Blackwood",
        crime="Murder by poisoning",
        culprit="The butler",
        murder_method="Arsenic in the wine",
        timeline=["8 PM: Dinner begins", "9 PM: Victim dies", "10 PM: Body discovered"],
        resolution="The detective reveals the butler's motive",
    )
    db_session.add(plot)
    db_session.commit()

    assert plot.id is not None
    assert plot.game_id == game.id
    assert plot.victim == "Lord Blackwood"
    assert isinstance(plot.timeline, list)
    assert plot.game == game


def test_create_clue(db_session):
    """Test creating a GeneratedClue."""
    game = Game(theme="cruise", num_players=8, difficulty="medium")
    db_session.add(game)
    db_session.commit()

    clue = GeneratedClue(
        game_id=game.id,
        clue_id="CLUE_001",
        description="A bloody knife found in the cabin",
        location="Cabin 12",
        revealed_by="The steward",
        significance="Murder weapon",
        misleading=False,
    )
    db_session.add(clue)
    db_session.commit()

    assert clue.id is not None
    assert clue.game_id == game.id
    assert clue.clue_id == "CLUE_001"
    assert clue.misleading is False
    assert clue.game == game


def test_create_metadata(db_session):
    """Test creating GeneratedMetadata."""
    game = Game(theme="noir", num_players=6, difficulty="medium")
    db_session.add(game)
    db_session.commit()

    metadata = GeneratedMetadata(
        game_id=game.id,
        title="Murder at the Speakeasy",
        estimated_duration=120,
        game_instructions="Players must interrogate suspects...",
        introduction="The year is 1925, and a famous jazz singer has been found dead...",
    )
    db_session.add(metadata)
    db_session.commit()

    assert metadata.id is not None
    assert metadata.game_id == game.id
    assert metadata.title == "Murder at the Speakeasy"
    assert metadata.estimated_duration == 120
    assert metadata.game == game


def test_create_validation_result(db_session):
    """Test creating a ValidationResult."""
    game = Game(theme="horror", num_players=5, difficulty="hard")
    db_session.add(game)
    db_session.commit()

    validation = ValidationResult(
        game_id=game.id,
        iteration=1,
        validation_passed=True,
        validation_errors=None,
    )
    db_session.add(validation)
    db_session.commit()

    assert validation.id is not None
    assert validation.game_id == game.id
    assert validation.iteration == 1
    assert validation.validation_passed is True
    assert isinstance(validation.created_at, datetime)
    assert validation.game == game


def test_game_relationships(db_session):
    """Test relationships between Game and related models."""
    game = Game(theme="mystery", num_players=6, difficulty="medium")
    db_session.add(game)
    db_session.commit()

    # Add characters
    char1 = GeneratedCharacter(
        game_id=game.id, name="Detective Jones", role="Detective",
        background="Ex-cop", personality="Analytical", secret="Hidden past"
    )
    char2 = GeneratedCharacter(
        game_id=game.id, name="Suspect Smith", role="Businessman",
        background="Corporate exec", personality="Ruthless", secret="Embezzlement"
    )
    db_session.add_all([char1, char2])

    # Add plot
    plot = GeneratedPlot(
        game_id=game.id, setting="Office building", victim="CEO",
        crime="Murder", culprit="Smith", murder_method="Poison",
        timeline=["Event 1"], resolution="Justice served"
    )
    db_session.add(plot)

    # Add clues
    clue1 = GeneratedClue(
        game_id=game.id, clue_id="C1", description="Evidence",
        location="Desk", significance="Key evidence", misleading=False
    )
    clue2 = GeneratedClue(
        game_id=game.id, clue_id="C2", description="Red herring",
        location="Floor", significance="Distraction", misleading=True
    )
    db_session.add_all([clue1, clue2])

    # Add metadata
    metadata = GeneratedMetadata(
        game_id=game.id, title="Corporate Conspiracy",
        estimated_duration=90, game_instructions="Instructions",
        introduction="Intro text"
    )
    db_session.add(metadata)

    # Add validation
    validation = ValidationResult(
        game_id=game.id, iteration=1, validation_passed=True,
        validation_errors=None
    )
    db_session.add(validation)

    db_session.commit()

    # Test relationships
    assert len(game.characters) == 2
    assert game.plot == plot
    assert len(game.clues) == 2
    assert game.game_metadata == metadata
    assert len(game.validation_results) == 1


def test_game_cascade_delete(db_session):
    """Test that deleting a game cascades to related models."""
    game = Game(theme="test", num_players=4, difficulty="easy")
    db_session.add(game)
    db_session.commit()

    # Add related records
    char = GeneratedCharacter(
        game_id=game.id, name="Test", role="Role",
        background="BG", personality="Pers", secret="Secret"
    )
    plot = GeneratedPlot(
        game_id=game.id, setting="Set", victim="Vic", crime="Crime",
        culprit="Culp", murder_method="Method", timeline=["T1"],
        resolution="Res"
    )
    clue = GeneratedClue(
        game_id=game.id, clue_id="CID", description="Desc",
        location="Loc", significance="Sig", misleading=False
    )
    metadata = GeneratedMetadata(
        game_id=game.id, title="Title", estimated_duration=60,
        game_instructions="Inst", introduction="Intro"
    )
    validation = ValidationResult(
        game_id=game.id, iteration=1, validation_passed=True,
        validation_errors=None
    )
    db_session.add_all([char, plot, clue, metadata, validation])
    db_session.commit()

    game_id = game.id

    # Delete game
    db_session.delete(game)
    db_session.commit()

    # Verify all related records are deleted
    assert db_session.query(GeneratedCharacter).filter_by(game_id=game_id).count() == 0
    assert db_session.query(GeneratedPlot).filter_by(game_id=game_id).count() == 0
    assert db_session.query(GeneratedClue).filter_by(game_id=game_id).count() == 0
    assert db_session.query(GeneratedMetadata).filter_by(game_id=game_id).count() == 0
    assert db_session.query(ValidationResult).filter_by(game_id=game_id).count() == 0


def test_game_status_enum(db_session):
    """Test GameStatus enum values."""
    game = Game(theme="test", num_players=4, difficulty="easy")
    db_session.add(game)
    db_session.commit()

    # Test status transitions
    assert game.status == GameStatus.INITIALIZED

    game.status = GameStatus.CHARACTERS_GENERATED
    db_session.commit()
    assert game.status == GameStatus.CHARACTERS_GENERATED

    game.status = GameStatus.PLOT_GENERATED
    db_session.commit()
    assert game.status == GameStatus.PLOT_GENERATED

    game.status = GameStatus.CLUES_GENERATED
    db_session.commit()
    assert game.status == GameStatus.CLUES_GENERATED

    game.status = GameStatus.METADATA_GENERATED
    db_session.commit()
    assert game.status == GameStatus.METADATA_GENERATED

    game.status = GameStatus.VALIDATED
    db_session.commit()
    assert game.status == GameStatus.VALIDATED

    game.status = GameStatus.COMPLETED
    db_session.commit()
    assert game.status == GameStatus.COMPLETED
