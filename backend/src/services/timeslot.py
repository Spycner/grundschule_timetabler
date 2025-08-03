"""TimeSlot service for business logic."""

from datetime import time

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.models.timeslot import TimeSlot
from src.schemas.timeslot import TimeSlotCreate, TimeSlotUpdate


class TimeSlotService:
    """Service class for timeslot operations."""

    @staticmethod
    def get_timeslot(db: Session, timeslot_id: int) -> TimeSlot | None:
        """Get a timeslot by ID."""
        return db.query(TimeSlot).filter(TimeSlot.id == timeslot_id).first()

    @staticmethod
    def get_timeslot_by_day_period(
        db: Session, day: int, period: int
    ) -> TimeSlot | None:
        """Get a timeslot by day and period."""
        return (
            db.query(TimeSlot)
            .filter(TimeSlot.day == day, TimeSlot.period == period)
            .first()
        )

    @staticmethod
    def get_timeslots(db: Session, skip: int = 0, limit: int = 100) -> list[TimeSlot]:
        """Get all timeslots ordered by day and period."""
        return (
            db.query(TimeSlot)
            .order_by(TimeSlot.day, TimeSlot.period)
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def check_time_overlap(
        db: Session,
        day: int,
        start_time: time,
        end_time: time,
        exclude_id: int | None = None,
    ) -> bool:
        """Check if a time range overlaps with existing timeslots on the same day."""
        query = db.query(TimeSlot).filter(TimeSlot.day == day)

        if exclude_id:
            query = query.filter(TimeSlot.id != exclude_id)

        existing_slots = query.all()

        for slot in existing_slots:
            # Check for overlap: new start is before existing end AND new end is after existing start
            if start_time < slot.end_time and end_time > slot.start_time:
                return True

        return False

    @staticmethod
    def create_timeslot(db: Session, timeslot: TimeSlotCreate) -> TimeSlot:
        """Create a new timeslot."""
        # Check for time overlap
        if TimeSlotService.check_time_overlap(
            db, timeslot.day, timeslot.start_time, timeslot.end_time
        ):
            raise ValueError("Time range overlaps with existing timeslot")

        db_timeslot = TimeSlot(**timeslot.model_dump())
        db.add(db_timeslot)
        try:
            db.commit()
            db.refresh(db_timeslot)
            return db_timeslot
        except IntegrityError as e:
            db.rollback()
            # SQLite doesn't always include constraint names, check for unique constraint
            if "UNIQUE constraint failed" in str(e.orig) and "timeslots.day" in str(
                e.orig
            ):
                raise ValueError(
                    "TimeSlot with this day and period already exists"
                ) from e
            raise

    @staticmethod
    def update_timeslot(
        db: Session, timeslot_id: int, timeslot_update: TimeSlotUpdate
    ) -> TimeSlot | None:
        """Update a timeslot."""
        db_timeslot = TimeSlotService.get_timeslot(db, timeslot_id)
        if not db_timeslot:
            return None

        update_data = timeslot_update.model_dump(exclude_unset=True)

        # If updating time, check for overlap
        if (
            "start_time" in update_data or "end_time" in update_data
        ) and TimeSlotService.check_time_overlap(
            db,
            update_data.get("day", db_timeslot.day),
            update_data.get("start_time", db_timeslot.start_time),
            update_data.get("end_time", db_timeslot.end_time),
            exclude_id=timeslot_id,
        ):
            raise ValueError("Time range overlaps with existing timeslot")

        for key, value in update_data.items():
            setattr(db_timeslot, key, value)

        try:
            db.commit()
            db.refresh(db_timeslot)
            return db_timeslot
        except IntegrityError as e:
            db.rollback()
            # SQLite doesn't always include constraint names, check for unique constraint
            if "UNIQUE constraint failed" in str(e.orig) and "timeslots.day" in str(
                e.orig
            ):
                raise ValueError(
                    "TimeSlot with this day and period already exists"
                ) from e
            raise

    @staticmethod
    def delete_timeslot(db: Session, timeslot_id: int) -> bool:
        """Delete a timeslot."""
        db_timeslot = TimeSlotService.get_timeslot(db, timeslot_id)
        if not db_timeslot:
            return False

        db.delete(db_timeslot)
        db.commit()
        return True

    @staticmethod
    def generate_default_schedule(db: Session) -> int:
        """Generate a default weekly schedule for a German Grundschule."""
        # Clear existing timeslots (optional - might want to check first)
        db.query(TimeSlot).delete()

        # Define the standard schedule
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
            for slot in schedule_template:
                # Parse time strings
                start_hour, start_min = map(int, slot["start"].split(":"))
                end_hour, end_min = map(int, slot["end"].split(":"))

                db_timeslot = TimeSlot(
                    day=day,
                    period=slot["period"],
                    start_time=time(start_hour, start_min),
                    end_time=time(end_hour, end_min),
                    is_break=slot["is_break"],
                )
                db.add(db_timeslot)
                count += 1

        db.commit()
        return count
