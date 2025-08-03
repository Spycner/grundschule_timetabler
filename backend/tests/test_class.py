"""Tests for Class model and API endpoints."""

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


def test_create_class(client: TestClient, db: Session):
    """Test creating a new class."""
    class_data = {
        "name": "1a",
        "grade": 1,
        "size": 22,
        "home_room": "101",
    }

    response = client.post("/api/v1/classes", json=class_data)
    assert response.status_code == 201

    data = response.json()
    assert data["name"] == class_data["name"]
    assert data["grade"] == class_data["grade"]
    assert data["size"] == class_data["size"]
    assert data["home_room"] == class_data["home_room"]
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_create_class_duplicate_name(client: TestClient, db: Session):
    """Test that duplicate class names are rejected."""
    class_data = {
        "name": "1a",
        "grade": 1,
        "size": 22,
        "home_room": "101",
    }

    # Create first class
    response = client.post("/api/v1/classes", json=class_data)
    assert response.status_code == 201

    # Try to create second class with same name
    class_data["home_room"] = "102"  # Change room to avoid that being the issue
    response = client.post("/api/v1/classes", json=class_data)
    assert response.status_code == 409
    assert "name" in response.json()["detail"].lower()


def test_create_class_invalid_grade(client: TestClient):
    """Test that invalid grade levels are rejected."""
    # Grade too low
    class_data = {
        "name": "0a",
        "grade": 0,
        "size": 22,
        "home_room": "101",
    }

    response = client.post("/api/v1/classes", json=class_data)
    assert response.status_code == 422

    # Grade too high
    class_data["name"] = "5a"
    class_data["grade"] = 5
    response = client.post("/api/v1/classes", json=class_data)
    assert response.status_code == 422


def test_create_class_invalid_size(client: TestClient):
    """Test that invalid class sizes are rejected."""
    # Size too low
    class_data = {
        "name": "1a",
        "grade": 1,
        "size": 0,
        "home_room": "101",
    }

    response = client.post("/api/v1/classes", json=class_data)
    assert response.status_code == 422

    # Size too high
    class_data["size"] = 36
    response = client.post("/api/v1/classes", json=class_data)
    assert response.status_code == 422


def test_create_class_missing_required_fields(client: TestClient):
    """Test that missing required fields are rejected."""
    # Missing name
    class_data = {
        "grade": 1,
        "size": 22,
        "home_room": "101",
    }

    response = client.post("/api/v1/classes", json=class_data)
    assert response.status_code == 422

    # Missing grade
    class_data = {
        "name": "1a",
        "size": 22,
        "home_room": "101",
    }

    response = client.post("/api/v1/classes", json=class_data)
    assert response.status_code == 422


def test_create_class_without_home_room(client: TestClient, db: Session):
    """Test creating a class without home_room (optional field)."""
    class_data = {
        "name": "1b",
        "grade": 1,
        "size": 20,
    }

    response = client.post("/api/v1/classes", json=class_data)
    assert response.status_code == 201

    data = response.json()
    assert data["name"] == class_data["name"]
    assert data["home_room"] is None


def test_get_classes(client: TestClient, db: Session):
    """Test getting list of all classes."""
    # Create some classes
    classes = [
        {
            "name": "1a",
            "grade": 1,
            "size": 22,
            "home_room": "101",
        },
        {
            "name": "2b",
            "grade": 2,
            "size": 24,
            "home_room": "202",
        },
        {
            "name": "3c",
            "grade": 3,
            "size": 21,
            "home_room": "303",
        },
    ]

    for class_data in classes:
        response = client.post("/api/v1/classes", json=class_data)
        assert response.status_code == 201

    # Get all classes
    response = client.get("/api/v1/classes")
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 3
    assert data[0]["name"] == classes[0]["name"]
    assert data[1]["name"] == classes[1]["name"]
    assert data[2]["name"] == classes[2]["name"]


def test_get_class_by_id(client: TestClient, db: Session):
    """Test getting a specific class by ID."""
    class_data = {
        "name": "1a",
        "grade": 1,
        "size": 22,
        "home_room": "101",
    }

    # Create class
    response = client.post("/api/v1/classes", json=class_data)
    assert response.status_code == 201
    class_id = response.json()["id"]

    # Get class by ID
    response = client.get(f"/api/v1/classes/{class_id}")
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == class_id
    assert data["name"] == class_data["name"]
    assert data["grade"] == class_data["grade"]


def test_get_class_not_found(client: TestClient):
    """Test getting a non-existent class."""
    response = client.get("/api/v1/classes/999999")
    assert response.status_code == 404


def test_update_class(client: TestClient, db: Session):
    """Test updating a class."""
    class_data = {
        "name": "1a",
        "grade": 1,
        "size": 22,
        "home_room": "101",
    }

    # Create class
    response = client.post("/api/v1/classes", json=class_data)
    assert response.status_code == 201
    class_id = response.json()["id"]

    # Update class
    update_data = {
        "size": 25,
        "home_room": "105",
    }
    response = client.put(f"/api/v1/classes/{class_id}", json=update_data)
    assert response.status_code == 200

    data = response.json()
    assert data["size"] == 25
    assert data["home_room"] == "105"
    # Unchanged fields should remain the same
    assert data["name"] == class_data["name"]
    assert data["grade"] == class_data["grade"]


def test_update_class_not_found(client: TestClient):
    """Test updating a non-existent class."""
    update_data = {
        "size": 25,
    }
    response = client.put("/api/v1/classes/999999", json=update_data)
    assert response.status_code == 404


def test_update_class_duplicate_name(client: TestClient, db: Session):
    """Test that updating to a duplicate name is rejected."""
    # Create two classes
    class1 = {
        "name": "1a",
        "grade": 1,
        "size": 22,
        "home_room": "101",
    }
    class2 = {
        "name": "1b",
        "grade": 1,
        "size": 24,
        "home_room": "102",
    }

    response = client.post("/api/v1/classes", json=class1)
    assert response.status_code == 201

    response = client.post("/api/v1/classes", json=class2)
    assert response.status_code == 201
    class2_id = response.json()["id"]

    # Try to update class2 with class1's name
    update_data = {"name": class1["name"]}
    response = client.put(f"/api/v1/classes/{class2_id}", json=update_data)
    assert response.status_code == 409


def test_delete_class(client: TestClient, db: Session):
    """Test deleting a class."""
    class_data = {
        "name": "1a",
        "grade": 1,
        "size": 22,
        "home_room": "101",
    }

    # Create class
    response = client.post("/api/v1/classes", json=class_data)
    assert response.status_code == 201
    class_id = response.json()["id"]

    # Delete class
    response = client.delete(f"/api/v1/classes/{class_id}")
    assert response.status_code == 204

    # Verify class is deleted
    response = client.get(f"/api/v1/classes/{class_id}")
    assert response.status_code == 404


def test_delete_class_not_found(client: TestClient):
    """Test deleting a non-existent class."""
    response = client.delete("/api/v1/classes/999999")
    assert response.status_code == 404


def test_class_name_examples(client: TestClient, db: Session):
    """Test various valid class name formats."""
    valid_names = ["1a", "2b", "3c", "4d", "1A", "2B", "Klasse 1", "Flex A"]

    for i, name in enumerate(valid_names):
        class_data = {
            "name": name,
            "grade": (i % 4) + 1,  # Cycle through grades 1-4
            "size": 20 + i,
            "home_room": f"10{i}",
        }

        response = client.post("/api/v1/classes", json=class_data)
        assert response.status_code == 201
        assert response.json()["name"] == name
