"""Tests for Teacher model and API endpoints."""

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


def test_create_teacher(client: TestClient, db: Session):
    """Test creating a new teacher."""
    teacher_data = {
        "first_name": "Maria",
        "last_name": "Müller",
        "email": "maria.mueller@schule.de",
        "abbreviation": "MUE",
        "max_hours_per_week": 28,
        "is_part_time": False,
    }

    response = client.post("/api/v1/teachers", json=teacher_data)
    assert response.status_code == 201

    data = response.json()
    assert data["email"] == teacher_data["email"]
    assert data["first_name"] == teacher_data["first_name"]
    assert data["last_name"] == teacher_data["last_name"]
    assert data["abbreviation"] == teacher_data["abbreviation"]
    assert data["max_hours_per_week"] == teacher_data["max_hours_per_week"]
    assert data["is_part_time"] == teacher_data["is_part_time"]
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_create_teacher_duplicate_email(client: TestClient, db: Session):
    """Test that duplicate email addresses are rejected."""
    teacher_data = {
        "first_name": "Maria",
        "last_name": "Müller",
        "email": "maria.mueller@schule.de",
        "abbreviation": "MUE",
        "max_hours_per_week": 28,
        "is_part_time": False,
    }

    # Create first teacher
    response = client.post("/api/v1/teachers", json=teacher_data)
    assert response.status_code == 201

    # Try to create second teacher with same email
    teacher_data["abbreviation"] = "MU2"  # Change abbreviation to avoid that conflict
    response = client.post("/api/v1/teachers", json=teacher_data)
    assert response.status_code == 409
    assert "email" in response.json()["detail"].lower()


def test_create_teacher_duplicate_abbreviation(client: TestClient, db: Session):
    """Test that duplicate abbreviations are rejected."""
    teacher_data = {
        "first_name": "Maria",
        "last_name": "Müller",
        "email": "maria.mueller@schule.de",
        "abbreviation": "MUE",
        "max_hours_per_week": 28,
        "is_part_time": False,
    }

    # Create first teacher
    response = client.post("/api/v1/teachers", json=teacher_data)
    assert response.status_code == 201

    # Try to create second teacher with same abbreviation
    teacher_data["email"] = (
        "another.teacher@schule.de"  # Change email to avoid that conflict
    )
    response = client.post("/api/v1/teachers", json=teacher_data)
    assert response.status_code == 409
    assert "abbreviation" in response.json()["detail"].lower()


def test_create_teacher_invalid_email(client: TestClient):
    """Test that invalid email addresses are rejected."""
    teacher_data = {
        "first_name": "Maria",
        "last_name": "Müller",
        "email": "not-an-email",
        "abbreviation": "MUE",
        "max_hours_per_week": 28,
        "is_part_time": False,
    }

    response = client.post("/api/v1/teachers", json=teacher_data)
    assert response.status_code == 422


def test_create_teacher_missing_required_fields(client: TestClient):
    """Test that missing required fields are rejected."""
    # Missing first_name
    teacher_data = {
        "last_name": "Müller",
        "email": "maria.mueller@schule.de",
        "abbreviation": "MUE",
    }

    response = client.post("/api/v1/teachers", json=teacher_data)
    assert response.status_code == 422


def test_create_teacher_invalid_max_hours(client: TestClient):
    """Test that invalid max_hours_per_week values are rejected."""
    teacher_data = {
        "first_name": "Maria",
        "last_name": "Müller",
        "email": "maria.mueller@schule.de",
        "abbreviation": "MUE",
        "max_hours_per_week": 50,  # Too high
        "is_part_time": False,
    }

    response = client.post("/api/v1/teachers", json=teacher_data)
    assert response.status_code == 422

    teacher_data["max_hours_per_week"] = 0  # Too low
    response = client.post("/api/v1/teachers", json=teacher_data)
    assert response.status_code == 422


def test_create_teacher_invalid_abbreviation_length(client: TestClient):
    """Test that abbreviations must be 2-3 characters."""
    teacher_data = {
        "first_name": "Maria",
        "last_name": "Müller",
        "email": "maria.mueller@schule.de",
        "abbreviation": "M",  # Too short
        "max_hours_per_week": 28,
        "is_part_time": False,
    }

    response = client.post("/api/v1/teachers", json=teacher_data)
    assert response.status_code == 422

    teacher_data["abbreviation"] = "MUEL"  # Too long
    response = client.post("/api/v1/teachers", json=teacher_data)
    assert response.status_code == 422


