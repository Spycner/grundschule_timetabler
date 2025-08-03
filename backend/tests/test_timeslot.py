"""Tests for TimeSlot model and API endpoints."""

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


def test_create_timeslot(client: TestClient, db: Session):
    """Test creating a new timeslot."""
    timeslot_data = {
        "day": 1,  # Monday
        "period": 1,
        "start_time": "08:00",
        "end_time": "08:45",
        "is_break": False,
    }

    response = client.post("/api/v1/timeslots", json=timeslot_data)
    assert response.status_code == 201

    data = response.json()
    assert data["day"] == timeslot_data["day"]
    assert data["period"] == timeslot_data["period"]
    assert data["start_time"] == "08:00:00"
    assert data["end_time"] == "08:45:00"
    assert data["is_break"] == timeslot_data["is_break"]
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_create_timeslot_duplicate_day_period(client: TestClient, db: Session):
    """Test that duplicate day/period combinations are rejected."""
    timeslot_data = {
        "day": 1,
        "period": 1,
        "start_time": "08:00",
        "end_time": "08:45",
        "is_break": False,
    }

    # Create first timeslot
    response = client.post("/api/v1/timeslots", json=timeslot_data)
    assert response.status_code == 201

    # Try to create second timeslot with same day/period
    timeslot_data["start_time"] = "09:00"  # Different time
    timeslot_data["end_time"] = "09:45"
    response = client.post("/api/v1/timeslots", json=timeslot_data)
    assert response.status_code == 409
    assert "already exists" in response.json()["detail"].lower()


def test_create_timeslot_invalid_day(client: TestClient, db: Session):
    """Test that invalid day values are rejected."""
    # Test day = 0
    timeslot_data = {
        "day": 0,
        "period": 1,
        "start_time": "08:00",
        "end_time": "08:45",
        "is_break": False,
    }
    response = client.post("/api/v1/timeslots", json=timeslot_data)
    assert response.status_code == 422

    # Test day = 6 (Saturday)
    timeslot_data["day"] = 6
    response = client.post("/api/v1/timeslots", json=timeslot_data)
    assert response.status_code == 422


def test_create_timeslot_invalid_time_range(client: TestClient, db: Session):
    """Test that end_time must be after start_time."""
    timeslot_data = {
        "day": 1,
        "period": 1,
        "start_time": "09:00",
        "end_time": "08:00",  # Earlier than start
        "is_break": False,
    }
    response = client.post("/api/v1/timeslots", json=timeslot_data)
    assert response.status_code == 422
    assert "end_time must be after start_time" in response.json()["detail"][0]["msg"]


def test_create_break_timeslot(client: TestClient, db: Session):
    """Test creating a break timeslot."""
    timeslot_data = {
        "day": 1,
        "period": 3,
        "start_time": "09:30",
        "end_time": "09:50",
        "is_break": True,
    }

    response = client.post("/api/v1/timeslots", json=timeslot_data)
    assert response.status_code == 201

    data = response.json()
    assert data["is_break"] is True


def test_get_timeslots(client: TestClient, db: Session):
    """Test getting all timeslots (ordered by day and period)."""
    # Create timeslots in random order
    timeslots = [
        {
            "day": 2,
            "period": 1,
            "start_time": "08:00",
            "end_time": "08:45",
            "is_break": False,
        },
        {
            "day": 1,
            "period": 2,
            "start_time": "08:45",
            "end_time": "09:30",
            "is_break": False,
        },
        {
            "day": 1,
            "period": 1,
            "start_time": "08:00",
            "end_time": "08:45",
            "is_break": False,
        },
    ]

    for timeslot in timeslots:
        response = client.post("/api/v1/timeslots", json=timeslot)
        assert response.status_code == 201

    # Get all timeslots
    response = client.get("/api/v1/timeslots")
    assert response.status_code == 200

    data = response.json()
    assert len(data) >= 3

    # Check ordering: should be Monday period 1, Monday period 2, Tuesday period 1
    ordered_slots = [
        slot for slot in data if slot["day"] in [1, 2] and slot["period"] in [1, 2]
    ]
    assert ordered_slots[0]["day"] == 1 and ordered_slots[0]["period"] == 1
    assert ordered_slots[1]["day"] == 1 and ordered_slots[1]["period"] == 2
    assert ordered_slots[2]["day"] == 2 and ordered_slots[2]["period"] == 1


