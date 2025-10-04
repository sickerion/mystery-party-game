"""Tests for incremental API endpoints."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.api.main import app
from src.database.base import Base, get_db
import tempfile
import os


@pytest.fixture
def temp_db():
    """Create a temporary database for testing."""
    fd, db_path = tempfile.mkstemp(suffix=".db")
    os.close(fd)

    db_url = f"sqlite:///{db_path}"
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)

    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    yield TestingSessionLocal

    # Clean up
    app.dependency_overrides.clear()
    engine.dispose()
    try:
        os.remove(db_path)
    except:
        pass


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


def test_create_game(client, temp_db):
    """Test POST /games endpoint."""
    response = client.post(
        "/games",
        json={
            "theme": "film noir",
            "num_players": 6,
            "difficulty": "medium",
            "special_requests": "Include detective",
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert data["theme"] == "film noir"
    assert data["num_players"] == 6
    assert data["status"] == "initialized"
    assert "id" in data


def test_list_games(client, temp_db):
    """Test GET /games endpoint."""
    # Create a few games
    client.post("/games", json={"theme": "test1", "num_players": 4, "difficulty": "easy"})
    client.post("/games", json={"theme": "test2", "num_players": 6, "difficulty": "medium"})

    response = client.get("/games")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


def test_list_games_with_status_filter(client, temp_db):
    """Test GET /games with status filter."""
    client.post("/games", json={"theme": "test1", "num_players": 4, "difficulty": "easy"})

    response = client.get("/games?status=initialized")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["status"] == "initialized"


def test_get_game_not_found(client, temp_db):
    """Test GET /games/{game_id} with non-existent ID."""
    response = client.get("/games/non-existent-id")

    assert response.status_code == 404


def test_get_game_without_components(client, temp_db):
    """Test GET /games/{game_id} when components not yet generated."""
    create_response = client.post(
        "/games",
        json={"theme": "test", "num_players": 4, "difficulty": "easy"},
    )
    game_id = create_response.json()["id"]

    response = client.get(f"/games/{game_id}")

    assert response.status_code == 400
    assert "Characters not yet generated" in response.json()["detail"]


def test_delete_game(client, temp_db):
    """Test DELETE /games/{game_id}."""
    create_response = client.post(
        "/games",
        json={"theme": "test", "num_players": 4, "difficulty": "easy"},
    )
    game_id = create_response.json()["id"]

    response = client.delete(f"/games/{game_id}")

    assert response.status_code == 204

    # Verify game is deleted
    get_response = client.get(f"/games/{game_id}")
    assert get_response.status_code == 404


def test_delete_game_not_found(client, temp_db):
    """Test DELETE /games/{game_id} with non-existent ID."""
    response = client.delete("/games/non-existent-id")

    assert response.status_code == 404


def test_generate_characters_not_found(client, temp_db):
    """Test POST /games/{game_id}/characters with non-existent game."""
    response = client.post("/games/non-existent-id/characters")

    assert response.status_code == 404


def test_generate_plot_without_characters(client, temp_db):
    """Test POST /games/{game_id}/plot without characters."""
    create_response = client.post(
        "/games",
        json={"theme": "test", "num_players": 4, "difficulty": "easy"},
    )
    game_id = create_response.json()["id"]

    response = client.post(f"/games/{game_id}/plot")

    assert response.status_code == 400
    assert "Characters must be generated first" in response.json()["detail"]


def test_generate_clues_without_plot(client, temp_db):
    """Test POST /games/{game_id}/clues without plot."""
    create_response = client.post(
        "/games",
        json={"theme": "test", "num_players": 4, "difficulty": "easy"},
    )
    game_id = create_response.json()["id"]

    response = client.post(f"/games/{game_id}/clues")

    assert response.status_code == 400
    assert "Characters must be generated first" in response.json()["detail"]


def test_generate_metadata_without_clues(client, temp_db):
    """Test POST /games/{game_id}/metadata without clues."""
    create_response = client.post(
        "/games",
        json={"theme": "test", "num_players": 4, "difficulty": "easy"},
    )
    game_id = create_response.json()["id"]

    response = client.post(f"/games/{game_id}/metadata")

    assert response.status_code == 400
    assert "Characters must be generated first" in response.json()["detail"]


def test_validate_without_metadata(client, temp_db):
    """Test POST /games/{game_id}/validate without metadata."""
    create_response = client.post(
        "/games",
        json={"theme": "test", "num_players": 4, "difficulty": "easy"},
    )
    game_id = create_response.json()["id"]

    response = client.post(f"/games/{game_id}/validate")

    assert response.status_code == 400
    assert "Characters must be generated first" in response.json()["detail"]


def test_api_workflow_sequence_validation_only(client, temp_db):
    """Test that endpoints enforce correct sequence (without actual LLM calls)."""
    # 1. Create game
    create_response = client.post(
        "/games",
        json={"theme": "test", "num_players": 4, "difficulty": "easy"},
    )
    assert create_response.status_code == 201
    game_id = create_response.json()["id"]

    # 2. Try to generate plot before characters - should fail
    plot_response = client.post(f"/games/{game_id}/plot")
    assert plot_response.status_code == 400
    assert "Characters must be generated first" in plot_response.json()["detail"]

    # 3. Try to generate clues before characters - should fail
    clues_response = client.post(f"/games/{game_id}/clues")
    assert clues_response.status_code == 400

    # 4. Try to generate metadata before all components - should fail
    metadata_response = client.post(f"/games/{game_id}/metadata")
    assert metadata_response.status_code == 400

    # 5. Try to validate before all components - should fail
    validate_response = client.post(f"/games/{game_id}/validate")
    assert validate_response.status_code == 400

    # Note: We don't test actual generation here because it requires API keys
    # The full workflow is tested in integration tests with mocked LLM calls


def test_list_games_pagination(client, temp_db):
    """Test GET /games with pagination."""
    # Create 5 games
    for i in range(5):
        client.post("/games", json={"theme": f"test{i}", "num_players": 4, "difficulty": "easy"})

    # Get first 2
    response = client.get("/games?limit=2&offset=0")
    assert response.status_code == 200
    assert len(response.json()) == 2

    # Get next 2
    response = client.get("/games?limit=2&offset=2")
    assert response.status_code == 200
    assert len(response.json()) == 2

    # Get last 1
    response = client.get("/games?limit=2&offset=4")
    assert response.status_code == 200
    assert len(response.json()) == 1
