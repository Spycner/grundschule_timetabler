"""Schedule service for business logic and conflict detection."""

from datetime import UTC, datetime

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload

from src.models.schedule import Schedule
from src.models.teacher_availability import AvailabilityType
from src.models.timeslot import TimeSlot
from src.schemas.schedule import ConflictDetail, ScheduleCreate, ScheduleUpdate
from src.services.teacher_availability import TeacherAvailabilityService


class ScheduleService:
    """Service class for schedule operations."""

    @staticmethod
    def get_schedule(db: Session, schedule_id: int) -> Schedule | None:
        """Get a schedule entry by ID."""
        return (
            db.query(Schedule)
            .options(
                joinedload(Schedule.class_),
                joinedload(Schedule.teacher),
                joinedload(Schedule.subject),
                joinedload(Schedule.timeslot),
            )
            .filter(Schedule.id == schedule_id)
            .first()
        )

    @staticmethod
    def get_schedules(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        week_type: str | None = None,
        day: int | None = None,
        include_breaks: bool = True,
    ) -> list[Schedule]:
        """Get all schedules with optional filters."""
        query = db.query(Schedule).options(
            joinedload(Schedule.class_),
            joinedload(Schedule.teacher),
            joinedload(Schedule.subject),
            joinedload(Schedule.timeslot),
        )

        # Apply filters
        if week_type:
            query = query.filter(
                (Schedule.week_type == week_type) | (Schedule.week_type == "ALL")
            )

        # Join once and apply filters
        query = query.join(TimeSlot)

        if day:
            query = query.filter(TimeSlot.day == day)

        if not include_breaks:
            query = query.filter(~TimeSlot.is_break)

        # Order by day and period
        query = query.order_by(TimeSlot.day, TimeSlot.period)

        return query.offset(skip).limit(limit).all()

    @staticmethod
    def get_schedules_by_class(
        db: Session, class_id: int, week_type: str | None = None
    ) -> list[Schedule]:
        """Get all schedules for a specific class."""
        query = (
            db.query(Schedule)
            .options(
                joinedload(Schedule.class_),
                joinedload(Schedule.teacher),
                joinedload(Schedule.subject),
                joinedload(Schedule.timeslot),
            )
            .filter(Schedule.class_id == class_id)
        )

        if week_type:
            query = query.filter(
                (Schedule.week_type == week_type) | (Schedule.week_type == "ALL")
            )

        return query.join(TimeSlot).order_by(TimeSlot.day, TimeSlot.period).all()

    @staticmethod
    def get_schedules_by_teacher(
        db: Session, teacher_id: int, week_type: str | None = None
    ) -> list[Schedule]:
        """Get all schedules for a specific teacher."""
        query = (
            db.query(Schedule)
            .options(
                joinedload(Schedule.class_),
                joinedload(Schedule.teacher),
                joinedload(Schedule.subject),
                joinedload(Schedule.timeslot),
            )
            .filter(Schedule.teacher_id == teacher_id)
        )

        if week_type:
            query = query.filter(
                (Schedule.week_type == week_type) | (Schedule.week_type == "ALL")
            )

        return query.join(TimeSlot).order_by(TimeSlot.day, TimeSlot.period).all()

    @staticmethod
    def get_schedules_by_room(
        db: Session, room: str, week_type: str | None = None
    ) -> list[Schedule]:
        """Get all schedules for a specific room."""
        query = (
            db.query(Schedule)
            .options(
                joinedload(Schedule.class_),
                joinedload(Schedule.teacher),
                joinedload(Schedule.subject),
                joinedload(Schedule.timeslot),
            )
            .filter(Schedule.room == room)
        )

        if week_type:
            query = query.filter(
                (Schedule.week_type == week_type) | (Schedule.week_type == "ALL")
            )

        return query.join(TimeSlot).order_by(TimeSlot.day, TimeSlot.period).all()

    @staticmethod
    def get_schedules_by_timeslot(
        db: Session, timeslot_id: int, week_type: str | None = None
    ) -> list[Schedule]:
        """Get all schedules at a specific timeslot."""
        query = (
            db.query(Schedule)
            .options(
                joinedload(Schedule.class_),
                joinedload(Schedule.teacher),
                joinedload(Schedule.subject),
                joinedload(Schedule.timeslot),
            )
            .filter(Schedule.timeslot_id == timeslot_id)
        )

        if week_type:
            query = query.filter(
                (Schedule.week_type == week_type) | (Schedule.week_type == "ALL")
            )

        return query.all()

    @staticmethod
    def validate_schedule(
        db: Session, schedule: ScheduleCreate, exclude_id: int | None = None
    ) -> list[ConflictDetail]:
        """Validate a schedule entry for conflicts."""
        conflicts = []

        # Check if timeslot is a break
        timeslot = (
            db.query(TimeSlot).filter(TimeSlot.id == schedule.timeslot_id).first()
        )
        if timeslot and timeslot.is_break:
            conflicts.append(
                ConflictDetail(
                    type="break_conflict",
                    message="Cannot schedule classes during break periods",
                )
            )

        # Check teacher availability
        if timeslot:
            # Convert timeslot day (1-5) to availability weekday (0-4)
            weekday = timeslot.day - 1
            availability = TeacherAvailabilityService.check_teacher_availability(
                db,
                schedule.teacher_id,
                weekday,
                timeslot.period,
                datetime.now(UTC).date(),  # Use current date for availability check
            )

            if availability == AvailabilityType.BLOCKED:
                conflicts.append(
                    ConflictDetail(
                        type="availability_conflict",
                        message="Teacher is not available during this period",
                    )
                )
            elif availability is None:
                # No explicit availability set - could be a warning
                pass  # For now, allow if no explicit availability is set

        # Build base query for conflict checking
        base_query = db.query(Schedule).filter(
            Schedule.timeslot_id == schedule.timeslot_id,
            (Schedule.week_type == schedule.week_type)
            | (Schedule.week_type == "ALL")
            | (schedule.week_type == "ALL"),
        )

        if exclude_id:
            base_query = base_query.filter(Schedule.id != exclude_id)

        # Check teacher conflict
        teacher_conflict = base_query.filter(
            Schedule.teacher_id == schedule.teacher_id
        ).first()
        if teacher_conflict:
            conflicts.append(
                ConflictDetail(
                    type="teacher_conflict",
                    message="Teacher is already scheduled for another class at this time",
                    existing_entry_id=teacher_conflict.id,
                )
            )

        # Check class conflict
        class_conflict = base_query.filter(
            Schedule.class_id == schedule.class_id
        ).first()
        if class_conflict:
            conflicts.append(
                ConflictDetail(
                    type="class_conflict",
                    message="Class already has another subject scheduled at this time",
                    existing_entry_id=class_conflict.id,
                )
            )

        # Check room conflict (only if room is specified)
        if schedule.room:
            room_conflict = base_query.filter(Schedule.room == schedule.room).first()
            if room_conflict:
                conflicts.append(
                    ConflictDetail(
                        type="room_conflict",
                        message=f"Room '{schedule.room}' is already booked at this time",
                        existing_entry_id=room_conflict.id,
                    )
                )

        return conflicts

    @staticmethod
    def create_schedule(db: Session, schedule: ScheduleCreate) -> Schedule:
        """Create a new schedule entry with conflict checking."""
        # Validate for conflicts
        conflicts = ScheduleService.validate_schedule(db, schedule)
        if conflicts:
            # Raise appropriate error based on conflict type
            if any(c.type == "break_conflict" for c in conflicts):
                raise ValueError("Cannot schedule during break periods")
            if any(c.type == "availability_conflict" for c in conflicts):
                raise ValueError("Teacher is not available during this period")
            if any(c.type == "teacher_conflict" for c in conflicts):
                raise ValueError("Teacher conflict detected")
            if any(c.type == "class_conflict" for c in conflicts):
                raise ValueError("Class conflict detected")
            if any(c.type == "room_conflict" for c in conflicts):
                raise ValueError("Room conflict detected")

        db_schedule = Schedule(**schedule.model_dump())
        db.add(db_schedule)
        try:
            db.commit()
            db.refresh(db_schedule)
            # Load relationships
            db.refresh(db_schedule, ["class_", "teacher", "subject", "timeslot"])
            return db_schedule
        except IntegrityError as e:
            db.rollback()
            # Handle database-level constraint violations
            if "class_id" in str(e.orig):
                raise ValueError("Class conflict detected") from e
            if "teacher_id" in str(e.orig):
                raise ValueError("Teacher conflict detected") from e
            raise

    @staticmethod
    def update_schedule(
        db: Session, schedule_id: int, schedule_update: ScheduleUpdate
    ) -> Schedule | None:
        """Update a schedule entry."""
        db_schedule = ScheduleService.get_schedule(db, schedule_id)
        if not db_schedule:
            return None

        update_data = schedule_update.model_dump(exclude_unset=True)

        # If critical fields are being updated, validate for conflicts
        if any(
            field in update_data
            for field in ["class_id", "teacher_id", "timeslot_id", "room", "week_type"]
        ):
            # Create a ScheduleCreate object with the updated values
            current_data = {
                "class_id": update_data.get("class_id", db_schedule.class_id),
                "teacher_id": update_data.get("teacher_id", db_schedule.teacher_id),
                "subject_id": update_data.get("subject_id", db_schedule.subject_id),
                "timeslot_id": update_data.get("timeslot_id", db_schedule.timeslot_id),
                "room": update_data.get("room", db_schedule.room),
                "week_type": update_data.get("week_type", db_schedule.week_type),
            }
            schedule_check = ScheduleCreate(**current_data)
            conflicts = ScheduleService.validate_schedule(
                db, schedule_check, exclude_id=schedule_id
            )
            if conflicts:
                # Raise appropriate error based on conflict type
                if any(c.type == "break_conflict" for c in conflicts):
                    raise ValueError("Cannot schedule during break periods")
                if any(c.type == "teacher_conflict" for c in conflicts):
                    raise ValueError("Teacher conflict detected")
                if any(c.type == "class_conflict" for c in conflicts):
                    raise ValueError("Class conflict detected")
                if any(c.type == "room_conflict" for c in conflicts):
                    raise ValueError("Room conflict detected")

        for field, value in update_data.items():
            setattr(db_schedule, field, value)

        try:
            db.commit()
            db.refresh(db_schedule, ["class_", "teacher", "subject", "timeslot"])
            return db_schedule
        except IntegrityError as e:
            db.rollback()
            if "class_id" in str(e.orig):
                raise ValueError("Class conflict detected") from e
            if "teacher_id" in str(e.orig):
                raise ValueError("Teacher conflict detected") from e
            raise

    @staticmethod
    def delete_schedule(db: Session, schedule_id: int) -> bool:
        """Delete a schedule entry."""
        db_schedule = db.query(Schedule).filter(Schedule.id == schedule_id).first()
        if not db_schedule:
            return False

        db.delete(db_schedule)
        db.commit()
        return True

    @staticmethod
    def create_bulk_schedules(
        db: Session, schedules: list[ScheduleCreate]
    ) -> list[Schedule]:
        """Create multiple schedule entries at once."""
        created_schedules = []

        # Validate all entries first
        for schedule in schedules:
            conflicts = ScheduleService.validate_schedule(db, schedule)
            if conflicts:
                # Raise error on first conflict found
                if any(c.type == "break_conflict" for c in conflicts):
                    raise ValueError("Cannot schedule during break periods")
                if any(c.type == "teacher_conflict" for c in conflicts):
                    raise ValueError("Teacher conflict detected in bulk creation")
                if any(c.type == "class_conflict" for c in conflicts):
                    raise ValueError("Class conflict detected in bulk creation")
                if any(c.type == "room_conflict" for c in conflicts):
                    raise ValueError("Room conflict detected in bulk creation")

        # If all validations pass, create all entries
        for schedule in schedules:
            db_schedule = Schedule(**schedule.model_dump())
            db.add(db_schedule)
            created_schedules.append(db_schedule)

        try:
            db.commit()
            # Refresh all created schedules
            for db_schedule in created_schedules:
                db.refresh(db_schedule, ["class_", "teacher", "subject", "timeslot"])
            return created_schedules
        except IntegrityError as e:
            db.rollback()
            raise ValueError("Conflict detected during bulk creation") from e

    @staticmethod
    def get_all_conflicts(db: Session) -> list[tuple[Schedule, list[ConflictDetail]]]:
        """Find all conflicts in the current schedule."""
        conflicts_found = []
        all_schedules = db.query(Schedule).all()

        for schedule in all_schedules:
            schedule_data = ScheduleCreate(
                class_id=schedule.class_id,
                teacher_id=schedule.teacher_id,
                subject_id=schedule.subject_id,
                timeslot_id=schedule.timeslot_id,
                room=schedule.room,
                week_type=schedule.week_type,
            )
            conflicts = ScheduleService.validate_schedule(
                db, schedule_data, exclude_id=schedule.id
            )
            if conflicts:
                conflicts_found.append((schedule, conflicts))

        return conflicts_found
