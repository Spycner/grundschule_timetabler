"""Schedule service for business logic and conflict detection."""

from datetime import UTC, datetime
from typing import TypedDict

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload

from src.models.schedule import Schedule
from src.models.subject import Subject
from src.models.teacher import Teacher
from src.models.teacher_availability import AvailabilityType
from src.models.timeslot import TimeSlot
from src.schemas.schedule import ConflictDetail, ScheduleCreate, ScheduleUpdate
from src.services.scheduling_algorithm import SchedulingAlgorithm, SchedulingSolution
from src.services.teacher_availability import TeacherAvailabilityService
from src.services.teacher_subject import TeacherSubjectService


class ScheduleStatistics(TypedDict):
    """Type definition for schedule statistics."""

    total_schedules: int
    schedules_by_teacher: dict[str, int]
    schedules_by_class: dict[str, int]
    schedules_by_subject: dict[str, int]


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

        # Check teacher qualification for the subject FIRST
        qualification = TeacherSubjectService.check_teacher_qualification(
            db, schedule.teacher_id, schedule.subject_id
        )
        if not qualification:
            conflicts.append(
                ConflictDetail(
                    type="qualification_conflict",
                    message="Teacher is not qualified to teach this subject",
                )
            )

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
            # Raise appropriate error based on conflict type (prioritize qualification first)
            if any(c.type == "qualification_conflict" for c in conflicts):
                raise ValueError("Teacher is not qualified to teach this subject")
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
            # If we get here, there's an unknown conflict type
            raise ValueError(f"Schedule conflict: {conflicts[0].message}")

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

    @staticmethod
    def generate_schedule(
        db: Session,
        preserve_existing: bool = True,
        time_limit_seconds: int = 60,
        clear_existing: bool = False,
    ) -> SchedulingSolution:
        """
        Generate a complete schedule using the scheduling algorithm.

        Args:
            db: Database session
            preserve_existing: If True, keep existing schedule entries as fixed assignments
            time_limit_seconds: Maximum time to spend solving
            clear_existing: If True, delete all existing schedules before generating

        Returns:
            SchedulingSolution with the generated schedule and metadata
        """
        # Clear existing schedules if requested
        if clear_existing:
            db.query(Schedule).delete()
            db.commit()

        # Get existing schedules to preserve
        fixed_assignments = []
        if preserve_existing and not clear_existing:
            fixed_assignments = db.query(Schedule).all()

        # Initialize and run the scheduling algorithm
        algorithm = SchedulingAlgorithm(db)
        solution = algorithm.solve(
            fixed_assignments=fixed_assignments, time_limit_seconds=time_limit_seconds
        )

        # If solution is feasible, save the new schedules to database
        if solution.is_feasible and solution.schedules:
            created_schedules = []
            for schedule_create in solution.schedules:
                # Check if this schedule already exists (to avoid duplicates)
                existing = (
                    db.query(Schedule)
                    .filter(
                        Schedule.teacher_id == schedule_create.teacher_id,
                        Schedule.class_id == schedule_create.class_id,
                        Schedule.subject_id == schedule_create.subject_id,
                        Schedule.timeslot_id == schedule_create.timeslot_id,
                        Schedule.week_type == schedule_create.week_type,
                    )
                    .first()
                )

                if not existing:
                    # Create new schedule entry
                    db_schedule = Schedule(**schedule_create.model_dump())
                    db.add(db_schedule)
                    created_schedules.append(db_schedule)

            try:
                db.commit()
                # Refresh created schedules with relationships
                for db_schedule in created_schedules:
                    db.refresh(
                        db_schedule, ["class_", "teacher", "subject", "timeslot"]
                    )
            except IntegrityError as e:
                db.rollback()
                raise ValueError("Failed to save generated schedule") from e

        return solution

    @staticmethod
    def optimize_existing_schedule(
        db: Session,
        time_limit_seconds: int = 60,
    ) -> SchedulingSolution:
        """
        Optimize the existing schedule while preserving all current assignments.

        This method is useful for improving the quality of a manually created schedule
        or for adding additional lessons to an existing schedule.

        Args:
            db: Database session
            time_limit_seconds: Maximum time to spend optimizing

        Returns:
            SchedulingSolution with optimization results
        """
        # Get all existing schedules as fixed assignments
        existing_schedules = db.query(Schedule).all()

        # Run the algorithm with all existing schedules as fixed
        algorithm = SchedulingAlgorithm(db)
        return algorithm.solve(
            fixed_assignments=existing_schedules, time_limit_seconds=time_limit_seconds
        )

    @staticmethod
    def validate_generated_schedule(
        db: Session, solution: SchedulingSolution
    ) -> list[ConflictDetail]:
        """
        Validate a generated schedule solution for any remaining conflicts.

        Args:
            db: Database session
            solution: The scheduling solution to validate

        Returns:
            List of any conflicts found
        """
        all_conflicts = []

        for schedule_create in solution.schedules:
            conflicts = ScheduleService.validate_schedule(db, schedule_create)
            all_conflicts.extend(conflicts)

        return all_conflicts

    @staticmethod
    def get_schedule_statistics(db: Session) -> ScheduleStatistics:
        """
        Get statistics about the current schedule.

        Returns:
            Dictionary with various schedule statistics
        """
        total_schedules = db.query(Schedule).count()

        # Count by teacher
        teacher_counts = {}
        teacher_schedules = (
            db.query(Schedule).options(joinedload(Schedule.teacher)).all()
        )
        for schedule in teacher_schedules:
            teacher_name = f"{schedule.teacher.first_name} {schedule.teacher.last_name}"
            teacher_counts[teacher_name] = teacher_counts.get(teacher_name, 0) + 1

        # Count by class
        class_counts = {}
        class_schedules = db.query(Schedule).options(joinedload(Schedule.class_)).all()
        for schedule in class_schedules:
            class_name = schedule.class_.name
            class_counts[class_name] = class_counts.get(class_name, 0) + 1

        # Count by subject
        subject_counts = {}
        subject_schedules = (
            db.query(Schedule).options(joinedload(Schedule.subject)).all()
        )
        for schedule in subject_schedules:
            subject_name = schedule.subject.name
            subject_counts[subject_name] = subject_counts.get(subject_name, 0) + 1

        return {
            "total_schedules": total_schedules,
            "schedules_by_teacher": teacher_counts,
            "schedules_by_class": class_counts,
            "schedules_by_subject": subject_counts,
        }

    @staticmethod
    def generate_partial_schedule(
        db: Session,
        target_classes: list[int] | None = None,
        target_subjects: list[int] | None = None,
        target_days: list[int] | None = None,
        preserve_existing: bool = True,
        time_limit_seconds: int = 60,
    ) -> SchedulingSolution:
        """
        Generate schedule for specific classes, subjects, or days only.

        This allows for incremental schedule building where you can focus
        on scheduling specific parts of the timetable.

        Args:
            db: Database session
            target_classes: List of class IDs to schedule (None = all classes)
            target_subjects: List of subject IDs to schedule (None = all subjects)
            target_days: List of days to schedule (1-5, None = all days)
            preserve_existing: Keep existing schedule entries
            time_limit_seconds: Maximum solving time

        Returns:
            SchedulingSolution with partial schedule results
        """
        # Get existing schedules to preserve
        fixed_assignments = []
        if preserve_existing:
            query = db.query(Schedule)

            # Filter out existing entries that conflict with our targets
            if target_classes or target_subjects or target_days:
                from src.models.timeslot import TimeSlot

                # Build filter conditions
                filters = []

                if target_classes:
                    filters.append(~Schedule.class_id.in_(target_classes))

                if target_subjects:
                    filters.append(~Schedule.subject_id.in_(target_subjects))

                if target_days:
                    # Join with TimeSlot to filter by day
                    query = query.join(TimeSlot)
                    filters.append(~TimeSlot.day.in_(target_days))

                if filters:
                    from sqlalchemy import and_

                    # Keep existing schedules that don't match our targets
                    query = query.filter(and_(*filters))

            fixed_assignments = query.all()

        # Create a constrained algorithm that only considers target entities
        algorithm = SchedulingAlgorithm(db)

        # Override the load_data method to filter for our targets
        algorithm.load_data()

        if target_classes:
            algorithm.classes = [c for c in algorithm.classes if c.id in target_classes]

        if target_subjects:
            algorithm.subjects = [
                s for s in algorithm.subjects if s.id in target_subjects
            ]

        if target_days:
            algorithm.timeslots = [
                ts for ts in algorithm.timeslots if ts.day in target_days
            ]

        # Solve with constraints
        solution = algorithm.solve(
            fixed_assignments=fixed_assignments, time_limit_seconds=time_limit_seconds
        )

        # Save new schedules if feasible
        if solution.is_feasible and solution.schedules:
            created_schedules = []
            for schedule_create in solution.schedules:
                # Check if this schedule already exists
                existing = (
                    db.query(Schedule)
                    .filter(
                        Schedule.teacher_id == schedule_create.teacher_id,
                        Schedule.class_id == schedule_create.class_id,
                        Schedule.subject_id == schedule_create.subject_id,
                        Schedule.timeslot_id == schedule_create.timeslot_id,
                        Schedule.week_type == schedule_create.week_type,
                    )
                    .first()
                )

                if not existing:
                    db_schedule = Schedule(**schedule_create.model_dump())
                    db.add(db_schedule)
                    created_schedules.append(db_schedule)

            try:
                db.commit()
                for db_schedule in created_schedules:
                    db.refresh(
                        db_schedule, ["class_", "teacher", "subject", "timeslot"]
                    )
            except IntegrityError as e:
                db.rollback()
                raise ValueError("Failed to save partial schedule") from e

        return solution

    @staticmethod
    def create_schedule_template(
        db: Session,
        template_name: str,
        description: str | None = None,
        class_ids: list[int] | None = None,
    ) -> dict[str, object]:
        """
        Create a schedule template from existing schedule entries.

        Templates store the pattern of schedules that can be reapplied
        to different classes or time periods.

        Args:
            db: Database session
            template_name: Name for the template
            description: Optional description
            class_ids: Specific classes to include (None = all)

        Returns:
            Dictionary with template data
        """
        query = db.query(Schedule).options(
            joinedload(Schedule.class_),
            joinedload(Schedule.teacher),
            joinedload(Schedule.subject),
            joinedload(Schedule.timeslot),
        )

        if class_ids:
            query = query.filter(Schedule.class_id.in_(class_ids))

        schedules = query.all()

        if not schedules:
            raise ValueError("No schedules found to create template")

        # Extract template entries
        template_entries = []
        for schedule in schedules:
            entry = {
                "class_name": schedule.class_.name,
                "subject_name": schedule.subject.name,
                "teacher_name": f"{schedule.teacher.first_name} {schedule.teacher.last_name}",
                "day": schedule.timeslot.day,
                "period": schedule.timeslot.period,
                "week_type": schedule.week_type,
                "room": schedule.room,
            }
            template_entries.append(entry)

        # Calculate grade levels
        grade_levels = list({schedule.class_.grade for schedule in schedules})

        return {
            "name": template_name,
            "description": description
            or f"Template created from {len(schedules)} schedule entries",
            "grade_levels": grade_levels,
            "entries": template_entries,
            "created_from_classes": [schedule.class_.name for schedule in schedules],
            "entry_count": len(template_entries),
        }

    @staticmethod
    def apply_schedule_template(
        db: Session,
        template_data: dict[str, object],
        class_mappings: dict[str, int],
        teacher_preferences: dict[str, int] | None = None,
        override_existing: bool = False,
    ) -> list[Schedule]:
        """
        Apply a schedule template to create new schedule entries.

        Args:
            db: Database session
            template_data: Template data from create_schedule_template
            class_mappings: Map template class names to actual class IDs
            teacher_preferences: Optional teacher preferences for assignments
            override_existing: Whether to replace existing schedule entries

        Returns:
            List of created schedule entries
        """
        teacher_preferences = teacher_preferences or {}
        created_schedules = []

        # Build lookup maps
        teachers_by_name = {}
        for teacher in db.query(Teacher).all():
            full_name = f"{teacher.first_name} {teacher.last_name}"
            teachers_by_name[full_name] = teacher

        subjects_by_name = {s.name: s for s in db.query(Subject).all()}

        # Get timeslots for day/period lookup
        timeslots_map = {}
        for ts in db.query(TimeSlot).all():
            timeslots_map[(ts.day, ts.period)] = ts

        entries = template_data.get("entries", [])
        if not isinstance(entries, list):
            entries = []
        for entry in entries:
            # Map template class name to actual class ID
            class_id = class_mappings.get(entry["class_name"])
            if not class_id:
                continue  # Skip if class mapping not provided

            # Find subject
            subject = subjects_by_name.get(entry["subject_name"])
            if not subject:
                continue  # Skip if subject not found

            # Find timeslot
            timeslot = timeslots_map.get((entry["day"], entry["period"]))
            if not timeslot or timeslot.is_break:
                continue  # Skip breaks and invalid timeslots

            # Find teacher (prefer user preference, fallback to template)
            teacher = None
            if entry["teacher_name"] in teacher_preferences:
                teacher_id = teacher_preferences[entry["teacher_name"]]
                teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()

            if not teacher:
                teacher = teachers_by_name.get(entry["teacher_name"])

            if not teacher:
                continue  # Skip if no suitable teacher found

            # Check if schedule already exists
            existing = (
                db.query(Schedule)
                .filter(
                    Schedule.class_id == class_id,
                    Schedule.timeslot_id == timeslot.id,
                    Schedule.week_type == entry.get("week_type", "ALL"),
                )
                .first()
            )

            if existing and not override_existing:
                continue  # Skip if exists and not overriding

            if existing and override_existing:
                db.delete(existing)

            # Create new schedule entry
            new_schedule = Schedule(
                class_id=class_id,
                teacher_id=teacher.id,
                subject_id=subject.id,
                timeslot_id=timeslot.id,
                room=entry.get("room"),
                week_type=entry.get("week_type", "ALL"),
            )

            db.add(new_schedule)
            created_schedules.append(new_schedule)

        try:
            db.commit()
            # Refresh with relationships
            for schedule in created_schedules:
                db.refresh(schedule, ["class_", "teacher", "subject", "timeslot"])
        except IntegrityError as e:
            db.rollback()
            raise ValueError("Failed to apply template - conflicts detected") from e

        return created_schedules
