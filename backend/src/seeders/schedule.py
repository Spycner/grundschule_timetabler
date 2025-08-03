"""Seeder for Schedule entries."""

from sqlalchemy.orm import Session

from src.models.class_ import Class
from src.models.schedule import Schedule
from src.models.subject import Subject
from src.models.teacher import Teacher
from src.models.timeslot import TimeSlot


def seed_schedule(db: Session) -> int:
    """
    Seed development schedule entries.

    Creates a sample weekly schedule for class 1a as an example.
    """
    # Get entities
    class_1a = db.query(Class).filter(Class.name == "1a").first()
    if not class_1a:
        print("Class 1a not found. Please run class seeder first.")
        return 0

    # Get teachers
    maria = db.query(Teacher).filter(Teacher.abbreviation == "MUE").first()
    thomas = db.query(Teacher).filter(Teacher.abbreviation == "SCH").first()
    anna = db.query(Teacher).filter(Teacher.abbreviation == "WEB").first()

    if not all([maria, thomas, anna]):
        print("Required teachers not found. Please run teacher seeder first.")
        return 0

    # Get subjects
    math = db.query(Subject).filter(Subject.code == "MA").first()
    german = db.query(Subject).filter(Subject.code == "DE").first()
    science = db.query(Subject).filter(Subject.code == "SU").first()
    sport = db.query(Subject).filter(Subject.code == "SP").first()
    art = db.query(Subject).filter(Subject.code == "KU").first()
    music = db.query(Subject).filter(Subject.code == "MU").first()

    if not all([math, german, science, sport, art, music]):
        print("Required subjects not found. Please run subject seeder first.")
        return 0

    # Get timeslots (non-break periods)
    timeslots = (
        db.query(TimeSlot)
        .filter(~TimeSlot.is_break)
        .order_by(TimeSlot.day, TimeSlot.period)
        .all()
    )

    if len(timeslots) < 20:
        print("Not enough timeslots found. Please run timeslot seeder first.")
        return 0

    # Check for existing schedule entries
    existing = db.query(Schedule).first()
    if existing:
        print("Schedule entries already exist. Skipping schedule seeding.")
        return 0

    # Create a sample weekly schedule for class 1a
    schedule_entries = [
        # Monday
        Schedule(
            class_id=class_1a.id,
            teacher_id=maria.id,
            subject_id=german.id,
            timeslot_id=timeslots[0].id,
            room="101",
            week_type="ALL",
        ),  # Period 1
        Schedule(
            class_id=class_1a.id,
            teacher_id=maria.id,
            subject_id=german.id,
            timeslot_id=timeslots[1].id,
            room="101",
            week_type="ALL",
        ),  # Period 2
        # Period 3 is break
        Schedule(
            class_id=class_1a.id,
            teacher_id=maria.id,
            subject_id=math.id,
            timeslot_id=timeslots[2].id,
            room="101",
            week_type="ALL",
        ),  # Period 4
        Schedule(
            class_id=class_1a.id,
            teacher_id=maria.id,
            subject_id=math.id,
            timeslot_id=timeslots[3].id,
            room="101",
            week_type="ALL",
        ),  # Period 5
        # Period 6 is break
        Schedule(
            class_id=class_1a.id,
            teacher_id=anna.id,
            subject_id=art.id,
            timeslot_id=timeslots[4].id,
            room="101",
            week_type="ALL",
        ),  # Period 7
        # Tuesday
        Schedule(
            class_id=class_1a.id,
            teacher_id=maria.id,
            subject_id=math.id,
            timeslot_id=timeslots[5].id,
            room="101",
            week_type="ALL",
        ),  # Period 1
        Schedule(
            class_id=class_1a.id,
            teacher_id=maria.id,
            subject_id=math.id,
            timeslot_id=timeslots[6].id,
            room="101",
            week_type="ALL",
        ),  # Period 2
        # Period 3 is break
        Schedule(
            class_id=class_1a.id,
            teacher_id=thomas.id,
            subject_id=sport.id,
            timeslot_id=timeslots[7].id,
            room="Turnhalle",
            week_type="ALL",
        ),  # Period 4
        Schedule(
            class_id=class_1a.id,
            teacher_id=thomas.id,
            subject_id=sport.id,
            timeslot_id=timeslots[8].id,
            room="Turnhalle",
            week_type="ALL",
        ),  # Period 5
        # Period 6 is break
        Schedule(
            class_id=class_1a.id,
            teacher_id=maria.id,
            subject_id=science.id,
            timeslot_id=timeslots[9].id,
            room="101",
            week_type="ALL",
        ),  # Period 7
        # Wednesday
        Schedule(
            class_id=class_1a.id,
            teacher_id=maria.id,
            subject_id=german.id,
            timeslot_id=timeslots[10].id,
            room="101",
            week_type="ALL",
        ),  # Period 1
        Schedule(
            class_id=class_1a.id,
            teacher_id=maria.id,
            subject_id=german.id,
            timeslot_id=timeslots[11].id,
            room="101",
            week_type="ALL",
        ),  # Period 2
        # Period 3 is break
        Schedule(
            class_id=class_1a.id,
            teacher_id=maria.id,
            subject_id=math.id,
            timeslot_id=timeslots[12].id,
            room="101",
            week_type="ALL",
        ),  # Period 4
        Schedule(
            class_id=class_1a.id,
            teacher_id=anna.id,
            subject_id=music.id,
            timeslot_id=timeslots[13].id,
            room="Musikraum",
            week_type="ALL",
        ),  # Period 5
        # Thursday
        Schedule(
            class_id=class_1a.id,
            teacher_id=maria.id,
            subject_id=german.id,
            timeslot_id=timeslots[14].id,
            room="101",
            week_type="ALL",
        ),  # Period 1
        Schedule(
            class_id=class_1a.id,
            teacher_id=maria.id,
            subject_id=science.id,
            timeslot_id=timeslots[15].id,
            room="101",
            week_type="ALL",
        ),  # Period 2
        # Period 3 is break
        Schedule(
            class_id=class_1a.id,
            teacher_id=maria.id,
            subject_id=math.id,
            timeslot_id=timeslots[16].id,
            room="101",
            week_type="ALL",
        ),  # Period 4
        Schedule(
            class_id=class_1a.id,
            teacher_id=maria.id,
            subject_id=math.id,
            timeslot_id=timeslots[17].id,
            room="101",
            week_type="ALL",
        ),  # Period 5
        # Friday
        Schedule(
            class_id=class_1a.id,
            teacher_id=maria.id,
            subject_id=german.id,
            timeslot_id=timeslots[18].id,
            room="101",
            week_type="ALL",
        ),  # Period 1
        Schedule(
            class_id=class_1a.id,
            teacher_id=maria.id,
            subject_id=science.id,
            timeslot_id=timeslots[19].id,
            room="101",
            week_type="ALL",
        ),  # Period 2
        # Period 3 is break
        # Periods 4-5: A/B week example
        Schedule(
            class_id=class_1a.id,
            teacher_id=anna.id,
            subject_id=art.id,
            timeslot_id=timeslots[20].id,
            room="101",
            week_type="A",
        ),  # Period 4, A week
        Schedule(
            class_id=class_1a.id,
            teacher_id=anna.id,
            subject_id=music.id,
            timeslot_id=timeslots[20].id,
            room="Musikraum",
            week_type="B",
        ),  # Period 4, B week
    ]

    # Add all schedule entries
    for entry in schedule_entries:
        db.add(entry)

    db.commit()
    print(f"Created {len(schedule_entries)} schedule entries for class 1a")
    return len(schedule_entries)


def clear_schedule(db: Session) -> int:
    """Clear all schedule entries."""
    count = db.query(Schedule).count()
    db.query(Schedule).delete()
    db.commit()
    print(f"Cleared {count} schedule entries")
    return count
