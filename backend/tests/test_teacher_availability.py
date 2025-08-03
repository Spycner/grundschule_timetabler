"""Tests for TeacherAvailability model and API endpoints."""

from datetime import date

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.models.teacher import Teacher
from src.models.teacher_availability import AvailabilityType, TeacherAvailability


class TestTeacherAvailabilityModel:
    """Test TeacherAvailability model functionality."""

    def test_create_availability(self, db: Session):
        """Test creating a teacher availability entry."""
        # Create a teacher first
        teacher = Teacher(
            first_name="Maria",
            last_name="Müller",
            email="maria.mueller@schule.de",
            abbreviation="MUE",
            max_hours_per_week=28,
            is_part_time=False,
        )
        db.add(teacher)
        db.commit()
        db.refresh(teacher)

        # Create availability
        availability = TeacherAvailability(
            teacher_id=teacher.id,
            weekday=0,  # Monday
            period=1,  # First period
            availability_type=AvailabilityType.AVAILABLE,
            effective_from=date(2020, 1, 1),
        )
        db.add(availability)
        db.commit()
        db.refresh(availability)

        assert availability.id is not None
        assert availability.teacher_id == teacher.id
        assert availability.weekday == 0
        assert availability.period == 1
        assert availability.availability_type == AvailabilityType.AVAILABLE
        assert availability.effective_from == date(2020, 1, 1)
        assert availability.effective_until is None

    def test_availability_types(self, db: Session):
        """Test different availability types."""
        # Create a teacher
        teacher = Teacher(
            first_name="Hans",
            last_name="Schmidt",
            email="hans.schmidt@schule.de",
            abbreviation="SCH",
            max_hours_per_week=20,
            is_part_time=True,
        )
        db.add(teacher)
        db.commit()

        # Test all availability types
        for av_type in [
            AvailabilityType.AVAILABLE,
            AvailabilityType.BLOCKED,
            AvailabilityType.PREFERRED,
        ]:
            availability = TeacherAvailability(
                teacher_id=teacher.id,
                weekday=1,
                period=2,
                availability_type=av_type,
                effective_from=date(2020, 1, 1),
            )
            db.add(availability)
            db.commit()
            assert availability.availability_type == av_type
            db.delete(availability)
            db.commit()

    def test_weekday_validation(self, db: Session):
        """Test weekday validation (0-4 for Monday-Friday)."""
        teacher = Teacher(
            first_name="Test",
            last_name="Teacher",
            email="test@schule.de",
            abbreviation="TT1",
            max_hours_per_week=28,
        )
        db.add(teacher)
        db.commit()

        # Valid weekdays (0-4)
        for day in range(5):
            availability = TeacherAvailability(
                teacher_id=teacher.id,
                weekday=day,
                period=1,
                availability_type=AvailabilityType.AVAILABLE,
                effective_from=date(2020, 1, 1),
            )
            db.add(availability)
            db.commit()
            assert availability.weekday == day
            db.delete(availability)
            db.commit()

    def test_period_validation(self, db: Session):
        """Test period validation (1-8)."""
        teacher = Teacher(
            first_name="Test",
            last_name="Teacher2",
            email="test2@schule.de",
            abbreviation="TT2",
            max_hours_per_week=28,
        )
        db.add(teacher)
        db.commit()

        # Valid periods (1-8)
        for period in range(1, 9):
            availability = TeacherAvailability(
                teacher_id=teacher.id,
                weekday=0,
                period=period,
                availability_type=AvailabilityType.AVAILABLE,
                effective_from=date(2020, 1, 1),
            )
            db.add(availability)
            db.commit()
            assert availability.period == period
            db.delete(availability)
            db.commit()

    def test_date_range(self, db: Session):
        """Test effective date range functionality."""
        teacher = Teacher(
            first_name="Date",
            last_name="Test",
            email="date.test@schule.de",
            abbreviation="DT1",
            max_hours_per_week=28,
        )
        db.add(teacher)
        db.commit()

        # Test with end date
        availability = TeacherAvailability(
            teacher_id=teacher.id,
            weekday=2,
            period=3,
            availability_type=AvailabilityType.BLOCKED,
            effective_from=date(2020, 1, 1),
            effective_until=date(2020, 6, 30),
            reason="Elternzeit",
        )
        db.add(availability)
        db.commit()

        assert availability.effective_from == date(2020, 1, 1)
        assert availability.effective_until == date(2020, 6, 30)
        assert availability.reason == "Elternzeit"

    def test_unique_constraint(self, db: Session):
        """Test unique constraint per teacher/weekday/period/date."""
        teacher = Teacher(
            first_name="Unique",
            last_name="Test",
            email="unique.test@schule.de",
            abbreviation="UT1",
            max_hours_per_week=28,
        )
        db.add(teacher)
        db.commit()

        # Create first availability
        availability1 = TeacherAvailability(
            teacher_id=teacher.id,
            weekday=3,
            period=4,
            availability_type=AvailabilityType.AVAILABLE,
            effective_from=date(2020, 1, 1),
        )
        db.add(availability1)
        db.commit()

        # Try to create duplicate (should fail)
        availability2 = TeacherAvailability(
            teacher_id=teacher.id,
            weekday=3,
            period=4,
            availability_type=AvailabilityType.BLOCKED,
            effective_from=date(2020, 1, 1),
        )
        db.add(availability2)
        with pytest.raises(Exception):  # Should raise IntegrityError  # noqa: B017
            db.commit()
        db.rollback()


