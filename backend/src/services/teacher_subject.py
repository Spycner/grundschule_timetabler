"""Service layer for TeacherSubject operations."""

from sqlalchemy import and_
from sqlalchemy.orm import Session, joinedload

from src.models.subject import Subject
from src.models.teacher import Teacher
from src.models.teacher_subject import QualificationLevel, TeacherSubject
from src.schemas.teacher_subject import (
    TeacherSubjectCreate,
    TeacherSubjectUpdate,
)


class TeacherSubjectService:
    """Service for managing teacher-subject assignments."""

    @staticmethod
    def create_assignment(
        db: Session, teacher_id: int, assignment: TeacherSubjectCreate
    ) -> TeacherSubject:
        """Create a new teacher-subject assignment."""
        # Check if teacher exists
        teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
        if not teacher:
            raise ValueError("Teacher not found")

        # Check if subject exists
        subject = db.query(Subject).filter(Subject.id == assignment.subject_id).first()
        if not subject:
            raise ValueError("Subject not found")

        # Check for duplicate assignment
        existing = (
            db.query(TeacherSubject)
            .filter(
                and_(
                    TeacherSubject.teacher_id == teacher_id,
                    TeacherSubject.subject_id == assignment.subject_id,
                )
            )
            .first()
        )
        if existing:
            raise ValueError("Teacher is already assigned to this subject")

        # Create new assignment
        db_assignment = TeacherSubject(teacher_id=teacher_id, **assignment.model_dump())
        db.add(db_assignment)
        db.commit()
        db.refresh(db_assignment)
        return db_assignment

    @staticmethod
    def get_teacher_subjects(db: Session, teacher_id: int) -> list[TeacherSubject]:
        """Get all subjects assigned to a teacher."""
        return (
            db.query(TeacherSubject)
            .options(joinedload(TeacherSubject.subject))
            .filter(TeacherSubject.teacher_id == teacher_id)
            .order_by(TeacherSubject.qualification_level)
            .all()
        )

    @staticmethod
    def get_subject_teachers(
        db: Session, subject_id: int, grade: int | None = None
    ) -> list[TeacherSubject]:
        """Get all teachers qualified for a subject, optionally filtered by grade."""
        query = (
            db.query(TeacherSubject)
            .options(joinedload(TeacherSubject.teacher))
            .filter(TeacherSubject.subject_id == subject_id)
        )

        if grade is not None:
            # Filter by grade in Python after fetching - simpler than complex JSON queries
            pass  # We'll filter in Python below

        # Order by qualification level (PRIMARY first)
        results = query.order_by(
            TeacherSubject.qualification_level,
            TeacherSubject.teacher_id,
        ).all()

        # Filter by grade in Python if needed
        if grade is not None:
            results = [r for r in results if r.can_teach_grade(grade)]

        return results

    @staticmethod
    def update_assignment(
        db: Session,
        teacher_id: int,
        subject_id: int,
        assignment_update: TeacherSubjectUpdate,
    ) -> TeacherSubject:
        """Update an existing teacher-subject assignment."""
        assignment = (
            db.query(TeacherSubject)
            .filter(
                and_(
                    TeacherSubject.teacher_id == teacher_id,
                    TeacherSubject.subject_id == subject_id,
                )
            )
            .first()
        )

        if not assignment:
            raise ValueError("Assignment not found")

        # Update fields
        update_data = assignment_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(assignment, field, value)

        db.commit()
        db.refresh(assignment)
        return assignment

    @staticmethod
    def delete_assignment(db: Session, teacher_id: int, subject_id: int) -> None:
        """Delete a teacher-subject assignment."""
        assignment = (
            db.query(TeacherSubject)
            .filter(
                and_(
                    TeacherSubject.teacher_id == teacher_id,
                    TeacherSubject.subject_id == subject_id,
                )
            )
            .first()
        )

        if not assignment:
            raise ValueError("Assignment not found")

        db.delete(assignment)
        db.commit()

    @staticmethod
    def get_qualification_matrix(db: Session) -> dict:
        """Get a matrix of all teacher-subject qualifications."""
        teachers = db.query(Teacher).order_by(Teacher.last_name).all()
        subjects = db.query(Subject).order_by(Subject.name).all()
        assignments = (
            db.query(TeacherSubject)
            .options(
                joinedload(TeacherSubject.teacher),
                joinedload(TeacherSubject.subject),
            )
            .all()
        )

        # Build summary statistics
        summary = {
            "total_teachers": len(teachers),
            "total_subjects": len(subjects),
            "total_assignments": len(assignments),
            "primary_qualifications": sum(
                1
                for a in assignments
                if a.qualification_level == QualificationLevel.PRIMARY
            ),
            "secondary_qualifications": sum(
                1
                for a in assignments
                if a.qualification_level == QualificationLevel.SECONDARY
            ),
            "substitute_qualifications": sum(
                1
                for a in assignments
                if a.qualification_level == QualificationLevel.SUBSTITUTE
            ),
        }

        return {
            "teachers": teachers,
            "subjects": subjects,
            "assignments": assignments,
            "summary": summary,
        }

    @staticmethod
    def get_teacher_workload(db: Session, teacher_id: int) -> dict:
        """Calculate teacher's workload across all subjects."""
        teacher = db.query(Teacher).filter(Teacher.id == teacher_id).first()
        if not teacher:
            raise ValueError("Teacher not found")

        assignments = (
            db.query(TeacherSubject)
            .options(joinedload(TeacherSubject.subject))
            .filter(TeacherSubject.teacher_id == teacher_id)
            .all()
        )

        total_hours = sum(a.max_hours_per_week or 0 for a in assignments)
        available_hours = teacher.max_hours_per_week - total_hours

        subjects_data = [
            {
                "subject_id": a.subject_id,
                "subject_name": a.subject.name,
                "qualification_level": a.qualification_level.value,
                "max_hours_per_week": a.max_hours_per_week or 0,
                "grades": a.grades,
            }
            for a in assignments
        ]

        return {
            "teacher_id": teacher_id,
            "total_assigned_hours": total_hours,
            "max_hours_per_week": teacher.max_hours_per_week,
            "available_hours": available_hours,
            "subjects": subjects_data,
        }

    @staticmethod
    def check_teacher_qualification(
        db: Session, teacher_id: int, subject_id: int, grade: int | None = None
    ) -> TeacherSubject | None:
        """Check if a teacher is qualified to teach a subject."""
        query = db.query(TeacherSubject).filter(
            and_(
                TeacherSubject.teacher_id == teacher_id,
                TeacherSubject.subject_id == subject_id,
            )
        )

        assignment = query.first()
        if not assignment:
            return None

        # Check grade if specified
        if grade is not None and not assignment.can_teach_grade(grade):
            return None

        # Check certification validity
        if not assignment.is_certification_valid():
            return None

        return assignment

    @staticmethod
    def get_best_qualified_teacher(
        db: Session, subject_id: int, grade: int, available_teacher_ids: list[int]
    ) -> TeacherSubject | None:
        """Find the best qualified available teacher for a subject and grade."""
        assignments = (
            db.query(TeacherSubject)
            .filter(
                and_(
                    TeacherSubject.subject_id == subject_id,
                    TeacherSubject.teacher_id.in_(available_teacher_ids),
                )
            )
            .all()
        )

        # Filter by grade and certification validity
        valid_assignments = [
            a
            for a in assignments
            if a.can_teach_grade(grade) and a.is_certification_valid()
        ]

        if not valid_assignments:
            return None

        # Sort by qualification level (PRIMARY > SECONDARY > SUBSTITUTE)
        valid_assignments.sort(key=lambda a: a.get_priority_score(), reverse=True)
        return valid_assignments[0]
