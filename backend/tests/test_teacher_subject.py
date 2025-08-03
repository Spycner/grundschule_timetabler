"""Tests for TeacherSubject model and API endpoints."""

from datetime import UTC, datetime

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


def test_create_teacher_subject_assignment(client: TestClient, db: Session):
    """Test creating a teacher-subject assignment."""
    # First create a teacher
    teacher_data = {
        "first_name": "Maria",
        "last_name": "Schmidt",
        "email": "maria.schmidt@schule.de",
        "abbreviation": "SCH",
        "max_hours_per_week": 28,
        "is_part_time": False,
    }
    teacher_response = client.post("/api/v1/teachers", json=teacher_data)
    assert teacher_response.status_code == 201
    teacher_id = teacher_response.json()["id"]

    # Create a subject
    subject_data = {"name": "Mathematik", "code": "MA", "color": "#FF5733"}
    subject_response = client.post("/api/v1/subjects", json=subject_data)
    assert subject_response.status_code == 201
    subject_id = subject_response.json()["id"]

    # Assign subject to teacher
    assignment_data = {
        "subject_id": subject_id,
        "qualification_level": "PRIMARY",
        "grades": [1, 2, 3, 4],
        "max_hours_per_week": 10,
    }
    response = client.post(
        f"/api/v1/teachers/{teacher_id}/subjects", json=assignment_data
    )
    assert response.status_code == 201

    data = response.json()
    assert data["teacher_id"] == teacher_id
    assert data["subject_id"] == subject_id
    assert data["qualification_level"] == "PRIMARY"
    assert data["grades"] == [1, 2, 3, 4]
    assert data["max_hours_per_week"] == 10
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_create_assignment_with_certification(client: TestClient, db: Session):
    """Test creating assignment with certification details."""
    # Create teacher and subject
    teacher_response = client.post(
        "/api/v1/teachers",
        json={
            "first_name": "Hans",
            "last_name": "Weber",
            "email": "hans.weber@schule.de",
            "abbreviation": "WEB",
            "max_hours_per_week": 28,
        },
    )
    teacher_id = teacher_response.json()["id"]

    subject_response = client.post(
        "/api/v1/subjects", json={"name": "Sport", "code": "SP", "color": "#00FF00"}
    )
    subject_id = subject_response.json()["id"]

    # Assign with certification
    assignment_data = {
        "subject_id": subject_id,
        "qualification_level": "PRIMARY",
        "grades": [1, 2, 3, 4],
        "certification_date": "2020-09-01",
        "certification_expires": "2025-08-31",
        "certification_document": "Sport Teaching Certificate",
    }
    response = client.post(
        f"/api/v1/teachers/{teacher_id}/subjects", json=assignment_data
    )
    assert response.status_code == 201

    data = response.json()
    assert data["certification_date"] == "2020-09-01"
    assert data["certification_expires"] == "2025-08-31"
    assert data["certification_document"] == "Sport Teaching Certificate"


def test_get_teacher_subjects(client: TestClient, db: Session):
    """Test getting all subjects for a teacher."""
    # Create teacher
    teacher_response = client.post(
        "/api/v1/teachers",
        json={
            "first_name": "Anna",
            "last_name": "Meyer",
            "email": "anna.meyer@schule.de",
            "abbreviation": "MEY",
            "max_hours_per_week": 28,
        },
    )
    teacher_id = teacher_response.json()["id"]

    # Create multiple subjects
    subjects = []
    for name, code in [("Deutsch", "DE"), ("Englisch", "EN"), ("Kunst", "KU")]:
        resp = client.post(
            "/api/v1/subjects", json={"name": name, "code": code, "color": "#FF0000"}
        )
        subjects.append(resp.json())

    # Assign subjects with different qualification levels
    for i, subject in enumerate(subjects):
        level = ["PRIMARY", "SECONDARY", "SUBSTITUTE"][i]
        client.post(
            f"/api/v1/teachers/{teacher_id}/subjects",
            json={
                "subject_id": subject["id"],
                "qualification_level": level,
                "grades": [1, 2, 3, 4],
            },
        )

    # Get teacher's subjects
    response = client.get(f"/api/v1/teachers/{teacher_id}/subjects")
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 3
    assert {item["qualification_level"] for item in data} == {
        "PRIMARY",
        "SECONDARY",
        "SUBSTITUTE",
    }


