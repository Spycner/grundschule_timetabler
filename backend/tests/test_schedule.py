"""Tests for Schedule model and API endpoints."""

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


def test_create_schedule_entry(client: TestClient, db: Session):
    """Test creating a new schedule entry."""
    # First, create necessary entities
    teacher_data = {
        "first_name": "Maria",
        "last_name": "Müller",
        "email": "maria.mueller@schule.de",
        "abbreviation": "MUE",
        "max_hours_per_week": 28,
        "is_part_time": False,
    }
    teacher_response = client.post("/api/v1/teachers", json=teacher_data)
    assert teacher_response.status_code == 201
    teacher_id = teacher_response.json()["id"]

    class_data = {
        "name": "1a",
        "grade": 1,
        "size": 20,
        "home_room": "101",
    }
    class_response = client.post("/api/v1/classes", json=class_data)
    assert class_response.status_code == 201
    class_id = class_response.json()["id"]

    subject_data = {
        "name": "Mathematik",
        "code": "MA",
        "color": "#2563EB",
    }
    subject_response = client.post("/api/v1/subjects", json=subject_data)
    assert subject_response.status_code == 201
    subject_id = subject_response.json()["id"]

    # Generate default timeslots
    timeslot_response = client.post("/api/v1/timeslots/generate-default")
    assert timeslot_response.status_code == 201

    # Get the generated timeslots
    timeslots_response = client.get("/api/v1/timeslots")
    assert timeslots_response.status_code == 200
    timeslots = timeslots_response.json()
    assert len(timeslots) > 0
    timeslot_id = timeslots[0]["id"]

    # Create schedule entry
    schedule_data = {
        "class_id": class_id,
        "teacher_id": teacher_id,
        "subject_id": subject_id,
        "timeslot_id": timeslot_id,
        "room": "101",
        "week_type": "ALL",
    }

    response = client.post("/api/v1/schedule", json=schedule_data)
    assert response.status_code == 201

    data = response.json()
    assert data["class"]["id"] == class_id
    assert data["teacher"]["id"] == teacher_id
    assert data["subject"]["id"] == subject_id
    assert data["timeslot"]["id"] == timeslot_id
    assert data["room"] == "101"
    assert data["week_type"] == "ALL"
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_teacher_conflict_detection(client: TestClient, db: Session):
    """Test that a teacher cannot be scheduled in two places at the same time."""
    # Create entities
    teacher_data = {
        "first_name": "Maria",
        "last_name": "Müller",
        "email": "maria.mueller@schule.de",
        "abbreviation": "MUE",
        "max_hours_per_week": 28,
        "is_part_time": False,
    }
    teacher_response = client.post("/api/v1/teachers", json=teacher_data)
    teacher_id = teacher_response.json()["id"]

    # Create two classes
    class1_response = client.post(
        "/api/v1/classes",
        json={"name": "1a", "grade": 1, "size": 20, "home_room": "101"},
    )
    class1_id = class1_response.json()["id"]

    class2_response = client.post(
        "/api/v1/classes",
        json={"name": "1b", "grade": 1, "size": 20, "home_room": "102"},
    )
    class2_id = class2_response.json()["id"]

    subject_response = client.post(
        "/api/v1/subjects",
        json={"name": "Mathematik", "code": "MA", "color": "#2563EB"},
    )
    subject_id = subject_response.json()["id"]

    # Generate timeslots
    client.post("/api/v1/timeslots/generate-default")
    timeslots_response = client.get("/api/v1/timeslots")
    timeslots = timeslots_response.json()
    timeslot_id = timeslots[0]["id"]

    # Create first schedule entry
    schedule1_data = {
        "class_id": class1_id,
        "teacher_id": teacher_id,
        "subject_id": subject_id,
        "timeslot_id": timeslot_id,
        "room": "101",
        "week_type": "ALL",
    }
    response1 = client.post("/api/v1/schedule", json=schedule1_data)
    assert response1.status_code == 201

    # Try to create conflicting schedule entry
    schedule2_data = {
        "class_id": class2_id,
        "teacher_id": teacher_id,
        "subject_id": subject_id,
        "timeslot_id": timeslot_id,
        "room": "102",
        "week_type": "ALL",
    }
    response2 = client.post("/api/v1/schedule", json=schedule2_data)
    assert response2.status_code == 409
    assert "teacher" in response2.json()["detail"].lower()