class TestTeacherAvailabilityAPI:
    """Test TeacherAvailability API endpoints."""

    def test_create_availability_endpoint(self, client: TestClient, db: Session):  # noqa: ARG002
        """Test creating availability via API."""
        # Create a teacher first
        teacher_data = {
            "first_name": "API",
            "last_name": "Teacher",
            "email": "api.teacher@schule.de",
            "abbreviation": "API",
            "max_hours_per_week": 28,
            "is_part_time": False,
        }
        response = client.post("/api/v1/teachers", json=teacher_data)
        assert response.status_code == 201
        teacher_id = response.json()["id"]

        # Create availability
        availability_data = {
            "weekday": 0,
            "period": 1,
            "availability_type": "AVAILABLE",
            "effective_from": "2020-01-01",
        }
        response = client.post(
            f"/api/v1/teachers/{teacher_id}/availability", json=availability_data
        )
        assert response.status_code == 201

        data = response.json()
        assert data["weekday"] == 0
        assert data["period"] == 1
        assert data["availability_type"] == "AVAILABLE"
        assert data["teacher_id"] == teacher_id

    def test_get_teacher_availability(self, client: TestClient, db: Session):  # noqa: ARG002
        """Test getting all availability for a teacher."""
        # Create teacher
        teacher_data = {
            "first_name": "Get",
            "last_name": "Test",
            "email": "get.test@schule.de",
            "abbreviation": "GT1",
            "max_hours_per_week": 20,
            "is_part_time": True,
        }
        response = client.post("/api/v1/teachers", json=teacher_data)
        teacher_id = response.json()["id"]

        # Create multiple availability entries
        for day in range(3):  # Monday to Wednesday
            for period in [1, 2, 3]:
                availability_data = {
                    "weekday": day,
                    "period": period,
                    "availability_type": "AVAILABLE" if period < 3 else "BLOCKED",
                    "effective_from": "2020-01-01",
                }
                response = client.post(
                    f"/api/v1/teachers/{teacher_id}/availability",
                    json=availability_data,
                )
                assert response.status_code == 201

        # Get all availability
        response = client.get(f"/api/v1/teachers/{teacher_id}/availability")
        assert response.status_code == 200

        data = response.json()
        assert len(data) == 9  # 3 days * 3 periods

    def test_update_availability(self, client: TestClient, db: Session):  # noqa: ARG002
        """Test updating an availability entry."""
        # Create teacher
        teacher_data = {
            "first_name": "Update",
            "last_name": "Test",
            "email": "update.test@schule.de",
            "abbreviation": "UT2",
            "max_hours_per_week": 28,
        }
        response = client.post("/api/v1/teachers", json=teacher_data)
        teacher_id = response.json()["id"]

        # Create availability
        availability_data = {
            "weekday": 1,
            "period": 2,
            "availability_type": "AVAILABLE",
            "effective_from": "2020-01-01",
        }
        response = client.post(
            f"/api/v1/teachers/{teacher_id}/availability", json=availability_data
        )
        availability_id = response.json()["id"]

        # Update availability
        update_data = {
            "availability_type": "BLOCKED",
            "reason": "Doctor appointment",
        }
        response = client.put(
            f"/api/v1/teachers/{teacher_id}/availability/{availability_id}",
            json=update_data,
        )
        assert response.status_code == 200

        data = response.json()
        assert data["availability_type"] == "BLOCKED"
        assert data["reason"] == "Doctor appointment"

    def test_delete_availability(self, client: TestClient, db: Session):  # noqa: ARG002
        """Test deleting an availability entry."""
        # Create teacher
        teacher_data = {
            "first_name": "Delete",
            "last_name": "Test",
            "email": "delete.test@schule.de",
            "abbreviation": "DT2",
            "max_hours_per_week": 28,
        }
        response = client.post("/api/v1/teachers", json=teacher_data)
        teacher_id = response.json()["id"]

        # Create availability
        availability_data = {
            "weekday": 2,
            "period": 3,
            "availability_type": "AVAILABLE",
            "effective_from": "2020-01-01",
        }
        response = client.post(
            f"/api/v1/teachers/{teacher_id}/availability", json=availability_data
        )
        availability_id = response.json()["id"]

        # Delete availability
        response = client.delete(
            f"/api/v1/teachers/{teacher_id}/availability/{availability_id}"
        )
        assert response.status_code == 204

        # Verify it's deleted
        response = client.get(f"/api/v1/teachers/{teacher_id}/availability")
        assert len(response.json()) == 0

    def test_bulk_import_availability(self, client: TestClient, db: Session):  # noqa: ARG002
        """Test bulk importing availability data."""
        # Create teacher
        teacher_data = {
            "first_name": "Bulk",
            "last_name": "Import",
            "email": "bulk.import@schule.de",
            "abbreviation": "BI1",
            "max_hours_per_week": 20,
            "is_part_time": True,
        }
        response = client.post("/api/v1/teachers", json=teacher_data)
        teacher_id = response.json()["id"]

        # Bulk import data
        bulk_data = {
            "teacher_id": teacher_id,
            "availabilities": [
                {
                    "weekday": 0,
                    "period": 1,
                    "availability_type": "AVAILABLE",
                    "effective_from": "2020-01-01",
                },
                {
                    "weekday": 0,
                    "period": 2,
                    "availability_type": "AVAILABLE",
                    "effective_from": "2020-01-01",
                },
                {
                    "weekday": 1,
                    "period": 1,
                    "availability_type": "BLOCKED",
                    "effective_from": "2020-01-01",
                    "reason": "Part-time schedule",
                },
            ],
        }
        response = client.post("/api/v1/teachers/availability/bulk", json=bulk_data)
        assert response.status_code == 201

        data = response.json()
        assert data["created_count"] == 3

    def test_availability_overview(self, client: TestClient, db: Session):  # noqa: ARG002
        """Test getting availability overview for all teachers."""
        # Create multiple teachers with availability
        for i in range(2):
            teacher_data = {
                "first_name": f"Teacher{i}",
                "last_name": "Overview",
                "email": f"teacher{i}.overview@schule.de",
                "abbreviation": f"TO{i}",
                "max_hours_per_week": 28 if i == 0 else 20,
                "is_part_time": i == 1,
            }
            response = client.post("/api/v1/teachers", json=teacher_data)
            teacher_id = response.json()["id"]

            # Add availability
            availability_data = {
                "weekday": i,
                "period": 1,
                "availability_type": "AVAILABLE" if i == 0 else "BLOCKED",
                "effective_from": "2020-01-01",
            }
            client.post(
                f"/api/v1/teachers/{teacher_id}/availability", json=availability_data
            )

        # Get overview
        response = client.get("/api/v1/teachers/availability/overview")
        assert response.status_code == 200

        data = response.json()
        assert "teachers" in data
        assert len(data["teachers"]) >= 2

    def test_filter_availability_by_day(self, client: TestClient, db: Session):  # noqa: ARG002
        """Test filtering availability by weekday."""
        # Create teacher
        teacher_data = {
            "first_name": "Filter",
            "last_name": "Day",
            "email": "filter.day@schule.de",
            "abbreviation": "FD1",
            "max_hours_per_week": 28,
        }
        response = client.post("/api/v1/teachers", json=teacher_data)
        teacher_id = response.json()["id"]

        # Add availability for different days
        for day in range(3):
            availability_data = {
                "weekday": day,
                "period": 1,
                "availability_type": "AVAILABLE",
                "effective_from": "2020-01-01",
            }
            client.post(
                f"/api/v1/teachers/{teacher_id}/availability", json=availability_data
            )

        # Filter by Monday (weekday=0)
        response = client.get(f"/api/v1/teachers/{teacher_id}/availability?weekday=0")
        assert response.status_code == 200

        data = response.json()
        assert len(data) == 1
        assert data[0]["weekday"] == 0

    def test_filter_availability_by_period(self, client: TestClient, db: Session):  # noqa: ARG002
        """Test filtering availability by period."""
        # Create teacher
        teacher_data = {
            "first_name": "Filter",
            "last_name": "Period",
            "email": "filter.period@schule.de",
            "abbreviation": "FP1",
            "max_hours_per_week": 28,
        }
        response = client.post("/api/v1/teachers", json=teacher_data)
        teacher_id = response.json()["id"]

        # Add availability for different periods
        for period in range(1, 4):
            availability_data = {
                "weekday": 0,
                "period": period,
                "availability_type": "AVAILABLE",
                "effective_from": "2020-01-01",
            }
            client.post(
                f"/api/v1/teachers/{teacher_id}/availability", json=availability_data
            )

        # Filter by period 2
        response = client.get(f"/api/v1/teachers/{teacher_id}/availability?period=2")
        assert response.status_code == 200

        data = response.json()
        assert len(data) == 1
        assert data[0]["period"] == 2