def test_update_teacher_subject_assignment(client: TestClient, db: Session):
    """Test updating a teacher-subject assignment."""
    # Create teacher and subject
    teacher_response = client.post(
        "/api/v1/teachers",
        json={
            "first_name": "Peter",
            "last_name": "Müller",
            "email": "peter.mueller@schule.de",
            "abbreviation": "MUL",
            "max_hours_per_week": 28,
        },
    )
    teacher_id = teacher_response.json()["id"]

    subject_response = client.post(
        "/api/v1/subjects",
        json={"name": "Sachunterricht", "code": "SU", "color": "#0000FF"},
    )
    subject_id = subject_response.json()["id"]

    # Create assignment
    client.post(
        f"/api/v1/teachers/{teacher_id}/subjects",
        json={
            "subject_id": subject_id,
            "qualification_level": "SECONDARY",
            "grades": [1, 2],
        },
    )

    # Update assignment
    update_data = {
        "qualification_level": "PRIMARY",
        "grades": [1, 2, 3, 4],
        "max_hours_per_week": 15,
    }
    response = client.put(
        f"/api/v1/teachers/{teacher_id}/subjects/{subject_id}", json=update_data
    )
    assert response.status_code == 200

    data = response.json()
    assert data["qualification_level"] == "PRIMARY"
    assert data["grades"] == [1, 2, 3, 4]
    assert data["max_hours_per_week"] == 15


def test_delete_teacher_subject_assignment(client: TestClient, db: Session):
    """Test deleting a teacher-subject assignment."""
    # Create teacher and subject
    teacher_response = client.post(
        "/api/v1/teachers",
        json={
            "first_name": "Julia",
            "last_name": "Becker",
            "email": "julia.becker@schule.de",
            "abbreviation": "BEC",
            "max_hours_per_week": 28,
        },
    )
    teacher_id = teacher_response.json()["id"]

    subject_response = client.post(
        "/api/v1/subjects", json={"name": "Musik", "code": "MU", "color": "#FFD700"}
    )
    subject_id = subject_response.json()["id"]

    # Create assignment
    client.post(
        f"/api/v1/teachers/{teacher_id}/subjects",
        json={
            "subject_id": subject_id,
            "qualification_level": "PRIMARY",
            "grades": [1, 2, 3, 4],
        },
    )

    # Delete assignment
    response = client.delete(f"/api/v1/teachers/{teacher_id}/subjects/{subject_id}")
    assert response.status_code == 204

    # Verify deletion
    response = client.get(f"/api/v1/teachers/{teacher_id}/subjects")
    assert response.status_code == 200
    assert len(response.json()) == 0


def test_duplicate_assignment_rejected(client: TestClient, db: Session):
    """Test that duplicate teacher-subject assignments are rejected."""
    # Create teacher and subject
    teacher_response = client.post(
        "/api/v1/teachers",
        json={
            "first_name": "Thomas",
            "last_name": "Wagner",
            "email": "thomas.wagner@schule.de",
            "abbreviation": "WAG",
            "max_hours_per_week": 28,
        },
    )
    teacher_id = teacher_response.json()["id"]

    subject_response = client.post(
        "/api/v1/subjects",
        json={"name": "Religion", "code": "RE", "color": "#800080"},
    )
    subject_id = subject_response.json()["id"]

    # Create first assignment
    assignment_data = {
        "subject_id": subject_id,
        "qualification_level": "PRIMARY",
        "grades": [1, 2, 3, 4],
    }
    response = client.post(
        f"/api/v1/teachers/{teacher_id}/subjects", json=assignment_data
    )
    assert response.status_code == 201

    # Try to create duplicate
    response = client.post(
        f"/api/v1/teachers/{teacher_id}/subjects", json=assignment_data
    )
    assert response.status_code == 409
    assert "already assigned" in response.json()["detail"].lower()


