"""Unit tests for FastAPI endpoints."""

import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_root_endpoint():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert data["version"] == "0.1.0"


def test_health_endpoint():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_generate_endpoint_invalid_num_players():
    """Test generate endpoint with invalid number of players."""
    response = client.post(
        "/generate",
        json={
            "theme": "film noir",
            "num_players": 2,  # Too few players (minimum is 3)
            "difficulty": "medium",
        },
    )
    assert response.status_code == 422  # Validation error


def test_generate_endpoint_missing_theme():
    """Test generate endpoint with missing theme."""
    response = client.post(
        "/generate",
        json={
            "num_players": 6,
            "difficulty": "medium",
        },
    )
    assert response.status_code == 422  # Validation error


def test_openapi_schema():
    """Test that OpenAPI schema is accessible."""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    assert "openapi" in schema
    assert "info" in schema
    assert schema["info"]["title"] == "Mystery Party Game Generator API"
