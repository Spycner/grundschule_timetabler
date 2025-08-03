"""Tests for health check endpoints."""

from fastapi.testclient import TestClient


def test_health_check(client: TestClient):
    """Test basic health check endpoint."""
    response = client.get("/api/health")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert data["service"] == "Grundschule Timetabler API"
    assert data["version"] == "0.1.0"
    assert data["environment"] in ["development", "testing", "production"]


def test_readiness_check(client: TestClient):
    """Test readiness check including database connectivity."""
    response = client.get("/api/health/ready")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] in ["ready", "not ready"]
    assert "timestamp" in data
    assert data["service"] == "Grundschule Timetabler API"
    assert data["version"] == "0.1.0"
    assert "database" in data


def test_root_endpoint(client: TestClient):
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200

    data = response.json()
    assert data["message"] == "Welcome to Grundschule Timetabler API"
    assert data["version"] == "0.1.0"
    assert data["docs"] == "/docs"
    assert data["health"] == "/api/health"