def test_get_teachers(client: TestClient, db: Session):
    """Test getting list of all teachers."""
    # Create some teachers
    teachers = [
        {
            "first_name": "Maria",
            "last_name": "Müller",
            "email": "maria.mueller@schule.de",
            "abbreviation": "MUE",
            "max_hours_per_week": 28,
            "is_part_time": False,
        },
        {
            "first_name": "Hans",
            "last_name": "Schmidt",
            "email": "hans.schmidt@schule.de",
            "abbreviation": "SCH",
            "max_hours_per_week": 20,
            "is_part_time": True,
        },
    ]

    for teacher in teachers:
        response = client.post("/api/v1/teachers", json=teacher)
        assert response.status_code == 201

    # Get all teachers
    response = client.get("/api/v1/teachers")
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 2
    assert data[0]["email"] == teachers[0]["email"]
    assert data[1]["email"] == teachers[1]["email"]


def test_get_teacher_by_id(client: TestClient, db: Session):
    """Test getting a specific teacher by ID."""
    teacher_data = {
        "first_name": "Maria",
        "last_name": "Müller",
        "email": "maria.mueller@schule.de",
        "abbreviation": "MUE",
        "max_hours_per_week": 28,
        "is_part_time": False,
    }

    # Create teacher
    response = client.post("/api/v1/teachers", json=teacher_data)
    assert response.status_code == 201
    teacher_id = response.json()["id"]

    # Get teacher by ID
    response = client.get(f"/api/v1/teachers/{teacher_id}")
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == teacher_id
    assert data["email"] == teacher_data["email"]


def test_get_teacher_not_found(client: TestClient):
    """Test getting a non-existent teacher."""
    response = client.get("/api/v1/teachers/999999")
    assert response.status_code == 404


def test_update_teacher(client: TestClient, db: Session):
    """Test updating a teacher."""
    teacher_data = {
        "first_name": "Maria",
        "last_name": "Müller",
        "email": "maria.mueller@schule.de",
        "abbreviation": "MUE",
        "max_hours_per_week": 28,
        "is_part_time": False,
    }

    # Create teacher
    response = client.post("/api/v1/teachers", json=teacher_data)
    assert response.status_code == 201
    teacher_id = response.json()["id"]

    # Update teacher
    update_data = {
        "max_hours_per_week": 20,
        "is_part_time": True,
    }
    response = client.put(f"/api/v1/teachers/{teacher_id}", json=update_data)
    assert response.status_code == 200

    data = response.json()
    assert data["max_hours_per_week"] == 20
    assert data["is_part_time"] is True
    # Unchanged fields should remain the same
    assert data["email"] == teacher_data["email"]
    assert data["first_name"] == teacher_data["first_name"]


def test_update_teacher_not_found(client: TestClient):
    """Test updating a non-existent teacher."""
    update_data = {
        "max_hours_per_week": 20,
    }
    response = client.put("/api/v1/teachers/999999", json=update_data)
    assert response.status_code == 404


def test_update_teacher_duplicate_email(client: TestClient, db: Session):
    """Test that updating to a duplicate email is rejected."""
    # Create two teachers
    teacher1 = {
        "first_name": "Maria",
        "last_name": "Müller",
        "email": "maria.mueller@schule.de",
        "abbreviation": "MUE",
        "max_hours_per_week": 28,
        "is_part_time": False,
    }
    teacher2 = {
        "first_name": "Hans",
        "last_name": "Schmidt",
        "email": "hans.schmidt@schule.de",
        "abbreviation": "SCH",
        "max_hours_per_week": 28,
        "is_part_time": False,
    }

    response = client.post("/api/v1/teachers", json=teacher1)
    assert response.status_code == 201

    response = client.post("/api/v1/teachers", json=teacher2)
    assert response.status_code == 201
    teacher2_id = response.json()["id"]

    # Try to update teacher2 with teacher1's email
    update_data = {"email": teacher1["email"]}
    response = client.put(f"/api/v1/teachers/{teacher2_id}", json=update_data)
    assert response.status_code == 409


def test_delete_teacher(client: TestClient, db: Session):
    """Test deleting a teacher."""
    teacher_data = {
        "first_name": "Maria",
        "last_name": "Müller",
        "email": "maria.mueller@schule.de",
        "abbreviation": "MUE",
        "max_hours_per_week": 28,
        "is_part_time": False,
    }

    # Create teacher
    response = client.post("/api/v1/teachers", json=teacher_data)
    assert response.status_code == 201
    teacher_id = response.json()["id"]

    # Delete teacher
    response = client.delete(f"/api/v1/teachers/{teacher_id}")
    assert response.status_code == 204

    # Verify teacher is deleted
    response = client.get(f"/api/v1/teachers/{teacher_id}")
    assert response.status_code == 404


def test_delete_teacher_not_found(client: TestClient):
    """Test deleting a non-existent teacher."""
    response = client.delete("/api/v1/teachers/999999")
    assert response.status_code == 404