def test_class_conflict_detection(client: TestClient, db: Session):
    """Test that a class cannot have two subjects at the same time."""
    # Create entities
    teacher1_response = client.post(
        "/api/v1/teachers",
        json={
            "first_name": "Maria",
            "last_name": "Müller",
            "email": "maria.mueller@schule.de",
            "abbreviation": "MUE",
            "max_hours_per_week": 28,
            "is_part_time": False,
        },
    )
    teacher1_id = teacher1_response.json()["id"]

    teacher2_response = client.post(
        "/api/v1/teachers",
        json={
            "first_name": "Thomas",
            "last_name": "Schmidt",
            "email": "thomas.schmidt@schule.de",
            "abbreviation": "SCH",
            "max_hours_per_week": 28,
            "is_part_time": False,
        },
    )
    teacher2_id = teacher2_response.json()["id"]

    class_response = client.post(
        "/api/v1/classes",
        json={"name": "1a", "grade": 1, "size": 20, "home_room": "101"},
    )
    class_id = class_response.json()["id"]

    subject1_response = client.post(
        "/api/v1/subjects",
        json={"name": "Mathematik", "code": "MA", "color": "#2563EB"},
    )
    subject1_id = subject1_response.json()["id"]

    subject2_response = client.post(
        "/api/v1/subjects",
        json={"name": "Deutsch", "code": "DE", "color": "#DC2626"},
    )
    subject2_id = subject2_response.json()["id"]

    # Generate timeslots
    client.post("/api/v1/timeslots/generate-default")
    timeslots_response = client.get("/api/v1/timeslots")
    timeslots = timeslots_response.json()
    timeslot_id = timeslots[0]["id"]

    # Create first schedule entry
    schedule1_data = {
        "class_id": class_id,
        "teacher_id": teacher1_id,
        "subject_id": subject1_id,
        "timeslot_id": timeslot_id,
        "room": "101",
        "week_type": "ALL",
    }
    response1 = client.post("/api/v1/schedule", json=schedule1_data)
    assert response1.status_code == 201

    # Try to create conflicting schedule entry
    schedule2_data = {
        "class_id": class_id,
        "teacher_id": teacher2_id,
        "subject_id": subject2_id,
        "timeslot_id": timeslot_id,
        "room": "102",
        "week_type": "ALL",
    }
    response2 = client.post("/api/v1/schedule", json=schedule2_data)
    assert response2.status_code == 409
    assert "class" in response2.json()["detail"].lower()


def test_room_conflict_detection(client: TestClient, db: Session):
    """Test that a room cannot be booked twice at the same time."""
    # Create entities
    teacher1_response = client.post(
        "/api/v1/teachers",
        json={
            "first_name": "Maria",
            "last_name": "Müller",
            "email": "maria.mueller@schule.de",
            "abbreviation": "MUE",
            "max_hours_per_week": 28,
            "is_part_time": False,
        },
    )
    teacher1_id = teacher1_response.json()["id"]

    teacher2_response = client.post(
        "/api/v1/teachers",
        json={
            "first_name": "Thomas",
            "last_name": "Schmidt",
            "email": "thomas.schmidt@schule.de",
            "abbreviation": "SCH",
            "max_hours_per_week": 28,
            "is_part_time": False,
        },
    )
    teacher2_id = teacher2_response.json()["id"]

    class1_response = client.post(
        "/api/v1/classes",
        json={"name": "1a", "grade": 1, "size": 20, "home_room": "101"},
    )
    class1_id = class1_response.json()["id"]

    class2_response = client.post(
        "/api/v1/classes",
        json={"name": "1b", "grade": 1, "size": 20, "home_room": "102"},
    )
    class2_id = class2_response.json()["id"]

    subject_response = client.post(
        "/api/v1/subjects",
        json={"name": "Sport", "code": "SP", "color": "#10B981"},
    )
    subject_id = subject_response.json()["id"]

    # Generate timeslots
    client.post("/api/v1/timeslots/generate-default")
    timeslots_response = client.get("/api/v1/timeslots")
    timeslots = timeslots_response.json()
    timeslot_id = timeslots[0]["id"]

    # Create first schedule entry
    schedule1_data = {
        "class_id": class1_id,
        "teacher_id": teacher1_id,
        "subject_id": subject_id,
        "timeslot_id": timeslot_id,
        "room": "Turnhalle",
        "week_type": "ALL",
    }
    response1 = client.post("/api/v1/schedule", json=schedule1_data)
    assert response1.status_code == 201

    # Try to create conflicting schedule entry
    schedule2_data = {
        "class_id": class2_id,
        "teacher_id": teacher2_id,
        "subject_id": subject_id,
        "timeslot_id": timeslot_id,
        "room": "Turnhalle",
        "week_type": "ALL",
    }
    response2 = client.post("/api/v1/schedule", json=schedule2_data)
    assert response2.status_code == 409
    assert "room" in response2.json()["detail"].lower()