def test_get_qualified_teachers_for_subject(client: TestClient, db: Session):
    """Test finding all teachers qualified for a subject."""
    # Create subject
    subject_response = client.post(
        "/api/v1/subjects",
        json={"name": "Informatik", "code": "INF", "color": "#4B0082"},
    )
    subject_id = subject_response.json()["id"]

    # Create multiple teachers and assign them to the subject
    teachers = []
    for _i, (first, last, email, abbr, level) in enumerate(
        [
            ("Laura", "Schmidt", "laura.s@schule.de", "LSC", "PRIMARY"),
            ("Max", "Fischer", "max.f@schule.de", "FIS", "SECONDARY"),
            ("Sophie", "Klein", "sophie.k@schule.de", "KLE", "SUBSTITUTE"),
        ]
    ):
        teacher_resp = client.post(
            "/api/v1/teachers",
            json={
                "first_name": first,
                "last_name": last,
                "email": email,
                "abbreviation": abbr,
                "max_hours_per_week": 28,
            },
        )
        teacher_id = teacher_resp.json()["id"]
        teachers.append(teacher_resp.json())

        # Assign to subject
        client.post(
            f"/api/v1/teachers/{teacher_id}/subjects",
            json={
                "subject_id": subject_id,
                "qualification_level": level,
                "grades": [1, 2, 3, 4],
            },
        )

    # Get qualified teachers
    response = client.get(f"/api/v1/subjects/{subject_id}/teachers")
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 3
    # Should be sorted by qualification level (PRIMARY first)
    assert data[0]["qualification_level"] == "PRIMARY"
    assert data[1]["qualification_level"] == "SECONDARY"
    assert data[2]["qualification_level"] == "SUBSTITUTE"


def test_get_teachers_by_grade(client: TestClient, db: Session):
    """Test finding teachers qualified for specific grades."""
    # Create subject
    subject_response = client.post(
        "/api/v1/subjects",
        json={"name": "Werken", "code": "WE", "color": "#8B4513"},
    )
    subject_id = subject_response.json()["id"]

    # Create teachers with different grade qualifications
    teacher1_resp = client.post(
        "/api/v1/teachers",
        json={
            "first_name": "Eva",
            "last_name": "Braun",
            "email": "eva.braun@schule.de",
            "abbreviation": "BRA",
            "max_hours_per_week": 28,
        },
    )
    teacher1_id = teacher1_resp.json()["id"]

    teacher2_resp = client.post(
        "/api/v1/teachers",
        json={
            "first_name": "Karl",
            "last_name": "Schwarz",
            "email": "karl.schwarz@schule.de",
            "abbreviation": "SCW",
            "max_hours_per_week": 28,
        },
    )
    teacher2_id = teacher2_resp.json()["id"]

    # Assign with different grades
    client.post(
        f"/api/v1/teachers/{teacher1_id}/subjects",
        json={
            "subject_id": subject_id,
            "qualification_level": "PRIMARY",
            "grades": [1, 2],  # Only grades 1-2
        },
    )

    client.post(
        f"/api/v1/teachers/{teacher2_id}/subjects",
        json={
            "subject_id": subject_id,
            "qualification_level": "PRIMARY",
            "grades": [3, 4],  # Only grades 3-4
        },
    )

    # Get teachers for grade 1
    response = client.get(f"/api/v1/subjects/{subject_id}/teachers/by-grade/1")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["teacher"]["email"] == "eva.braun@schule.de"

    # Get teachers for grade 3
    response = client.get(f"/api/v1/subjects/{subject_id}/teachers/by-grade/3")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["teacher"]["email"] == "karl.schwarz@schule.de"


