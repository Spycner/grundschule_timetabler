"""Tests for Subject model and API endpoints."""

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


def test_create_subject(client: TestClient, db: Session):
    """Test creating a new subject."""
    subject_data = {
        "name": "Mathematik",
        "code": "MA",
        "color": "#2563EB",  # Blue
    }

    response = client.post("/api/v1/subjects", json=subject_data)
    assert response.status_code == 201

    data = response.json()
    assert data["name"] == subject_data["name"]
    assert data["code"] == subject_data["code"]
    assert data["color"] == subject_data["color"]
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_create_subject_duplicate_name(client: TestClient, db: Session):
    """Test that duplicate subject names are rejected."""
    subject_data = {
        "name": "Mathematik",
        "code": "MA",
        "color": "#2563EB",
    }

    # Create first subject
    response = client.post("/api/v1/subjects", json=subject_data)
    assert response.status_code == 201

    # Try to create second subject with same name
    subject_data["code"] = "MAT"  # Change code to avoid that conflict
    subject_data["color"] = "#DC2626"  # Change color too
    response = client.post("/api/v1/subjects", json=subject_data)
    assert response.status_code == 409
    assert "name already exists" in response.json()["detail"].lower()


def test_create_subject_duplicate_code(client: TestClient, db: Session):
    """Test that duplicate subject codes are rejected."""
    subject_data = {
        "name": "Mathematik",
        "code": "MA",
        "color": "#2563EB",
    }

    # Create first subject
    response = client.post("/api/v1/subjects", json=subject_data)
    assert response.status_code == 201

    # Try to create second subject with same code
    subject_data["name"] = "Musik"  # Change name to avoid that conflict
    subject_data["color"] = "#DC2626"  # Change color too
    response = client.post("/api/v1/subjects", json=subject_data)
    assert response.status_code == 409
    assert "code already exists" in response.json()["detail"].lower()


def test_create_subject_invalid_color(client: TestClient, db: Session):
    """Test that invalid color formats are rejected."""
    subject_data = {
        "name": "Mathematik",
        "code": "MA",
        "color": "blue",  # Invalid format
    }

    response = client.post("/api/v1/subjects", json=subject_data)
    assert response.status_code == 422
    # Check that the error message mentions pattern matching
    assert "pattern" in response.json()["detail"][0]["msg"].lower()


def test_create_subject_invalid_code_length(client: TestClient, db: Session):
    """Test that codes must be 2-4 characters."""
    # Test too short
    subject_data = {
        "name": "Mathematik",
        "code": "M",  # Too short
        "color": "#2563EB",
    }

    response = client.post("/api/v1/subjects", json=subject_data)
    assert response.status_code == 422

    # Test too long
    subject_data["code"] = "MATHE"  # Too long
    response = client.post("/api/v1/subjects", json=subject_data)
    assert response.status_code == 422


def test_get_subjects(client: TestClient, db: Session):
    """Test getting all subjects."""
    # Create multiple subjects
    subjects = [
        {"name": "Mathematik", "code": "MA", "color": "#2563EB"},
        {"name": "Deutsch", "code": "DE", "color": "#DC2626"},
        {"name": "Sport", "code": "SPO", "color": "#16A34A"},
    ]

    for subject in subjects:
        response = client.post("/api/v1/subjects", json=subject)
        assert response.status_code == 201

    # Get all subjects
    response = client.get("/api/v1/subjects")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 3  # At least our 3 subjects


def test_get_subject_by_id(client: TestClient, db: Session):
    """Test getting a specific subject by ID."""
    subject_data = {
        "name": "Mathematik",
        "code": "MA",
        "color": "#2563EB",
    }

    # Create subject
    create_response = client.post("/api/v1/subjects", json=subject_data)
    assert create_response.status_code == 201
    created_subject = create_response.json()

    # Get subject by ID
    response = client.get(f"/api/v1/subjects/{created_subject['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == created_subject["id"]
    assert data["name"] == subject_data["name"]
    assert data["code"] == subject_data["code"]
    assert data["color"] == subject_data["color"]


def test_get_nonexistent_subject(client: TestClient, db: Session):
    """Test getting a subject that doesn't exist."""
    response = client.get("/api/v1/subjects/99999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_update_subject(client: TestClient, db: Session):
    """Test updating a subject."""
    subject_data = {
        "name": "Mathematik",
        "code": "MA",
        "color": "#2563EB",
    }

    # Create subject
    create_response = client.post("/api/v1/subjects", json=subject_data)
    assert create_response.status_code == 201
    created_subject = create_response.json()

    # Update subject
    update_data = {
        "name": "Mathematics",
        "color": "#3B82F6",  # Different blue
    }

    response = client.put(f"/api/v1/subjects/{created_subject['id']}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == update_data["name"]
    assert data["color"] == update_data["color"]
    assert data["code"] == subject_data["code"]  # Should remain unchanged


def test_update_subject_duplicate_name(client: TestClient, db: Session):
    """Test that updating to a duplicate name is rejected."""
    # Create two subjects
    subject1 = {"name": "Mathematik", "code": "MA", "color": "#2563EB"}
    subject2 = {"name": "Deutsch", "code": "DE", "color": "#DC2626"}

    response1 = client.post("/api/v1/subjects", json=subject1)
    assert response1.status_code == 201
    created_subject1 = response1.json()

    response2 = client.post("/api/v1/subjects", json=subject2)
    assert response2.status_code == 201

    # Try to update subject1 with subject2's name
    update_data = {"name": "Deutsch"}
    response = client.put(
        f"/api/v1/subjects/{created_subject1['id']}", json=update_data
    )
    assert response.status_code == 409
    assert "name already exists" in response.json()["detail"].lower()


def test_update_nonexistent_subject(client: TestClient, db: Session):
    """Test updating a subject that doesn't exist."""
    update_data = {"name": "Nonexistent"}
    response = client.put("/api/v1/subjects/99999", json=update_data)
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_delete_subject(client: TestClient, db: Session):
    """Test deleting a subject."""
    subject_data = {
        "name": "Mathematik",
        "code": "MA",
        "color": "#2563EB",
    }

    # Create subject
    create_response = client.post("/api/v1/subjects", json=subject_data)
    assert create_response.status_code == 201
    created_subject = create_response.json()

    # Delete subject
    response = client.delete(f"/api/v1/subjects/{created_subject['id']}")
    assert response.status_code == 204

    # Verify subject is deleted
    response = client.get(f"/api/v1/subjects/{created_subject['id']}")
    assert response.status_code == 404


def test_delete_nonexistent_subject(client: TestClient, db: Session):
    """Test deleting a subject that doesn't exist."""
    response = client.delete("/api/v1/subjects/99999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_subject_code_uppercase_conversion(client: TestClient, db: Session):
    """Test that subject codes are automatically converted to uppercase."""
    subject_data = {
        "name": "Mathematik",
        "code": "ma",  # Lowercase
        "color": "#2563EB",
    }

    response = client.post("/api/v1/subjects", json=subject_data)
    assert response.status_code == 201
    data = response.json()
    assert data["code"] == "MA"  # Should be uppercase