def test_break_period_validation(client: TestClient, db: Session):
    """Test that schedule entries cannot be created during break periods."""
    # Create entities
    teacher_response = client.post(
        "/api/v1/teachers",
        json={
            "first_name": "Maria",
            "last_name": "Müller",
            "email": "maria.mueller@schule.de",
            "abbreviation": "MUE",
            "max_hours_per_week": 28,
            "is_part_time": False,
        },
    )
    teacher_id = teacher_response.json()["id"]

    class_response = client.post(
        "/api/v1/classes",
        json={"name": "1a", "grade": 1, "size": 20, "home_room": "101"},
    )
    class_id = class_response.json()["id"]

    subject_response = client.post(
        "/api/v1/subjects",
        json={"name": "Mathematik", "code": "MA", "color": "#2563EB"},
    )
    subject_id = subject_response.json()["id"]

    # Generate timeslots (will include break periods)
    client.post("/api/v1/timeslots/generate-default")
    timeslots_response = client.get("/api/v1/timeslots")
    timeslots = timeslots_response.json()

    # Find a break timeslot
    break_timeslot = next(ts for ts in timeslots if ts["is_break"])

    # Try to create schedule entry during break
    schedule_data = {
        "class_id": class_id,
        "teacher_id": teacher_id,
        "subject_id": subject_id,
        "timeslot_id": break_timeslot["id"],
        "room": "101",
        "week_type": "ALL",
    }
    response = client.post("/api/v1/schedule", json=schedule_data)
    assert response.status_code == 400
    assert "break" in response.json()["detail"].lower()


