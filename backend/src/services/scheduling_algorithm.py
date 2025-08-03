"""Scheduling algorithm service using OR-Tools CP-SAT solver."""

from ortools.sat.python import cp_model
from sqlalchemy.orm import Session

from src.models.class_ import Class
from src.models.schedule import Schedule
from src.models.subject import Subject
from src.models.teacher import Teacher
from src.models.teacher_availability import AvailabilityType, TeacherAvailability
from src.models.teacher_subject import QualificationLevel, TeacherSubject
from src.models.timeslot import TimeSlot
from src.schemas.schedule import ScheduleCreate
from src.services.german_constraints import GermanConstraints


class SchedulingSolution:
    """Container for scheduling algorithm results."""

    def __init__(
        self,
        schedules: list[ScheduleCreate],
        quality_score: float,
        generation_time: float,
        satisfied_constraints: list[str],
        violated_constraints: list[str],
        objective_value: int,
    ):
        self.schedules = schedules
        self.quality_score = quality_score
        self.generation_time = generation_time
        self.satisfied_constraints = satisfied_constraints
        self.violated_constraints = violated_constraints
        self.objective_value = objective_value

    @property
    def is_feasible(self) -> bool:
        """Check if the solution is feasible (no violated hard constraints)."""
        return len(self.violated_constraints) == 0

    @property
    def schedule_count(self) -> int:
        """Number of scheduled lessons."""
        return len(self.schedules)