class TestScheduleIntegration:
    """Test integration of availability with schedule creation."""

    def test_prevent_schedule_on_blocked_period(self, client: TestClient, db: Session):  # noqa: ARG002
        """Test that schedules cannot be created on blocked periods."""
        # Create teacher
        teacher_data = {
            "first_name": "Blocked",
            "last_name": "Teacher",
            "email": "blocked.teacher@schule.de",
            "abbreviation": "BT1",
            "max_hours_per_week": 28,
        }
        response = client.post("/api/v1/teachers", json=teacher_data)
        assert response.status_code == 201, f"Failed to create teacher: {response.text}"
        teacher_id = response.json()["id"]

        # Create class
        class_data = {
            "name": "1a",
            "grade": 1,
            "size": 20,
        }
        response = client.post("/api/v1/classes", json=class_data)
        assert response.status_code == 201, f"Failed to create class: {response.text}"
        class_id = response.json()["id"]

        # Create subject
        subject_data = {
            "name": "Mathematik",
            "code": "MATH",
            "color": "#FF5733",
        }
        response = client.post("/api/v1/subjects", json=subject_data)
        assert response.status_code == 201, f"Failed to create subject: {response.text}"
        subject_id = response.json()["id"]

        # Create teacher-subject qualification
        qualification_data = {
            "subject_id": subject_id,
            "qualification_level": "PRIMARY",
            "grades": [1, 2, 3, 4],
        }
        response = client.post(
            f"/api/v1/teachers/{teacher_id}/subjects", json=qualification_data
        )
        assert response.status_code == 201, (
            f"Failed to create qualification: {response.text}"
        )

        # Create a timeslot for testing
        timeslot_data = {
            "day": 1,  # Monday (1-based in API, TimeSLot model uses 1-5)
            "period": 1,
            "start_time": "08:00",
            "end_time": "08:45",
        }
        response = client.post("/api/v1/timeslots", json=timeslot_data)
        if response.status_code == 201:
            timeslot_id = response.json()["id"]
            timeslot_day = 0  # 0-based for availability (0=Monday)
        else:
            # Timeslot might already exist, get it
            response = client.get("/api/v1/timeslots")
            timeslots = response.json()
            if timeslots:
                # Find a timeslot with day=1 and period=1
                for ts in timeslots:
                    if ts["day"] == 1 and ts["period"] == 1:
                        timeslot_id = ts["id"]
                        timeslot_day = 0  # Monday is 0 in availability
                        break
                else:
                    # Use first available timeslot
                    timeslot_id = timeslots[0]["id"]
                    timeslot_day = timeslots[0]["day"] - 1  # Convert to 0-based
            else:
                raise Exception("Could not create or find timeslot")

        # Block this period for the teacher (use a date in the past to ensure it's active)
        availability_data = {
            "weekday": timeslot_day,
            "period": 1,
            "availability_type": "BLOCKED",
            "effective_from": "2020-01-01",  # Use past date to ensure it's active
            "reason": "Administrative duties",
        }
        response = client.post(
            f"/api/v1/teachers/{teacher_id}/availability", json=availability_data
        )
        assert response.status_code == 201, (
            f"Failed to create availability: {response.text}"
        )

        # Try to create a schedule (should fail)
        schedule_data = {
            "class_id": class_id,
            "teacher_id": teacher_id,
            "subject_id": subject_id,
            "timeslot_id": timeslot_id,
        }
        response = client.post("/api/v1/schedule", json=schedule_data)
        assert response.status_code == 409  # Conflict
        assert "not available" in response.json()["detail"].lower()

    def test_validate_part_time_hours(self, client: TestClient, db: Session):  # noqa: ARG002
        """Test that part-time teachers don't exceed their max hours."""
        # Create part-time teacher
        teacher_data = {
            "first_name": "PartTime",
            "last_name": "Teacher",
            "email": "parttime.teacher@schule.de",
            "abbreviation": "PT1",
            "max_hours_per_week": 10,  # Only 10 hours per week
            "is_part_time": True,
        }
        response = client.post("/api/v1/teachers", json=teacher_data)
        teacher_id = response.json()["id"]

        # Mark teacher as available for limited periods
        for day in range(2):  # Monday and Tuesday
            for period in range(1, 6):  # 5 periods each day = 10 total
                availability_data = {
                    "weekday": day,
                    "period": period,
                    "availability_type": "AVAILABLE",
                    "effective_from": "2020-01-01",
                }
                client.post(
                    f"/api/v1/teachers/{teacher_id}/availability",
                    json=availability_data,
                )

        # Validate that exceeding max hours is prevented
        response = client.get(f"/api/v1/teachers/{teacher_id}/availability/validate")
        assert response.status_code == 200

        data = response.json()
        assert data["max_hours_per_week"] == 10
        assert data["available_hours"] == 10
        assert data["is_valid"] is True