def test_get_schedule_by_class(client: TestClient, db: Session):
    """Test getting schedule for a specific class."""
    # Create entities
    teacher_response = client.post(
        "/api/v1/teachers",
        json={
            "first_name": "Maria",
            "last_name": "Müller",
            "email": "maria.mueller@schule.de",
            "abbreviation": "MUE",
            "max_hours_per_week": 28,
            "is_part_time": False,
        },
    )
    teacher_id = teacher_response.json()["id"]

    class_response = client.post(
        "/api/v1/classes",
        json={"name": "1a", "grade": 1, "size": 20, "home_room": "101"},
    )
    class_id = class_response.json()["id"]

    subject_response = client.post(
        "/api/v1/subjects",
        json={"name": "Mathematik", "code": "MA", "color": "#2563EB"},
    )
    subject_id = subject_response.json()["id"]

    # Generate timeslots
    client.post("/api/v1/timeslots/generate-default")
    timeslots_response = client.get("/api/v1/timeslots")
    timeslots = timeslots_response.json()
    timeslot_id = timeslots[0]["id"]

    # Create schedule entry
    schedule_data = {
        "class_id": class_id,
        "teacher_id": teacher_id,
        "subject_id": subject_id,
        "timeslot_id": timeslot_id,
        "room": "101",
        "week_type": "ALL",
    }
    client.post("/api/v1/schedule", json=schedule_data)

    # Get schedule by class
    response = client.get(f"/api/v1/schedule/class/{class_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["class"]["id"] == class_id


def test_get_schedule_by_teacher(client: TestClient, db: Session):
    """Test getting schedule for a specific teacher."""
    # Create entities
    teacher_response = client.post(
        "/api/v1/teachers",
        json={
            "first_name": "Maria",
            "last_name": "Müller",
            "email": "maria.mueller@schule.de",
            "abbreviation": "MUE",
            "max_hours_per_week": 28,
            "is_part_time": False,
        },
    )
    teacher_id = teacher_response.json()["id"]

    class_response = client.post(
        "/api/v1/classes",
        json={"name": "1a", "grade": 1, "size": 20, "home_room": "101"},
    )
    class_id = class_response.json()["id"]

    subject_response = client.post(
        "/api/v1/subjects",
        json={"name": "Mathematik", "code": "MA", "color": "#2563EB"},
    )
    subject_id = subject_response.json()["id"]

    # Generate timeslots
    client.post("/api/v1/timeslots/generate-default")
    timeslots_response = client.get("/api/v1/timeslots")
    timeslots = timeslots_response.json()
    timeslot_id = timeslots[0]["id"]

    # Create schedule entry
    schedule_data = {
        "class_id": class_id,
        "teacher_id": teacher_id,
        "subject_id": subject_id,
        "timeslot_id": timeslot_id,
        "room": "101",
        "week_type": "ALL",
    }
    client.post("/api/v1/schedule", json=schedule_data)

    # Get schedule by teacher
    response = client.get(f"/api/v1/schedule/teacher/{teacher_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["teacher"]["id"] == teacher_id


def test_week_type_scheduling(client: TestClient, db: Session):
    """Test A/B week scheduling."""
    # Create entities
    teacher_response = client.post(
        "/api/v1/teachers",
        json={
            "first_name": "Maria",
            "last_name": "Müller",
            "email": "maria.mueller@schule.de",
            "abbreviation": "MUE",
            "max_hours_per_week": 28,
            "is_part_time": False,
        },
    )
    teacher_id = teacher_response.json()["id"]

    class_response = client.post(
        "/api/v1/classes",
        json={"name": "1a", "grade": 1, "size": 20, "home_room": "101"},
    )
    class_id = class_response.json()["id"]

    subject1_response = client.post(
        "/api/v1/subjects",
        json={"name": "Religion", "code": "REL", "color": "#8B5CF6"},
    )
    subject1_id = subject1_response.json()["id"]

    subject2_response = client.post(
        "/api/v1/subjects",
        json={"name": "Ethik", "code": "ETH", "color": "#EC4899"},
    )
    subject2_id = subject2_response.json()["id"]

    # Generate timeslots
    client.post("/api/v1/timeslots/generate-default")
    timeslots_response = client.get("/api/v1/timeslots")
    timeslots = timeslots_response.json()
    timeslot_id = timeslots[0]["id"]

    # Create A week schedule
    schedule_a_data = {
        "class_id": class_id,
        "teacher_id": teacher_id,
        "subject_id": subject1_id,
        "timeslot_id": timeslot_id,
        "room": "101",
        "week_type": "A",
    }
    response_a = client.post("/api/v1/schedule", json=schedule_a_data)
    assert response_a.status_code == 201

    # Create B week schedule (same timeslot, different subject)
    schedule_b_data = {
        "class_id": class_id,
        "teacher_id": teacher_id,
        "subject_id": subject2_id,
        "timeslot_id": timeslot_id,
        "room": "101",
        "week_type": "B",
    }
    response_b = client.post("/api/v1/schedule", json=schedule_b_data)
    assert response_b.status_code == 201

    # Get schedule with week_type filter
    response = client.get("/api/v1/schedule?week_type=A")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["week_type"] == "A"


def test_bulk_schedule_creation(client: TestClient, db: Session):
    """Test creating multiple schedule entries at once."""
    # Create entities
    teacher_response = client.post(
        "/api/v1/teachers",
        json={
            "first_name": "Maria",
            "last_name": "Müller",
            "email": "maria.mueller@schule.de",
            "abbreviation": "MUE",
            "max_hours_per_week": 28,
            "is_part_time": False,
        },
    )
    teacher_id = teacher_response.json()["id"]

    class_response = client.post(
        "/api/v1/classes",
        json={"name": "1a", "grade": 1, "size": 20, "home_room": "101"},
    )
    class_id = class_response.json()["id"]

    subject_response = client.post(
        "/api/v1/subjects",
        json={"name": "Mathematik", "code": "MA", "color": "#2563EB"},
    )
    subject_id = subject_response.json()["id"]

    # Generate timeslots
    client.post("/api/v1/timeslots/generate-default")
    timeslots_response = client.get("/api/v1/timeslots")
    timeslots = timeslots_response.json()
    non_break_slots = [ts for ts in timeslots if not ts["is_break"]][:3]

    # Create bulk schedule data
    bulk_data = [
        {
            "class_id": class_id,
            "teacher_id": teacher_id,
            "subject_id": subject_id,
            "timeslot_id": slot["id"],
            "room": "101",
            "week_type": "ALL",
        }
        for slot in non_break_slots
    ]

    response = client.post("/api/v1/schedule/bulk", json=bulk_data)
    assert response.status_code == 201
    data = response.json()
    assert len(data) == 3


def test_validate_schedule_conflicts(client: TestClient, db: Session):
    """Test schedule validation endpoint."""
    # Create entities
    teacher_response = client.post(
        "/api/v1/teachers",
        json={
            "first_name": "Maria",
            "last_name": "Müller",
            "email": "maria.mueller@schule.de",
            "abbreviation": "MUE",
            "max_hours_per_week": 28,
            "is_part_time": False,
        },
    )
    teacher_id = teacher_response.json()["id"]

    class_response = client.post(
        "/api/v1/classes",
        json={"name": "1a", "grade": 1, "size": 20, "home_room": "101"},
    )
    class_id = class_response.json()["id"]

    subject_response = client.post(
        "/api/v1/subjects",
        json={"name": "Mathematik", "code": "MA", "color": "#2563EB"},
    )
    subject_id = subject_response.json()["id"]

    # Generate timeslots
    client.post("/api/v1/timeslots/generate-default")
    timeslots_response = client.get("/api/v1/timeslots")
    timeslots = timeslots_response.json()
    timeslot_id = timeslots[0]["id"]

    # Create first schedule entry
    schedule_data = {
        "class_id": class_id,
        "teacher_id": teacher_id,
        "subject_id": subject_id,
        "timeslot_id": timeslot_id,
        "room": "101",
        "week_type": "ALL",
    }
    client.post("/api/v1/schedule", json=schedule_data)

    # Validate conflicting entry
    validation_data = {
        "class_id": class_id,
        "teacher_id": teacher_id,
        "subject_id": subject_id,
        "timeslot_id": timeslot_id,
        "room": "102",
        "week_type": "ALL",
    }
    response = client.post("/api/v1/schedule/validate", json=validation_data)
    assert response.status_code == 200
    data = response.json()
    assert data["valid"] is False
    assert len(data["conflicts"]) > 0


def test_update_schedule_entry(client: TestClient, db: Session):
    """Test updating a schedule entry."""
    # Create entities
    teacher_response = client.post(
        "/api/v1/teachers",
        json={
            "first_name": "Maria",
            "last_name": "Müller",
            "email": "maria.mueller@schule.de",
            "abbreviation": "MUE",
            "max_hours_per_week": 28,
            "is_part_time": False,
        },
    )
    teacher_id = teacher_response.json()["id"]

    class_response = client.post(
        "/api/v1/classes",
        json={"name": "1a", "grade": 1, "size": 20, "home_room": "101"},
    )
    class_id = class_response.json()["id"]

    subject_response = client.post(
        "/api/v1/subjects",
        json={"name": "Mathematik", "code": "MA", "color": "#2563EB"},
    )
    subject_id = subject_response.json()["id"]

    # Generate timeslots
    client.post("/api/v1/timeslots/generate-default")
    timeslots_response = client.get("/api/v1/timeslots")
    timeslots = timeslots_response.json()
    non_break_slots = [ts for ts in timeslots if not ts["is_break"]]
    timeslot1_id = non_break_slots[0]["id"]
    timeslot2_id = non_break_slots[1]["id"]

    # Create schedule entry
    schedule_data = {
        "class_id": class_id,
        "teacher_id": teacher_id,
        "subject_id": subject_id,
        "timeslot_id": timeslot1_id,
        "room": "101",
        "week_type": "ALL",
    }
    create_response = client.post("/api/v1/schedule", json=schedule_data)
    schedule_id = create_response.json()["id"]

    # Update schedule entry
    update_data = {
        "timeslot_id": timeslot2_id,
        "room": "102",
    }
    response = client.put(f"/api/v1/schedule/{schedule_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["timeslot"]["id"] == timeslot2_id
    assert data["room"] == "102"


def test_delete_schedule_entry(client: TestClient, db: Session):
    """Test deleting a schedule entry."""
    # Create entities
    teacher_response = client.post(
        "/api/v1/teachers",
        json={
            "first_name": "Maria",
            "last_name": "Müller",
            "email": "maria.mueller@schule.de",
            "abbreviation": "MUE",
            "max_hours_per_week": 28,
            "is_part_time": False,
        },
    )
    teacher_id = teacher_response.json()["id"]

    class_response = client.post(
        "/api/v1/classes",
        json={"name": "1a", "grade": 1, "size": 20, "home_room": "101"},
    )
    class_id = class_response.json()["id"]

    subject_response = client.post(
        "/api/v1/subjects",
        json={"name": "Mathematik", "code": "MA", "color": "#2563EB"},
    )
    subject_id = subject_response.json()["id"]

    # Generate timeslots
    client.post("/api/v1/timeslots/generate-default")
    timeslots_response = client.get("/api/v1/timeslots")
    timeslots = timeslots_response.json()
    timeslot_id = timeslots[0]["id"]

    # Create schedule entry
    schedule_data = {
        "class_id": class_id,
        "teacher_id": teacher_id,
        "subject_id": subject_id,
        "timeslot_id": timeslot_id,
        "room": "101",
        "week_type": "ALL",
    }
    create_response = client.post("/api/v1/schedule", json=schedule_data)
    schedule_id = create_response.json()["id"]

    # Delete schedule entry
    response = client.delete(f"/api/v1/schedule/{schedule_id}")
    assert response.status_code == 204

    # Verify deletion
    get_response = client.get(f"/api/v1/schedule/{schedule_id}")
    assert get_response.status_code == 404


def test_get_room_schedule(client: TestClient, db: Session):
    """Test getting schedule for a specific room."""
    # Create entities
    teacher_response = client.post(
        "/api/v1/teachers",
        json={
            "first_name": "Maria",
            "last_name": "Müller",
            "email": "maria.mueller@schule.de",
            "abbreviation": "MUE",
            "max_hours_per_week": 28,
            "is_part_time": False,
        },
    )
    teacher_id = teacher_response.json()["id"]

    class_response = client.post(
        "/api/v1/classes",
        json={"name": "1a", "grade": 1, "size": 20, "home_room": "101"},
    )
    class_id = class_response.json()["id"]

    subject_response = client.post(
        "/api/v1/subjects",
        json={"name": "Sport", "code": "SP", "color": "#10B981"},
    )
    subject_id = subject_response.json()["id"]

    # Generate timeslots
    client.post("/api/v1/timeslots/generate-default")
    timeslots_response = client.get("/api/v1/timeslots")
    timeslots = timeslots_response.json()
    timeslot_id = timeslots[0]["id"]

    # Create schedule entry
    schedule_data = {
        "class_id": class_id,
        "teacher_id": teacher_id,
        "subject_id": subject_id,
        "timeslot_id": timeslot_id,
        "room": "Turnhalle",
        "week_type": "ALL",
    }
    client.post("/api/v1/schedule", json=schedule_data)

    # Get schedule by room
    response = client.get("/api/v1/schedule/room/Turnhalle")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["room"] == "Turnhalle"


def test_schedule_query_filters(client: TestClient, db: Session):
    """Test schedule filtering by day and week type."""
    # Create entities
    teacher_response = client.post(
        "/api/v1/teachers",
        json={
            "first_name": "Maria",
            "last_name": "Müller",
            "email": "maria.mueller@schule.de",
            "abbreviation": "MUE",
            "max_hours_per_week": 28,
            "is_part_time": False,
        },
    )
    teacher_id = teacher_response.json()["id"]

    class_response = client.post(
        "/api/v1/classes",
        json={"name": "1a", "grade": 1, "size": 20, "home_room": "101"},
    )
    class_id = class_response.json()["id"]

    subject_response = client.post(
        "/api/v1/subjects",
        json={"name": "Mathematik", "code": "MA", "color": "#2563EB"},
    )
    subject_id = subject_response.json()["id"]

    # Generate timeslots
    client.post("/api/v1/timeslots/generate-default")
    timeslots_response = client.get("/api/v1/timeslots")
    timeslots = timeslots_response.json()
    monday_slot = next(ts for ts in timeslots if ts["day"] == 1 and not ts["is_break"])

    # Create schedule entry for Monday
    schedule_data = {
        "class_id": class_id,
        "teacher_id": teacher_id,
        "subject_id": subject_id,
        "timeslot_id": monday_slot["id"],
        "room": "101",
        "week_type": "ALL",
    }
    client.post("/api/v1/schedule", json=schedule_data)

    # Get schedule filtered by day
    response = client.get("/api/v1/schedule?day=1")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["timeslot"]["day"] == 1
