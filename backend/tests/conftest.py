"""Pytest configuration and fixtures."""

from datetime import time

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.main import app
from src.models.class_ import Class
from src.models.database import Base, get_db
from src.models.subject import Subject
from src.models.teacher import Teacher
from src.models.teacher_subject import QualificationLevel, TeacherSubject
from src.models.timeslot import TimeSlot

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override database dependency for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def db():
    """Create a fresh database for each test."""
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    """Create test client with overridden dependencies."""
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def sample_teachers(db):
    """Create sample teachers for testing."""
    teachers = [
        Teacher(
            first_name="Maria",
            last_name="Müller",
            email="maria@school.de",
            abbreviation="MM",
            max_hours_per_week=28,
            is_part_time=False,
        ),
        Teacher(
            first_name="Hans",
            last_name="Schmidt",
            email="hans@school.de",
            abbreviation="HS",
            max_hours_per_week=20,
            is_part_time=True,
        ),
        Teacher(
            first_name="Anna",
            last_name="Weber",
            email="anna@school.de",
            abbreviation="AW",
            max_hours_per_week=25,
            is_part_time=False,
        ),
    ]
    db.add_all(teachers)
    db.commit()
    return teachers


@pytest.fixture
def sample_classes(db):
    """Create sample classes for testing."""
    classes = [
        Class(name="1a", grade=1, size=22, home_room="Room 101"),
        Class(name="1b", grade=1, size=21, home_room="Room 102"),
        Class(name="2a", grade=2, size=24, home_room="Room 201"),
        Class(name="3a", grade=3, size=23, home_room="Room 301"),
        Class(name="4a", grade=4, size=25, home_room="Room 401"),
    ]
    db.add_all(classes)
    db.commit()
    return classes


@pytest.fixture
def sample_subjects(db):
    """Create sample subjects for testing."""
    subjects = [
        Subject(name="Deutsch", code="DE", color="#FF0000"),
        Subject(name="Mathematik", code="MA", color="#00FF00"),
        Subject(name="Sachunterricht", code="SU", color="#0000FF"),
        Subject(name="Sport", code="SP", color="#FFFF00"),
        Subject(name="Musik", code="MU", color="#FF00FF"),
        Subject(name="Kunst", code="KU", color="#00FFFF"),
    ]
    db.add_all(subjects)
    db.commit()
    return subjects


@pytest.fixture
def sample_timeslots(db):
    """Create sample timeslots for testing."""
    timeslots = []

    # Create a week schedule: Monday-Friday, 8 periods per day
    for day in range(1, 6):  # Monday = 1, Friday = 5
        for period in range(1, 9):  # 8 periods per day
            # Add break periods
            is_break = period in [3, 6]  # Third and sixth periods are breaks

            # Calculate times
            if period <= 2:
                start_hour = 7 + period
                end_hour = start_hour + 1
            elif period == 3:  # Break
                start_hour = 9
                end_hour = 9
            elif period <= 5:
                start_hour = 8 + period
                end_hour = start_hour + 1
            elif period == 6:  # Break
                start_hour = 12
                end_hour = 12
            else:
                start_hour = 7 + period
                end_hour = start_hour + 1

            timeslot = TimeSlot(
                day=day,
                period=period,
                start_time=time(start_hour, 0),
                end_time=time(end_hour, 0),
                is_break=is_break,
            )
            timeslots.append(timeslot)

    db.add_all(timeslots)
    db.commit()
    return timeslots


# Aliases for fixtures with underscores (used by scheduling algorithm tests)
@pytest.fixture
def _sample_teachers(sample_teachers):
    """Alias for sample_teachers fixture."""
    return sample_teachers


@pytest.fixture
def _sample_classes(sample_classes):
    """Alias for sample_classes fixture."""
    return sample_classes


@pytest.fixture
def _sample_subjects(sample_subjects):
    """Alias for sample_subjects fixture."""
    return sample_subjects


@pytest.fixture
def _sample_timeslots(sample_timeslots):
    """Alias for sample_timeslots fixture."""
    return sample_timeslots


@pytest.fixture
def _simple_scheduling_setup(
    sample_teachers, sample_classes, sample_subjects, sample_timeslots, db
):
    """Create simple scheduling setup with teacher-subject qualifications."""
    # Create teacher-subject qualifications
    teachers = sample_teachers
    subjects = sample_subjects

    # Give each teacher qualification for at least one subject
    for i, teacher in enumerate(teachers):
        subject = subjects[i % len(subjects)]
        ts = TeacherSubject(
            teacher_id=teacher.id,
            subject_id=subject.id,
            qualification_level=QualificationLevel.PRIMARY,
            grades=[1, 2, 3, 4],
            max_hours_per_week=10,
        )
        db.add(ts)

    # Add some secondary qualifications
    if len(teachers) > 1 and len(subjects) > 1:
        ts2 = TeacherSubject(
            teacher_id=teachers[0].id,
            subject_id=subjects[1].id,
            qualification_level=QualificationLevel.SECONDARY,
            grades=[1, 2],
            max_hours_per_week=5,
        )
        db.add(ts2)

    db.commit()
    return db
