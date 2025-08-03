"""TimeSlot seeder for development data."""

from datetime import time

from sqlalchemy.orm import Session

from src.models.timeslot import TimeSlot


def seed_timeslots(db: Session) -> None:
    """Seed timeslots with a standard German Grundschule schedule."""
    # Check if timeslots already exist
    existing_count = db.query(TimeSlot).count()
    if existing_count > 0:
        print(f"Skipping timeslot seeding - {existing_count} timeslots already exist")
        return

    print("Seeding timeslots...")

    # Define the standard schedule template
    schedule_template = [
        {"period": 1, "start": "08:00", "end": "08:45", "is_break": False},
        {"period": 2, "start": "08:45", "end": "09:30", "is_break": False},
        {
            "period": 3,
            "start": "09:30",
            "end": "09:50",
            "is_break": True,
        },  # Große Pause
        {"period": 4, "start": "09:50", "end": "10:35", "is_break": False},
        {"period": 5, "start": "10:35", "end": "11:20", "is_break": False},
        {
            "period": 6,
            "start": "11:20",
            "end": "11:30",
            "is_break": True,
        },  # Kleine Pause
        {"period": 7, "start": "11:30", "end": "12:15", "is_break": False},
        {"period": 8, "start": "12:15", "end": "13:00", "is_break": False},
    ]

    count = 0
    # Create timeslots for Monday through Friday
    for day in range(1, 6):  # 1=Monday to 5=Friday
        day_name = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"][day - 1]

        for slot in schedule_template:
            # Parse time strings
            start_hour, start_min = map(int, slot["start"].split(":"))
            end_hour, end_min = map(int, slot["end"].split(":"))

            # Determine slot type for logging
            slot_type = "Break" if slot["is_break"] else f"Period {slot['period']}"

            timeslot = TimeSlot(
                day=day,
                period=slot["period"],
                start_time=time(start_hour, start_min),
                end_time=time(end_hour, end_min),
                is_break=slot["is_break"],
            )
            db.add(timeslot)
            count += 1

            print(f"  Created {day_name} - {slot_type}: {slot['start']}-{slot['end']}")

    db.commit()
    print(f"Successfully seeded {count} timeslots for the weekly schedule")


def clear_timeslots(db: Session) -> None:
    """Clear all timeslots from the database."""
    count = db.query(TimeSlot).count()
    if count > 0:
        db.query(TimeSlot).delete()
        db.commit()
        print(f"Cleared {count} timeslots from the database")