def test_get_timeslot_by_id(client: TestClient, db: Session):
    """Test getting a specific timeslot by ID."""
    timeslot_data = {
        "day": 1,
        "period": 1,
        "start_time": "08:00",
        "end_time": "08:45",
        "is_break": False,
    }

    # Create timeslot
    response = client.post("/api/v1/timeslots", json=timeslot_data)
    assert response.status_code == 201
    created_id = response.json()["id"]

    # Get by ID
    response = client.get(f"/api/v1/timeslots/{created_id}")
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == created_id
    assert data["day"] == timeslot_data["day"]


def test_get_timeslot_not_found(client: TestClient, db: Session):
    """Test getting a non-existent timeslot."""
    response = client.get("/api/v1/timeslots/9999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_update_timeslot(client: TestClient, db: Session):
    """Test updating a timeslot."""
    # Create timeslot
    timeslot_data = {
        "day": 1,
        "period": 1,
        "start_time": "08:00",
        "end_time": "08:45",
        "is_break": False,
    }
    response = client.post("/api/v1/timeslots", json=timeslot_data)
    assert response.status_code == 201
    created_id = response.json()["id"]

    # Update timeslot
    update_data = {
        "start_time": "08:15",
        "end_time": "09:00",
    }
    response = client.put(f"/api/v1/timeslots/{created_id}", json=update_data)
    assert response.status_code == 200

    data = response.json()
    assert data["start_time"] == "08:15:00"
    assert data["end_time"] == "09:00:00"
    assert data["day"] == timeslot_data["day"]  # Unchanged


def test_delete_timeslot(client: TestClient, db: Session):
    """Test deleting a timeslot."""
    # Create timeslot
    timeslot_data = {
        "day": 1,
        "period": 1,
        "start_time": "08:00",
        "end_time": "08:45",
        "is_break": False,
    }
    response = client.post("/api/v1/timeslots", json=timeslot_data)
    assert response.status_code == 201
    created_id = response.json()["id"]

    # Delete timeslot
    response = client.delete(f"/api/v1/timeslots/{created_id}")
    assert response.status_code == 204

    # Verify it's deleted
    response = client.get(f"/api/v1/timeslots/{created_id}")
    assert response.status_code == 404


def test_generate_default_schedule(client: TestClient, db: Session):
    """Test generating a default weekly schedule."""
    response = client.post("/api/v1/timeslots/generate-default")
    assert response.status_code == 201

    data = response.json()
    assert "message" in data
    assert data["count"] == 40  # 5 days x 8 slots (6 periods + 2 breaks)

    # Verify the timeslots were created
    response = client.get("/api/v1/timeslots")
    assert response.status_code == 200

    timeslots = response.json()
    assert len(timeslots) >= 40

    # Check for breaks
    breaks = [slot for slot in timeslots if slot["is_break"]]
    assert len(breaks) >= 10  # 2 breaks per day x 5 days

    # Check Monday's schedule
    monday = [slot for slot in timeslots if slot["day"] == 1]
    assert len(monday) == 8  # 6 periods + 2 breaks

    # Verify periods are ordered correctly
    monday_sorted = sorted(monday, key=lambda x: x["period"])
    assert monday_sorted[0]["period"] == 1
    assert monday_sorted[0]["start_time"] == "08:00:00"
    assert monday_sorted[-1]["period"] == 8


def test_check_time_overlap(client: TestClient, db: Session):
    """Test that overlapping time ranges on the same day are detected."""
    # Create first timeslot
    timeslot1 = {
        "day": 1,
        "period": 1,
        "start_time": "08:00",
        "end_time": "08:45",
        "is_break": False,
    }
    response = client.post("/api/v1/timeslots", json=timeslot1)
    assert response.status_code == 201

    # Try to create overlapping timeslot
    timeslot2 = {
        "day": 1,
        "period": 2,
        "start_time": "08:30",  # Overlaps with first
        "end_time": "09:15",
        "is_break": False,
    }
    response = client.post("/api/v1/timeslots", json=timeslot2)
    assert response.status_code == 409
    assert "overlap" in response.json()["detail"].lower()


def test_timeslot_period_validation(client: TestClient, db: Session):
    """Test that period must be a positive integer."""
    timeslot_data = {
        "day": 1,
        "period": 0,  # Invalid
        "start_time": "08:00",
        "end_time": "08:45",
        "is_break": False,
    }
    response = client.post("/api/v1/timeslots", json=timeslot_data)
    assert response.status_code == 422

    timeslot_data["period"] = -1  # Also invalid
    response = client.post("/api/v1/timeslots", json=timeslot_data)
    assert response.status_code == 422