class SchedulingAlgorithm:
    """OR-Tools CP-SAT based scheduling algorithm for German Grundschule."""

    def __init__(self, db: Session):
        self.db = db
        self.model = cp_model.CpModel()
        self.solver = cp_model.CpSolver()

        # Data containers
        self.teachers: list[Teacher] = []
        self.classes: list[Class] = []
        self.subjects: list[Subject] = []
        self.timeslots: list[TimeSlot] = []
        self.teacher_availabilities: list[TeacherAvailability] = []
        self.teacher_subjects: list[TeacherSubject] = []

        # CP-SAT variables
        self.assignment_vars: dict[tuple[int, int, int, int], cp_model.IntVar] = {}

    def load_data(self) -> None:
        """Load all necessary data from the database."""
        self.teachers = self.db.query(Teacher).all()
        self.classes = self.db.query(Class).all()
        self.subjects = self.db.query(Subject).all()
        self.timeslots = self.db.query(TimeSlot).filter(~TimeSlot.is_break).all()
        self.teacher_availabilities = self.db.query(TeacherAvailability).all()
        self.teacher_subjects = self.db.query(TeacherSubject).all()

    def create_variables(self) -> None:
        """Create CP-SAT variables for the scheduling problem."""
        # Create binary variables for each possible assignment
        # assignment[t, c, s, ts] = 1 if teacher t teaches subject s to class c at timeslot ts
        for teacher in self.teachers:
            for class_ in self.classes:
                for subject in self.subjects:
                    for timeslot in self.timeslots:
                        var_name = f"assign_t{teacher.id}_c{class_.id}_s{subject.id}_ts{timeslot.id}"
                        var = self.model.NewBoolVar(var_name)
                        self.assignment_vars[
                            (teacher.id, class_.id, subject.id, timeslot.id)
                        ] = var

    def add_hard_constraints(self) -> None:
        """Add mandatory constraints that must be satisfied."""

        # 1. Each teacher can only teach one class at a time
        for teacher in self.teachers:
            for timeslot in self.timeslots:
                teacher_assignments = []
                for class_ in self.classes:
                    for subject in self.subjects:
                        key = (teacher.id, class_.id, subject.id, timeslot.id)
                        if key in self.assignment_vars:
                            teacher_assignments.append(self.assignment_vars[key])

                if teacher_assignments:
                    self.model.Add(sum(teacher_assignments) <= 1)

        # 2. Each class can only have one lesson at a time
        for class_ in self.classes:
            for timeslot in self.timeslots:
                class_assignments = []
                for teacher in self.teachers:
                    for subject in self.subjects:
                        key = (teacher.id, class_.id, subject.id, timeslot.id)
                        if key in self.assignment_vars:
                            class_assignments.append(self.assignment_vars[key])

                if class_assignments:
                    self.model.Add(sum(class_assignments) <= 1)

        # 3. Teacher qualification constraints
        # Only allow assignments where teacher is qualified for the subject
        qualified_assignments = self._get_qualified_teacher_subject_pairs()

        for teacher in self.teachers:
            for class_ in self.classes:
                for subject in self.subjects:
                    for timeslot in self.timeslots:
                        key = (teacher.id, class_.id, subject.id, timeslot.id)
                        if (
                            key in self.assignment_vars
                            and (teacher.id, subject.id) not in qualified_assignments
                        ):
                            # If teacher is not qualified for this subject, force assignment to 0
                            self.model.Add(self.assignment_vars[key] == 0)

        # 4. Teacher availability constraints
        self._add_availability_constraints()

    def _get_qualified_teacher_subject_pairs(self) -> set[tuple[int, int]]:
        """Get set of (teacher_id, subject_id) pairs where teacher is qualified."""
        qualified_pairs = set()
        for ts in self.teacher_subjects:
            # Accept PRIMARY and SECONDARY qualifications for scheduling
            if ts.qualification_level in [
                QualificationLevel.PRIMARY,
                QualificationLevel.SECONDARY,
            ]:
                qualified_pairs.add((ts.teacher_id, ts.subject_id))
        return qualified_pairs

    def _add_availability_constraints(self) -> None:
        """Add teacher availability constraints."""
        # Build availability lookup for faster access
        availability_map = {}
        for avail in self.teacher_availabilities:
            key = (avail.teacher_id, avail.weekday, avail.period)
            availability_map[key] = avail.availability_type

        for teacher in self.teachers:
            for timeslot in self.timeslots:
                # Convert timeslot day (1-5) to weekday (0-4)
                weekday = timeslot.day - 1
                availability_key = (teacher.id, weekday, timeslot.period)

                # If teacher is explicitly blocked, prevent any assignment
                if availability_map.get(availability_key) == AvailabilityType.BLOCKED:
                    for class_ in self.classes:
                        for subject in self.subjects:
                            var_key = (teacher.id, class_.id, subject.id, timeslot.id)
                            if var_key in self.assignment_vars:
                                self.model.Add(self.assignment_vars[var_key] == 0)

    def add_german_constraints(self) -> None:
        """Add German Grundschule specific constraints."""
        german_constraints = GermanConstraints(
            model=self.model,
            assignment_vars=self.assignment_vars,
            teachers=self.teachers,
            classes=self.classes,
            subjects=self.subjects,
            timeslots=self.timeslots,
        )
        german_constraints.add_all_german_constraints()

    def add_soft_constraints(self) -> None:
        """Add optimization objectives (soft constraints)."""
        objective_terms = []

        # 1. Prefer assignments where teacher is marked as AVAILABLE (Weight: 10)
        availability_map = {}
        for avail in self.teacher_availabilities:
            key = (avail.teacher_id, avail.weekday, avail.period)
            availability_map[key] = avail.availability_type

        for teacher in self.teachers:
            for timeslot in self.timeslots:
                weekday = timeslot.day - 1
                availability_key = (teacher.id, weekday, timeslot.period)

                if availability_map.get(availability_key) == AvailabilityType.AVAILABLE:
                    # Give bonus points for using preferred time slots
                    for class_ in self.classes:
                        for subject in self.subjects:
                            var_key = (teacher.id, class_.id, subject.id, timeslot.id)
                            if var_key in self.assignment_vars:
                                objective_terms.append(
                                    self.assignment_vars[var_key] * 10
                                )

        # 2. Prefer PRIMARY qualifications over SECONDARY (Weight: 5)
        primary_qualified = set()
        for ts in self.teacher_subjects:
            if ts.qualification_level == QualificationLevel.PRIMARY:
                primary_qualified.add((ts.teacher_id, ts.subject_id))

        for teacher in self.teachers:
            for class_ in self.classes:
                for subject in self.subjects:
                    for timeslot in self.timeslots:
                        var_key = (teacher.id, class_.id, subject.id, timeslot.id)
                        if (
                            var_key in self.assignment_vars
                            and (teacher.id, subject.id) in primary_qualified
                        ):
                            objective_terms.append(self.assignment_vars[var_key] * 5)

        # 3. Prefer core subjects (Deutsch, Mathematik, Sachunterricht) in morning periods (Weight: 8)
        core_subjects = self._get_core_subjects()
        morning_periods = [1, 2, 3]

        for subject in core_subjects:
            for class_ in self.classes:
                for teacher in self.teachers:
                    for timeslot in self.timeslots:
                        if timeslot.period in morning_periods:
                            var_key = (teacher.id, class_.id, subject.id, timeslot.id)
                            if var_key in self.assignment_vars:
                                objective_terms.append(
                                    self.assignment_vars[var_key] * 8
                                )

        # TODO: Re-enable these complex constraints after fixing OR-Tools syntax
        # 4. Minimize teacher gaps between lessons (Weight: 6)
        # 5. Balance teacher workload distribution (Weight: 4)

        # 6. Prefer afternoon periods for physical education/sport (Weight: 3)
        self._add_sport_afternoon_preference(objective_terms)

        # Set objective to maximize the sum of all preference terms
        if objective_terms:
            self.model.Maximize(sum(objective_terms))

    def _get_core_subjects(self) -> list[Subject]:
        """Get core subjects (Deutsch, Mathematik, Sachunterricht)."""
        core_subject_names = {"Deutsch", "Mathematik", "Sachunterricht"}
        return [s for s in self.subjects if s.name in core_subject_names]

    def _add_minimize_teacher_gaps_objective(self, objective_terms: list) -> None:
        """Add objective terms to minimize gaps between teacher lessons."""
        # Group timeslots by day and sort by period
        timeslots_by_day = {}
        for timeslot in self.timeslots:
            if timeslot.day not in timeslots_by_day:
                timeslots_by_day[timeslot.day] = []
            timeslots_by_day[timeslot.day].append(timeslot)

        # Sort each day's timeslots by period
        for day in timeslots_by_day:
            timeslots_by_day[day].sort(key=lambda ts: ts.period)

        # For each teacher and day, prefer consecutive assignments
        for teacher in self.teachers:
            for day, day_timeslots in timeslots_by_day.items():
                for i in range(len(day_timeslots) - 1):
                    current_slot = day_timeslots[i]
                    next_slot = day_timeslots[i + 1]

                    # Create variables for whether teacher has assignment in each slot
                    current_assignments = []
                    next_assignments = []

                    for class_ in self.classes:
                        for subject in self.subjects:
                            current_key = (
                                teacher.id,
                                class_.id,
                                subject.id,
                                current_slot.id,
                            )
                            next_key = (teacher.id, class_.id, subject.id, next_slot.id)

                            if current_key in self.assignment_vars:
                                current_assignments.append(
                                    self.assignment_vars[current_key]
                                )
                            if next_key in self.assignment_vars:
                                next_assignments.append(self.assignment_vars[next_key])

                    # Bonus for having consecutive assignments
                    if current_assignments and next_assignments:
                        # Create auxiliary variables to track if teacher has assignments in both slots
                        current_has_assignment = self.model.NewBoolVar(
                            f"teacher_{teacher.id}_day_{day}_period_{current_slot.period}_has_assignment"
                        )
                        next_has_assignment = self.model.NewBoolVar(
                            f"teacher_{teacher.id}_day_{day}_period_{next_slot.period}_has_assignment"
                        )
                        consecutive_bonus = self.model.NewBoolVar(
                            f"teacher_{teacher.id}_day_{day}_consecutive_{i}"
                        )

                        # current_has_assignment = 1 if any assignment in current slot
                        self.model.Add(
                            sum(current_assignments) >= current_has_assignment
                        )
                        self.model.Add(
                            sum(current_assignments)
                            <= len(current_assignments) * current_has_assignment
                        )

                        # next_has_assignment = 1 if any assignment in next slot
                        self.model.Add(sum(next_assignments) >= next_has_assignment)
                        self.model.Add(
                            sum(next_assignments)
                            <= len(next_assignments) * next_has_assignment
                        )

                        # consecutive_bonus = 1 if both slots have assignments
                        self.model.AddBoolAnd(
                            [current_has_assignment, next_has_assignment]
                        ).OnlyEnforceIf(consecutive_bonus)
                        self.model.AddBoolOr(
                            [current_has_assignment.Not(), next_has_assignment.Not()]
                        ).OnlyEnforceIf(consecutive_bonus.Not())

                        objective_terms.append(consecutive_bonus * 6)

    def _add_workload_balance_objective(self, objective_terms: list) -> None:
        """Add objective terms to balance teacher workloads."""
        # This is a simplified version - in practice, you might want more sophisticated balancing
        # For now, we'll add a small penalty for excessive assignments to any single teacher
        for teacher in self.teachers:
            teacher_assignments = []
            for class_ in self.classes:
                for subject in self.subjects:
                    for timeslot in self.timeslots:
                        var_key = (teacher.id, class_.id, subject.id, timeslot.id)
                        if var_key in self.assignment_vars:
                            teacher_assignments.append(self.assignment_vars[var_key])

            if teacher_assignments:
                # Small bonus for having a reasonable number of assignments
                # This encourages using teachers but not overloading them
                total_assignments = sum(teacher_assignments)

                # Create auxiliary variables for different assignment count ranges
                moderate_workload = self.model.NewBoolVar(
                    f"teacher_{teacher.id}_moderate_workload"
                )

                # Moderate workload: 8-15 assignments per week (reasonable for primary school)
                self.model.Add(total_assignments >= 8).OnlyEnforceIf(moderate_workload)
                self.model.Add(total_assignments <= 15).OnlyEnforceIf(moderate_workload)
                self.model.AddBoolOr(
                    [total_assignments <= 7, total_assignments >= 16]
                ).OnlyEnforceIf(moderate_workload.Not())

                objective_terms.append(moderate_workload * 4)

    def _add_sport_afternoon_preference(self, objective_terms: list) -> None:
        """Add preference for scheduling sport/physical education in afternoon periods."""
        sport_subjects = [
            s
            for s in self.subjects
            if any(
                keyword in s.name.lower()
                for keyword in ["sport", "turnen", "bewegung", "schwimmen"]
            )
        ]

        afternoon_periods = [4, 5, 6, 7, 8]  # Later periods in the day

        for subject in sport_subjects:
            for class_ in self.classes:
                for teacher in self.teachers:
                    for timeslot in self.timeslots:
                        if timeslot.period in afternoon_periods:
                            var_key = (teacher.id, class_.id, subject.id, timeslot.id)
                            if var_key in self.assignment_vars:
                                objective_terms.append(
                                    self.assignment_vars[var_key] * 3
                                )

    def solve(
        self,
        fixed_assignments: list[Schedule] | None = None,
        time_limit_seconds: int = 60,
    ) -> SchedulingSolution:
        """
        Solve the scheduling problem.

        Args:
            fixed_assignments: Existing schedule entries to preserve
            time_limit_seconds: Maximum time to spend solving

        Returns:
            SchedulingSolution with results
        """
        import time

        start_time = time.time()

        # Load data and create model
        self.load_data()
        self.create_variables()

        # Add fixed assignments as constraints
        if fixed_assignments:
            self._add_fixed_assignment_constraints(fixed_assignments)

        # Add all constraints
        self.add_hard_constraints()
        self.add_german_constraints()
        self.add_soft_constraints()

        # Configure solver
        self.solver.parameters.max_time_in_seconds = time_limit_seconds
        self.solver.parameters.log_search_progress = True

        # Solve
        status = self.solver.Solve(self.model)

        generation_time = time.time() - start_time

        # Process results
        if status in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
            schedules = self._extract_solution()
            quality_score = self._calculate_quality_score()
            satisfied_constraints = ["All hard constraints satisfied"]
            violated_constraints = []
            objective_value = self.solver.ObjectiveValue()

            return SchedulingSolution(
                schedules=schedules,
                quality_score=quality_score,
                generation_time=generation_time,
                satisfied_constraints=satisfied_constraints,
                violated_constraints=violated_constraints,
                objective_value=objective_value,
            )
        # No feasible solution found
        return SchedulingSolution(
            schedules=[],
            quality_score=0.0,
            generation_time=generation_time,
            satisfied_constraints=[],
            violated_constraints=["No feasible solution found"],
            objective_value=0,
        )

    def _add_fixed_assignment_constraints(
        self, fixed_assignments: list[Schedule]
    ) -> None:
        """Add constraints to preserve existing schedule entries."""
        for schedule in fixed_assignments:
            var_key = (
                schedule.teacher_id,
                schedule.class_id,
                schedule.subject_id,
                schedule.timeslot_id,
            )
            if var_key in self.assignment_vars:
                # Force this assignment to be selected
                self.model.Add(self.assignment_vars[var_key] == 1)

    def _extract_solution(self) -> list[ScheduleCreate]:
        """Extract the solution from the solved model."""
        schedules = []

        for (
            teacher_id,
            class_id,
            subject_id,
            timeslot_id,
        ), var in self.assignment_vars.items():
            if self.solver.Value(var) == 1:
                schedule = ScheduleCreate(
                    teacher_id=teacher_id,
                    class_id=class_id,
                    subject_id=subject_id,
                    timeslot_id=timeslot_id,
                    room=None,  # Room assignment can be done separately
                    week_type="ALL",
                )
                schedules.append(schedule)

        return schedules

    def _calculate_quality_score(self) -> float:
        """
        Calculate a comprehensive quality score for the solution (0-100).

        The score is based on multiple factors:
        - Teacher availability satisfaction
        - Primary qualification usage
        - Core subjects in morning periods
        - Teacher gap minimization
        - Workload balance
        - Pedagogical preferences
        """
        if not hasattr(self.solver, "ObjectiveValue"):
            return 0.0

        solution_schedules = self._extract_solution()
        if not solution_schedules:
            return 0.0

        total_score = 0.0
        max_possible_score = 0.0

        # 1. Teacher availability satisfaction score (25% of total)
        availability_score, availability_max = self._calculate_availability_score(
            solution_schedules
        )
        total_score += availability_score * 0.25
        max_possible_score += availability_max * 0.25

        # 2. Qualification optimization score (20% of total)
        qualification_score, qualification_max = self._calculate_qualification_score(
            solution_schedules
        )
        total_score += qualification_score * 0.20
        max_possible_score += qualification_max * 0.20

        # 3. Pedagogical timing score (20% of total)
        pedagogical_score, pedagogical_max = self._calculate_pedagogical_score(
            solution_schedules
        )
        total_score += pedagogical_score * 0.20
        max_possible_score += pedagogical_max * 0.20

        # 4. Teacher workload balance score (15% of total)
        workload_score, workload_max = self._calculate_workload_score(
            solution_schedules
        )
        total_score += workload_score * 0.15
        max_possible_score += workload_max * 0.15

        # 5. Schedule efficiency score (10% of total)
        efficiency_score, efficiency_max = self._calculate_efficiency_score(
            solution_schedules
        )
        total_score += efficiency_score * 0.10
        max_possible_score += efficiency_max * 0.10

        # 6. German compliance score (10% of total)
        compliance_score, compliance_max = self._calculate_compliance_score(
            solution_schedules
        )
        total_score += compliance_score * 0.10
        max_possible_score += compliance_max * 0.10

        # Calculate final percentage
        if max_possible_score > 0:
            return min(100.0, (total_score / max_possible_score) * 100)
        return 0.0

    def _calculate_availability_score(
        self, schedules: list[ScheduleCreate]
    ) -> tuple[float, float]:
        """Calculate score based on teacher availability preferences."""
        availability_map = {}
        for avail in self.teacher_availabilities:
            key = (avail.teacher_id, avail.weekday, avail.period)
            availability_map[key] = avail.availability_type

        score = 0.0
        max_score = 0.0

        for schedule in schedules:
            # Find the timeslot for this schedule
            timeslot = next(
                (ts for ts in self.timeslots if ts.id == schedule.timeslot_id), None
            )
            if timeslot:
                weekday = timeslot.day - 1
                availability_key = (schedule.teacher_id, weekday, timeslot.period)
                availability = availability_map.get(availability_key)

                max_score += 1.0
                if availability == AvailabilityType.AVAILABLE:
                    score += 1.0  # Perfect match
                elif availability is None:
                    score += 0.5  # Neutral (no preference set)
                # BLOCKED would be 0 points (but should be prevented by hard constraints)

        return score, max_score

    def _calculate_qualification_score(
        self, schedules: list[ScheduleCreate]
    ) -> tuple[float, float]:
        """Calculate score based on teacher qualification types."""
        qualification_map = {}
        for ts in self.teacher_subjects:
            key = (ts.teacher_id, ts.subject_id)
            qualification_map[key] = ts.qualification_level

        score = 0.0
        max_score = len(schedules)

        for schedule in schedules:
            qualification_key = (schedule.teacher_id, schedule.subject_id)
            qualification = qualification_map.get(qualification_key)

            if qualification == QualificationLevel.PRIMARY:
                score += 1.0  # Best qualification
            elif qualification == QualificationLevel.SECONDARY:
                score += 0.7  # Good qualification
            elif qualification == QualificationLevel.SUBSTITUTE:
                score += 0.3  # Emergency qualification
            # No qualification would be 0 (but prevented by hard constraints)

        return score, max_score

    def _calculate_pedagogical_score(
        self, schedules: list[ScheduleCreate]
    ) -> tuple[float, float]:
        """Calculate score based on pedagogical best practices."""
        core_subject_ids = {s.id for s in self._get_core_subjects()}
        sport_subject_ids = {
            s.id
            for s in self.subjects
            if any(
                keyword in s.name.lower()
                for keyword in ["sport", "turnen", "bewegung", "schwimmen"]
            )
        }

        score = 0.0
        max_score = 0.0

        for schedule in schedules:
            timeslot = next(
                (ts for ts in self.timeslots if ts.id == schedule.timeslot_id), None
            )
            if timeslot:
                max_score += 1.0

                # Core subjects in morning (periods 1-3)
                if schedule.subject_id in core_subject_ids:
                    if timeslot.period <= 3:
                        score += 1.0  # Perfect timing
                    elif timeslot.period <= 5:
                        score += 0.5  # Acceptable timing
                    # Later periods get 0 points for core subjects

                # Sport in afternoon (periods 4+)
                elif schedule.subject_id in sport_subject_ids:
                    if timeslot.period >= 4:
                        score += 1.0  # Perfect timing
                    else:
                        score += 0.3  # Not ideal but acceptable

                # Other subjects are neutral
                else:
                    score += 0.7  # Neutral score for other subjects

        return score, max_score

    def _calculate_workload_score(
        self, schedules: list[ScheduleCreate]
    ) -> tuple[float, float]:
        """Calculate score based on teacher workload distribution."""
        teacher_counts = {}
        for schedule in schedules:
            teacher_counts[schedule.teacher_id] = (
                teacher_counts.get(schedule.teacher_id, 0) + 1
            )

        score = 0.0
        max_score = len(self.teachers)

        for teacher in self.teachers:
            assignments = teacher_counts.get(teacher.id, 0)

            # Ideal range: 8-15 assignments per week for primary school
            if 8 <= assignments <= 15:
                score += 1.0  # Perfect workload
            elif 5 <= assignments <= 20:
                score += 0.7  # Acceptable workload
            elif assignments > 0:
                score += 0.3  # Some work but not ideal
            # 0 assignments gets 0 points

        return score, max_score

    def _calculate_efficiency_score(
        self, schedules: list[ScheduleCreate]
    ) -> tuple[float, float]:
        """Calculate score based on schedule efficiency (gaps, coverage, etc.)."""
        # Group schedules by class to check coverage
        class_schedules = {}
        for schedule in schedules:
            if schedule.class_id not in class_schedules:
                class_schedules[schedule.class_id] = []
            class_schedules[schedule.class_id].append(schedule)

        score = 0.0
        max_score = len(self.classes)

        # Score based on how well each class schedule is distributed
        for class_id in class_schedules:
            class_schedule_list = class_schedules[class_id]

            # Group by day
            days_with_lessons = set()
            for schedule in class_schedule_list:
                timeslot = next(
                    (ts for ts in self.timeslots if ts.id == schedule.timeslot_id), None
                )
                if timeslot:
                    days_with_lessons.add(timeslot.day)

            # Prefer classes to have lessons spread across multiple days
            if len(days_with_lessons) >= 4:  # 4-5 days per week
                score += 1.0
            elif len(days_with_lessons) >= 3:  # 3 days per week
                score += 0.7
            elif len(days_with_lessons) >= 2:  # 2 days per week
                score += 0.4
            # 1 day or less gets minimal score

        return score, max_score

    def _calculate_compliance_score(
        self, schedules: list[ScheduleCreate]
    ) -> tuple[float, float]:
        """Calculate score based on German educational regulation compliance."""
        score = 0.0
        max_score = 1.0  # Single compliance score

        # Check that no break periods are used (should be prevented by hard constraints)
        break_violations = 0
        for schedule in schedules:
            timeslot = next(
                (ts for ts in self.timeslots if ts.id == schedule.timeslot_id), None
            )
            if timeslot and timeslot.is_break:
                break_violations += 1

        # Check teacher hour limits compliance
        teacher_hours = {}
        for schedule in schedules:
            teacher_hours[schedule.teacher_id] = (
                teacher_hours.get(schedule.teacher_id, 0) + 1
            )

        hour_violations = 0
        for teacher in self.teachers:
            hours = teacher_hours.get(teacher.id, 0)
            if hours > teacher.max_hours_per_week:
                hour_violations += 1

        # Calculate compliance score
        total_violations = break_violations + hour_violations
        score = 1.0 if total_violations == 0 else max(0.0, 1.0 - total_violations * 0.1)

        return score, max_score
