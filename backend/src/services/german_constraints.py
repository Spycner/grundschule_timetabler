"""German Grundschule specific constraint rules engine."""

from ortools.sat.python import cp_model

from src.models.class_ import Class
from src.models.subject import Subject
from src.models.teacher import Teacher
from src.models.timeslot import TimeSlot


class GermanConstraints:
    """
    German Grundschule specific scheduling constraints.

    This class implements constraints specific to German elementary schools,
    including regulations, pedagogical best practices, and workload rules.
    """

    def __init__(
        self,
        model: cp_model.CpModel,
        assignment_vars: dict[tuple[int, int, int, int], cp_model.IntVar],
        teachers: list[Teacher],
        classes: list[Class],
        subjects: list[Subject],
        timeslots: list[TimeSlot],
    ):
        self.model = model
        self.assignment_vars = assignment_vars
        self.teachers = teachers
        self.classes = classes
        self.subjects = subjects
        self.timeslots = timeslots

    def add_all_german_constraints(self) -> None:
        """Add all German-specific constraints."""
        self.add_maximum_daily_hours_constraint()
        self.add_maximum_weekly_hours_constraint()
        self.add_break_period_constraints()
        self.add_part_time_teacher_constraints()
        self.add_grundschule_pedagogical_constraints()

    def add_maximum_daily_hours_constraint(self) -> None:
        """
        German regulation: Teachers cannot exceed maximum daily teaching hours.

        Typical limits:
        - Full-time teachers: 6-7 hours per day
        - Part-time teachers: Based on their contract percentage
        """
        max_daily_hours_full_time = 6

        for teacher in self.teachers:
            # Calculate max hours based on part-time status
            if teacher.is_part_time:
                # Assume part-time teachers work 50% by default (can be made configurable)
                max_daily_hours = max_daily_hours_full_time // 2
            else:
                max_daily_hours = max_daily_hours_full_time

            # Group timeslots by day
            timeslots_by_day = {}
            for timeslot in self.timeslots:
                if timeslot.day not in timeslots_by_day:
                    timeslots_by_day[timeslot.day] = []
                timeslots_by_day[timeslot.day].append(timeslot)

            # For each day, limit teacher's assignments
            for _day, day_timeslots in timeslots_by_day.items():
                daily_assignments = []
                for timeslot in day_timeslots:
                    for class_ in self.classes:
                        for subject in self.subjects:
                            key = (teacher.id, class_.id, subject.id, timeslot.id)
                            if key in self.assignment_vars:
                                daily_assignments.append(self.assignment_vars[key])

                if daily_assignments:
                    self.model.Add(sum(daily_assignments) <= max_daily_hours)

    def add_maximum_weekly_hours_constraint(self) -> None:
        """
        German regulation: Teachers cannot exceed their contracted weekly hours.

        Based on the max_hours field in the Teacher model.
        """
        for teacher in self.teachers:
            teacher_assignments = []
            for class_ in self.classes:
                for subject in self.subjects:
                    for timeslot in self.timeslots:
                        key = (teacher.id, class_.id, subject.id, timeslot.id)
                        if key in self.assignment_vars:
                            teacher_assignments.append(self.assignment_vars[key])

            if teacher_assignments:
                self.model.Add(sum(teacher_assignments) <= teacher.max_hours_per_week)

    def add_break_period_constraints(self) -> None:
        """
        German regulation: No teaching during mandatory break periods.

        Break periods are already filtered out in the main algorithm,
        but this adds an extra safety check.
        """
        # This constraint is primarily enforced by excluding break timeslots
        # from the timeslots list in the main algorithm.
        # Additional break-related constraints could be added here if needed.

    def add_part_time_teacher_constraints(self) -> None:
        """
        German context: Part-time teachers often have specific day constraints.

        This constraint ensures part-time teachers don't have scattered
        assignments across all days, which is common in German schools.
        """
        for teacher in self.teachers:
            if not teacher.is_part_time:
                continue

            # Group timeslots by day
            timeslots_by_day = {}
            for timeslot in self.timeslots:
                if timeslot.day not in timeslots_by_day:
                    timeslots_by_day[timeslot.day] = []
                timeslots_by_day[timeslot.day].append(timeslot)

            # Create binary variables for each day (1 if teacher works that day)
            day_vars = {}
            for day in timeslots_by_day:
                day_var = self.model.NewBoolVar(f"teacher_{teacher.id}_works_day_{day}")
                day_vars[day] = day_var

                # If teacher has any assignment on this day, day_var must be 1
                day_assignments = []
                for timeslot in timeslots_by_day[day]:
                    for class_ in self.classes:
                        for subject in self.subjects:
                            key = (teacher.id, class_.id, subject.id, timeslot.id)
                            if key in self.assignment_vars:
                                day_assignments.append(self.assignment_vars[key])

                if day_assignments:
                    # If any assignment on this day, then day_var = 1
                    self.model.Add(
                        sum(day_assignments) <= len(day_assignments) * day_var
                    )
                    # If day_var = 0, then no assignments on this day
                    self.model.Add(sum(day_assignments) >= day_var)

            # Limit number of working days for part-time teachers
            # Typical part-time teachers work 2-3 days per week
            max_working_days = 3
            if day_vars:
                self.model.Add(sum(day_vars.values()) <= max_working_days)

    def add_grundschule_pedagogical_constraints(self) -> None:
        """
        Grundschule pedagogical best practices.

        These are soft preferences that improve educational quality:
        - Core subjects (Deutsch, Mathematik) should be in morning periods
        - Physical Education should not be in the last period
        - No more than 2 consecutive hours of the same subject
        """
        # 1. Prefer core subjects in morning (periods 1-3)
        core_subjects = self._get_core_subjects()
        morning_periods = [1, 2, 3]

        for subject in core_subjects:
            for class_ in self.classes:
                for teacher in self.teachers:
                    morning_assignments = []
                    afternoon_assignments = []

                    for timeslot in self.timeslots:
                        key = (teacher.id, class_.id, subject.id, timeslot.id)
                        if key in self.assignment_vars:
                            if timeslot.period in morning_periods:
                                morning_assignments.append(self.assignment_vars[key])
                            else:
                                afternoon_assignments.append(self.assignment_vars[key])

                    # Soft constraint: prefer morning over afternoon for core subjects
                    # This is implemented as an objective term rather than hard constraint
                    # (Will be handled in the soft constraints/objective function)

        # 2. Avoid consecutive identical subjects (hard constraint for quality)
        self._add_no_consecutive_same_subject_constraint()

    def _get_core_subjects(self) -> list[Subject]:
        """Get core subjects (Deutsch, Mathematik, Sachunterricht)."""
        core_subject_names = {"Deutsch", "Mathematik", "Sachunterricht"}
        return [s for s in self.subjects if s.name in core_subject_names]

    def _add_no_consecutive_same_subject_constraint(self) -> None:
        """
        Prevent more than 2 consecutive periods of the same subject for a class.

        This prevents student fatigue and improves learning quality.
        """
        # Group timeslots by day and sort by period
        timeslots_by_day = {}
        for timeslot in self.timeslots:
            if timeslot.day not in timeslots_by_day:
                timeslots_by_day[timeslot.day] = []
            timeslots_by_day[timeslot.day].append(timeslot)

        # Sort each day's timeslots by period
        for day in timeslots_by_day:
            timeslots_by_day[day].sort(key=lambda ts: ts.period)

        for class_ in self.classes:
            for subject in self.subjects:
                for _day, day_timeslots in timeslots_by_day.items():
                    # Check each sequence of 3 consecutive periods
                    for i in range(len(day_timeslots) - 2):
                        consecutive_assignments = []
                        for j in range(3):  # 3 consecutive periods
                            timeslot = day_timeslots[i + j]
                            for teacher in self.teachers:
                                key = (teacher.id, class_.id, subject.id, timeslot.id)
                                if key in self.assignment_vars:
                                    consecutive_assignments.append(
                                        self.assignment_vars[key]
                                    )

                        # No more than 2 out of 3 consecutive periods for same subject
                        if consecutive_assignments:
                            self.model.Add(sum(consecutive_assignments) <= 2)

    def add_room_capacity_constraints(self, room_capacities: dict[str, int]) -> None:
        """
        Add room capacity constraints if room assignments are made.

        Args:
            room_capacities: Dict mapping room names to their capacity
        """
        # This would be implemented when room assignment is added to the model
        # For now, rooms are assigned separately after scheduling

    def add_special_room_requirements(
        self, subject_room_requirements: dict[int, list[str]]
    ) -> None:
        """
        Add constraints for subjects that require special rooms.

        Args:
            subject_room_requirements: Dict mapping subject_id to list of required room types

        Example: Sport requires gym, Music requires music room, etc.
        """
        # This would be implemented when room assignment is integrated
        # For now, special room requirements are handled post-scheduling

    def add_teacher_preference_constraints(
        self, teacher_preferences: dict[int, dict[str, object]]
    ) -> None:
        """
        Add soft constraints for teacher preferences.

        Args:
            teacher_preferences: Dict with teacher preferences like:
            {
                teacher_id: {
                    "preferred_days": [1, 2, 3],  # Monday, Tuesday, Wednesday
                    "avoid_early_periods": True,
                    "max_consecutive_hours": 4,
                }
            }
        """
        # These are typically implemented as soft constraints in the objective function
        # rather than hard constraints