def test_invalid_grade_rejected(client: TestClient, db: Session):
    """Test that invalid grades are rejected."""
    # Create teacher and subject
    teacher_response = client.post(
        "/api/v1/teachers",
        json={
            "first_name": "Nina",
            "last_name": "Wolf",
            "email": "nina.wolf@schule.de",
            "abbreviation": "WOL",
            "max_hours_per_week": 28,
        },
    )
    teacher_id = teacher_response.json()["id"]

    subject_response = client.post(
        "/api/v1/subjects",
        json={"name": "Ethik", "code": "ETH", "color": "#DAA520"},
    )
    subject_id = subject_response.json()["id"]

    # Try with invalid grades
    assignment_data = {
        "subject_id": subject_id,
        "qualification_level": "PRIMARY",
        "grades": [0, 5],  # Invalid: should be 1-4
    }
    response = client.post(
        f"/api/v1/teachers/{teacher_id}/subjects", json=assignment_data
    )
    assert response.status_code == 422


def test_invalid_qualification_level_rejected(client: TestClient, db: Session):
    """Test that invalid qualification levels are rejected."""
    # Create teacher and subject
    teacher_response = client.post(
        "/api/v1/teachers",
        json={
            "first_name": "Lisa",
            "last_name": "Hoffmann",
            "email": "lisa.hoffmann@schule.de",
            "abbreviation": "HOF",
            "max_hours_per_week": 28,
        },
    )
    teacher_id = teacher_response.json()["id"]

    subject_response = client.post(
        "/api/v1/subjects",
        json={"name": "Chemie", "code": "CH", "color": "#DC143C"},
    )
    subject_id = subject_response.json()["id"]

    # Try with invalid qualification level
    assignment_data = {
        "subject_id": subject_id,
        "qualification_level": "EXPERT",  # Invalid
        "grades": [1, 2, 3, 4],
    }
    response = client.post(
        f"/api/v1/teachers/{teacher_id}/subjects", json=assignment_data
    )
    assert response.status_code == 422


def test_qualification_matrix(client: TestClient, db: Session):
    """Test getting the full qualification matrix."""
    # Create teachers
    teachers = []
    for name, email, abbr in [
        ("Robert Meier", "robert.m@schule.de", "RME"),
        ("Sabine Lang", "sabine.l@schule.de", "LAN"),
    ]:
        first, last = name.split()
        resp = client.post(
            "/api/v1/teachers",
            json={
                "first_name": first,
                "last_name": last,
                "email": email,
                "abbreviation": abbr,
                "max_hours_per_week": 28,
            },
        )
        teachers.append(resp.json())

    # Create subjects
    subjects = []
    for name, code in [("Physik", "PH"), ("Biologie", "BIO")]:
        resp = client.post(
            "/api/v1/subjects", json={"name": name, "code": code, "color": "#000000"}
        )
        subjects.append(resp.json())

    # Create assignments
    for teacher in teachers:
        for subject in subjects:
            client.post(
                f"/api/v1/teachers/{teacher['id']}/subjects",
                json={
                    "subject_id": subject["id"],
                    "qualification_level": "PRIMARY",
                    "grades": [1, 2, 3, 4],
                },
            )

    # Get matrix
    response = client.get("/api/v1/teacher-subjects/matrix")
    assert response.status_code == 200

    data = response.json()
    assert "teachers" in data
    assert "subjects" in data
    assert "assignments" in data
    assert len(data["teachers"]) == 2
    assert len(data["subjects"]) == 2
    assert len(data["assignments"]) == 4


def test_workload_calculation(client: TestClient, db: Session):
    """Test calculating teacher workload across subjects."""
    # Create teacher
    teacher_response = client.post(
        "/api/v1/teachers",
        json={
            "first_name": "Frank",
            "last_name": "Zimmer",
            "email": "frank.zimmer@schule.de",
            "abbreviation": "ZIM",
            "max_hours_per_week": 28,
        },
    )
    teacher_id = teacher_response.json()["id"]

    # Create subjects and assign with hours
    subjects_data = [
        ("Geschichte", "GE", 8),
        ("Erdkunde", "EK", 6),
        ("Politik", "PO", 4),
    ]

    for name, code, hours in subjects_data:
        subject_resp = client.post(
            "/api/v1/subjects", json={"name": name, "code": code, "color": "#FF0000"}
        )
        subject_id = subject_resp.json()["id"]

        client.post(
            f"/api/v1/teachers/{teacher_id}/subjects",
            json={
                "subject_id": subject_id,
                "qualification_level": "PRIMARY",
                "grades": [1, 2, 3, 4],
                "max_hours_per_week": hours,
            },
        )

    # Get workload
    response = client.get(f"/api/v1/teachers/{teacher_id}/workload")
    assert response.status_code == 200

    data = response.json()
    assert data["teacher_id"] == teacher_id
    assert data["total_assigned_hours"] == 18
    assert data["max_hours_per_week"] == 28
    assert data["available_hours"] == 10
    assert len(data["subjects"]) == 3


