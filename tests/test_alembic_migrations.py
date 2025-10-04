"""Tests for Alembic migrations."""

import pytest
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from src.database.base import Base
from src.database.models import Game, GameStatus, GeneratedCharacter
import tempfile
import os


@pytest.fixture
def temp_db():
    """Create a temporary database for testing."""
    # Create a temporary file for the database
    fd, db_path = tempfile.mkstemp(suffix=".db")
    os.close(fd)

    db_url = f"sqlite:///{db_path}"

    # Create engine and tables
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)

    yield engine

    # Clean up
    engine.dispose()
    try:
        os.remove(db_path)
    except:
        pass


def test_database_tables_created(temp_db):
    """Test that all tables are created correctly."""
    inspector = inspect(temp_db)
    tables = inspector.get_table_names()

    assert "games" in tables
    assert "generated_characters" in tables
    assert "generated_plots" in tables
    assert "generated_clues" in tables
    assert "generated_metadata" in tables
    assert "validation_results" in tables


def test_games_table_schema(temp_db):
    """Test that games table has correct schema."""
    inspector = inspect(temp_db)

    columns = {col["name"]: col for col in inspector.get_columns("games")}

    assert "id" in columns
    assert "theme" in columns
    assert "num_players" in columns
    assert "difficulty" in columns
    assert "special_requests" in columns
    assert "status" in columns
    assert "created_at" in columns
    assert "updated_at" in columns

    # Check primary key
    pk_constraint = inspector.get_pk_constraint("games")
    assert "id" in pk_constraint["constrained_columns"]


def test_foreign_key_constraints(temp_db):
    """Test that foreign key constraints are properly set up."""
    inspector = inspect(temp_db)

    # Check GeneratedCharacter foreign key
    fks = inspector.get_foreign_keys("generated_characters")
    assert len(fks) > 0
    assert fks[0]["referred_table"] == "games"
    assert "game_id" in fks[0]["constrained_columns"]

    # Check GeneratedPlot foreign key
    fks = inspector.get_foreign_keys("generated_plots")
    assert len(fks) > 0
    assert fks[0]["referred_table"] == "games"

    # Check GeneratedClue foreign key
    fks = inspector.get_foreign_keys("generated_clues")
    assert len(fks) > 0
    assert fks[0]["referred_table"] == "games"

    # Check GeneratedMetadata foreign key
    fks = inspector.get_foreign_keys("generated_metadata")
    assert len(fks) > 0
    assert fks[0]["referred_table"] == "games"

    # Check ValidationResult foreign key
    fks = inspector.get_foreign_keys("validation_results")
    assert len(fks) > 0
    assert fks[0]["referred_table"] == "games"


def test_unique_constraints(temp_db):
    """Test that unique constraints are properly set up."""
    inspector = inspect(temp_db)

    # GeneratedPlot should have unique game_id
    unique_constraints = inspector.get_unique_constraints("generated_plots")
    game_id_is_unique = any(
        "game_id" in uc["column_names"]
        for uc in unique_constraints
    )
    assert game_id_is_unique

    # GeneratedMetadata should have unique game_id
    unique_constraints = inspector.get_unique_constraints("generated_metadata")
    game_id_is_unique = any(
        "game_id" in uc["column_names"]
        for uc in unique_constraints
    )
    assert game_id_is_unique


def test_migration_data_persistence(temp_db):
    """Test that data can be inserted and retrieved."""
    Session = sessionmaker(bind=temp_db)
    session = Session()

    # Insert test data
    game = Game(
        theme="test_theme",
        num_players=4,
        difficulty="easy",
        status=GameStatus.INITIALIZED
    )
    session.add(game)
    session.commit()
    game_id = game.id
    session.close()

    # Query data back
    session = Session()
    retrieved_game = session.query(Game).filter_by(id=game_id).first()

    assert retrieved_game is not None
    assert retrieved_game.theme == "test_theme"
    assert retrieved_game.num_players == 4
    assert retrieved_game.difficulty == "easy"
    assert retrieved_game.status == GameStatus.INITIALIZED

    session.close()


def test_alembic_migration_file_exists():
    """Test that Alembic migration file was created."""
    import os
    import glob

    migration_files = glob.glob("alembic/versions/*.py")
    assert len(migration_files) > 0

    # Check that at least one migration file contains our tables
    found_games_table = False
    for migration_file in migration_files:
        with open(migration_file, 'r') as f:
            content = f.read()
            if "'games'" in content or '"games"' in content:
                found_games_table = True
                break

    assert found_games_table, "No migration file contains the games table"
