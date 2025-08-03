"""Teacher Availability service for business logic."""

from datetime import UTC, date, datetime

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.models.schedule import Schedule
from src.models.teacher import Teacher
from src.models.teacher_availability import AvailabilityType, TeacherAvailability
from src.schemas.teacher_availability import (
    TeacherAvailabilityCreate,
    TeacherAvailabilityOverview,
    TeacherAvailabilityUpdate,
    TeacherAvailabilityValidation,
)


class TeacherAvailabilityService:
    """Service class for teacher availability operations."""

    @staticmethod
    def get_availability(
        db: Session, availability_id: int
    ) -> TeacherAvailability | None:
        """Get a single availability entry by ID."""
        return (
            db.query(TeacherAvailability)
            .filter(TeacherAvailability.id == availability_id)
            .first()
        )

    @staticmethod
    def get_teacher_availability(
        db: Session,
        teacher_id: int,
        weekday: int | None = None,
        period: int | None = None,
        active_date: date | None = None,
    ) -> list[TeacherAvailability]:
        """Get all availability entries for a teacher with optional filters."""
        query = db.query(TeacherAvailability).filter(
            TeacherAvailability.teacher_id == teacher_id
        )

        if weekday is not None:
            query = query.filter(TeacherAvailability.weekday == weekday)

        if period is not None:
            query = query.filter(TeacherAvailability.period == period)

        if active_date:
            query = query.filter(
                TeacherAvailability.effective_from <= active_date,
                (TeacherAvailability.effective_until.is_(None))
                | (TeacherAvailability.effective_until >= active_date),
            )

        return query.order_by(
            TeacherAvailability.weekday, TeacherAvailability.period
        ).all()

    @staticmethod
    def create_availability(
        db: Session, teacher_id: int, availability: TeacherAvailabilityCreate
    ) -> TeacherAvailability:
        """Create a new availability entry for a teacher."""
        # Check for overlapping entries
        existing = (
            db.query(TeacherAvailability)
            .filter(
                TeacherAvailability.teacher_id == teacher_id,
                TeacherAvailability.weekday == availability.weekday,
                TeacherAvailability.period == availability.period,
                TeacherAvailability.effective_from == availability.effective_from,
            )
            .first()
        )

        if existing:
            raise ValueError(
                f"Availability already exists for this teacher on "
                f"weekday {availability.weekday}, period {availability.period}, "
                f"starting from {availability.effective_from}"
            )

        db_availability = TeacherAvailability(
            teacher_id=teacher_id, **availability.model_dump()
        )
        db.add(db_availability)
        try:
            db.commit()
            db.refresh(db_availability)
            return db_availability
        except IntegrityError as e:
            db.rollback()
            raise ValueError(f"Failed to create availability: {e!s}") from e

    @staticmethod
    def update_availability(
        db: Session,
        availability_id: int,
        availability_update: TeacherAvailabilityUpdate,
    ) -> TeacherAvailability:
        """Update an existing availability entry."""
        db_availability = (
            db.query(TeacherAvailability)
            .filter(TeacherAvailability.id == availability_id)
            .first()
        )

        if not db_availability:
            raise ValueError(f"Availability with ID {availability_id} not found")

        # Update only provided fields
        update_data = availability_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_availability, field, value)

        try:
            db.commit()
            db.refresh(db_availability)
            return db_availability
        except IntegrityError as e:
            db.rollback()
            raise ValueError(f"Failed to update availability: {e!s}") from e

    @staticmethod
    def delete_availability(db: Session, availability_id: int) -> bool:
        """Delete an availability entry."""
        db_availability = (
            db.query(TeacherAvailability)
            .filter(TeacherAvailability.id == availability_id)
            .first()
        )

        if not db_availability:
            return False

        db.delete(db_availability)
        db.commit()
        return True

    @staticmethod
    def bulk_create_availability(
        db: Session, teacher_id: int, availabilities: list[TeacherAvailabilityCreate]
    ) -> tuple[int, list[TeacherAvailability]]:
        """Bulk create availability entries for a teacher."""
        created_entries = []

        for availability in availabilities:
            # Check for existing entry
            existing = (
                db.query(TeacherAvailability)
                .filter(
                    TeacherAvailability.teacher_id == teacher_id,
                    TeacherAvailability.weekday == availability.weekday,
                    TeacherAvailability.period == availability.period,
                    TeacherAvailability.effective_from == availability.effective_from,
                )
                .first()
            )

            if not existing:
                db_availability = TeacherAvailability(
                    teacher_id=teacher_id, **availability.model_dump()
                )
                db.add(db_availability)
                created_entries.append(db_availability)

        if created_entries:
            try:
                db.commit()
                for entry in created_entries:
                    db.refresh(entry)
            except IntegrityError as e:
                db.rollback()
                raise ValueError(f"Failed to bulk create availability: {e!s}") from e

        return len(created_entries), created_entries

    @staticmethod
    def check_teacher_availability(
        db: Session,
        teacher_id: int,
        weekday: int,
        period: int,
        check_date: date | None = None,
    ) -> AvailabilityType | None:
        """Check if a teacher is available at a specific time."""
        if check_date is None:
            check_date = datetime.now(UTC).date()

        availability = (
            db.query(TeacherAvailability)
            .filter(
                TeacherAvailability.teacher_id == teacher_id,
                TeacherAvailability.weekday == weekday,
                TeacherAvailability.period == period,
                TeacherAvailability.effective_from <= check_date,
                (TeacherAvailability.effective_until.is_(None))
                | (TeacherAvailability.effective_until >= check_date),
            )
            .first()
        )

        return availability.availability_type if availability else None

    @staticmethod
    def get_teacher_overview(
        db: Session, teacher_id: int, active_date: date | None = None
    ) -> TeacherAvailabilityOverview:
        """Get an overview of a teacher's availability."""
        teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
        if not teacher:
            raise ValueError(f"Teacher with ID {teacher_id} not found")

        if active_date is None:
            active_date = datetime.now(UTC).date()

        # Get all active availability entries
        availabilities = (
            db.query(TeacherAvailability)
            .filter(
                TeacherAvailability.teacher_id == teacher_id,
                TeacherAvailability.effective_from <= active_date,
                (TeacherAvailability.effective_until.is_(None))
                | (TeacherAvailability.effective_until >= active_date),
            )
            .all()
        )

        # Count hours by type
        available_hours = 0
        blocked_hours = 0
        preferred_hours = 0
        availability_by_day = {}

        for av in availabilities:
            if av.weekday not in availability_by_day:
                availability_by_day[av.weekday] = {
                    "available": 0,
                    "blocked": 0,
                    "preferred": 0,
                }

            if av.availability_type == AvailabilityType.AVAILABLE:
                available_hours += 1
                availability_by_day[av.weekday]["available"] += 1
            elif av.availability_type == AvailabilityType.BLOCKED:
                blocked_hours += 1
                availability_by_day[av.weekday]["blocked"] += 1
            elif av.availability_type == AvailabilityType.PREFERRED:
                preferred_hours += 1
                availability_by_day[av.weekday]["preferred"] += 1

        return TeacherAvailabilityOverview(
            teacher_id=teacher.id,
            teacher_name=f"{teacher.first_name} {teacher.last_name}",
            is_part_time=teacher.is_part_time,
            max_hours_per_week=teacher.max_hours_per_week,
            available_hours=available_hours,
            blocked_hours=blocked_hours,
            preferred_hours=preferred_hours,
            availability_by_day=availability_by_day,
        )

    @staticmethod
    def validate_teacher_availability(
        db: Session, teacher_id: int, active_date: date | None = None
    ) -> TeacherAvailabilityValidation:
        """Validate a teacher's availability against constraints."""
        teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
        if not teacher:
            raise ValueError(f"Teacher with ID {teacher_id} not found")

        if active_date is None:
            active_date = datetime.now(UTC).date()

        # Get available hours
        available_count = (
            db.query(TeacherAvailability)
            .filter(
                TeacherAvailability.teacher_id == teacher_id,
                TeacherAvailability.availability_type == AvailabilityType.AVAILABLE,
                TeacherAvailability.effective_from <= active_date,
                (TeacherAvailability.effective_until.is_(None))
                | (TeacherAvailability.effective_until >= active_date),
            )
            .count()
        )

        # Get scheduled hours (from Schedule model)
        scheduled_count = (
            db.query(Schedule).filter(Schedule.teacher_id == teacher_id).count()
        )

        warnings = []
        conflicts = []

        # Check if part-time teacher has too many available hours
        if teacher.is_part_time and available_count > teacher.max_hours_per_week:
            warnings.append(
                f"Part-time teacher has {available_count} available hours "
                f"but max is {teacher.max_hours_per_week}"
            )

        # Check if scheduled hours exceed max
        if scheduled_count > teacher.max_hours_per_week:
            conflicts.append(
                f"Teacher has {scheduled_count} scheduled hours "
                f"but max is {teacher.max_hours_per_week}"
            )

        # Check if scheduled hours exceed available hours
        if scheduled_count > available_count:
            conflicts.append(
                f"Teacher has {scheduled_count} scheduled hours "
                f"but only {available_count} available hours"
            )

        is_valid = len(conflicts) == 0

        return TeacherAvailabilityValidation(
            teacher_id=teacher.id,
            max_hours_per_week=teacher.max_hours_per_week,
            available_hours=available_count,
            scheduled_hours=scheduled_count,
            is_valid=is_valid,
            warnings=warnings,
            conflicts=conflicts,
        )

    @staticmethod
    def get_all_teacher_overviews(
        db: Session, active_date: date | None = None
    ) -> list[TeacherAvailabilityOverview]:
        """Get availability overview for all teachers."""
        teachers = db.query(Teacher).all()
        overviews = []

        for teacher in teachers:
            try:
                overview = TeacherAvailabilityService.get_teacher_overview(
                    db, teacher.id, active_date
                )
                overviews.append(overview)
            except ValueError:
                # Skip if teacher not found (shouldn't happen)
                continue

        return overviews