def test_expired_certification_warning(client: TestClient, db: Session):
    """Test that expired certifications generate warnings."""
    # Create teacher and subject
    teacher_response = client.post(
        "/api/v1/teachers",
        json={
            "first_name": "Claudia",
            "last_name": "Richter",
            "email": "claudia.richter@schule.de",
            "abbreviation": "RIC",
            "max_hours_per_week": 28,
        },
    )
    teacher_id = teacher_response.json()["id"]

    subject_response = client.post(
        "/api/v1/subjects",
        json={"name": "Schwimmen", "code": "SCH", "color": "#00CED1"},
    )
    subject_id = subject_response.json()["id"]

    # Assign with expired certification
    assignment_data = {
        "subject_id": subject_id,
        "qualification_level": "PRIMARY",
        "grades": [1, 2, 3, 4],
        "certification_date": "2018-09-01",
        "certification_expires": "2021-08-31",  # Expired
    }
    response = client.post(
        f"/api/v1/teachers/{teacher_id}/subjects", json=assignment_data
    )
    assert response.status_code == 201

    # Check for warning in response
    data = response.json()
    assert "warnings" in data or data["certification_expires"] < str(
        datetime.now(UTC).date()
    )


def test_schedule_validation_with_qualifications(client: TestClient, db: Session):
    """Test that schedule creation validates teacher qualifications."""
    # Clean up any existing data first
    from sqlalchemy import text

    db.execute(text("DELETE FROM schedules"))
    db.execute(text("DELETE FROM teacher_availability"))
    db.commit()

    # Create teacher without qualification
    teacher_response = client.post(
        "/api/v1/teachers",
        json={
            "first_name": "Martin",
            "last_name": "Krause",
            "email": "martin.krause@schule.de",
            "abbreviation": "KRA",
            "max_hours_per_week": 28,
        },
    )
    teacher_id = teacher_response.json()["id"]

    # Create subject
    subject_response = client.post(
        "/api/v1/subjects",
        json={"name": "Latein", "code": "LAT", "color": "#B22222"},
    )
    subject_id = subject_response.json()["id"]

    # Create class and timeslot
    class_response = client.post(
        "/api/v1/classes",
        json={"name": "4a", "grade": 4, "size": 25, "home_room": "204"},
    )
    class_id = class_response.json()["id"]

    timeslot_response = client.post(
        "/api/v1/timeslots",
        json={
            "day": 1,  # Monday
            "period": 1,
            "start_time": "08:00",
            "end_time": "08:45",
        },
    )
    timeslot_id = timeslot_response.json()["id"]

    # Try to create schedule without qualification
    schedule_data = {
        "class_id": class_id,
        "teacher_id": teacher_id,
        "subject_id": subject_id,
        "timeslot_id": timeslot_id,
        "room": "204",
    }
    response = client.post("/api/v1/schedule", json=schedule_data)
    assert response.status_code == 400
    assert "not qualified" in response.json()["detail"].lower()

    # Now add qualification and retry
    client.post(
        f"/api/v1/teachers/{teacher_id}/subjects",
        json={
            "subject_id": subject_id,
            "qualification_level": "PRIMARY",
            "grades": [4],
        },
    )

    # Should work now
    response = client.post("/api/v1/schedule", json=schedule_data)
    assert response.status_code == 201
