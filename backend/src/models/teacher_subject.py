"""Teacher-Subject association model definition."""

import enum
from datetime import UTC, date, datetime

from sqlalchemy import (
    JSON,
    CheckConstraint,
    Column,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship, validates

from src.models.database import Base


class QualificationLevel(enum.Enum):
    """Teacher qualification level for a subject."""

    PRIMARY = "PRIMARY"  # Hauptfach - Full qualification, preferred
    SECONDARY = "SECONDARY"  # Nebenfach - Can teach if needed
    SUBSTITUTE = "SUBSTITUTE"  # Vertretung - Emergency only


class TeacherSubject(Base):
    """Association between teachers and subjects with qualification details."""

    __tablename__ = "teacher_subjects"
    __table_args__ = (
        # Unique constraint: One entry per teacher-subject combination
        UniqueConstraint("teacher_id", "subject_id", name="uq_teacher_subject"),
        # Check constraint for grades
        CheckConstraint(
            "grades IS NULL OR (grades != '[]' AND JSON_ARRAY_LENGTH(grades) > 0)",
            name="ck_grades_not_empty",
        ),
    )

    id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=False, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False, index=True)
    qualification_level = Column(
        Enum(QualificationLevel), nullable=False, default=QualificationLevel.PRIMARY
    )
    grades = Column(JSON, nullable=True)  # Array of integers [1, 2, 3, 4]
    max_hours_per_week = Column(Integer, nullable=True)  # Subject-specific limit
    certification_date = Column(Date, nullable=True)  # When certification obtained
    certification_expires = Column(Date, nullable=True)  # Expiry date if applicable
    certification_document = Column(String, nullable=True)  # Document reference
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )

    # Relationships
    teacher = relationship("Teacher", backref="subject_assignments")
    subject = relationship("Subject", backref="teacher_assignments")

    @validates("grades")
    def validate_grades(self, key, grades):  # noqa: ARG002
        """Validate that grades are in valid range (1-4 for Grundschule)."""
        if grades is not None:
            if not isinstance(grades, list):
                raise ValueError("Grades must be a list")
            if not grades:
                raise ValueError("Grades list cannot be empty")
            for grade in grades:
                if not isinstance(grade, int) or not 1 <= grade <= 4:
                    raise ValueError(f"Grade must be between 1 and 4, got {grade}")
            # Sort and deduplicate
            grades = sorted(set(grades))
        return grades

    @validates("max_hours_per_week")
    def validate_max_hours(self, key, hours):  # noqa: ARG002
        """Validate max hours per week is reasonable."""
        if hours is not None and (
            not isinstance(hours, int) or hours < 1 or hours > 30
        ):
            raise ValueError(f"Max hours must be between 1 and 30, got {hours}")
        return hours

    @validates("certification_expires")
    def validate_certification_dates(self, key, expires):  # noqa: ARG002
        """Validate certification expiry is after certification date."""
        if expires and self.certification_date and expires < self.certification_date:
            raise ValueError("Certification expiry must be after certification date")
        return expires

    def is_certification_valid(self, check_date: date | None = None) -> bool:
        """Check if certification is still valid."""
        if not self.certification_expires:
            return True  # No expiry means always valid
        check_date = check_date or datetime.now(UTC).date()
        return check_date <= self.certification_expires

    def can_teach_grade(self, grade: int) -> bool:
        """Check if teacher is qualified to teach this grade."""
        if self.grades is None:
            return True  # No grade restriction means can teach all grades
        return grade in self.grades

    def get_priority_score(self) -> int:
        """Get priority score for scheduling (higher is better)."""
        scores = {
            QualificationLevel.PRIMARY: 3,
            QualificationLevel.SECONDARY: 2,
            QualificationLevel.SUBSTITUTE: 1,
        }
        return scores[self.qualification_level]

    def __repr__(self):
        """String representation of TeacherSubject."""
        return (
            f"<TeacherSubject("
            f"teacher_id={self.teacher_id}, "
            f"subject_id={self.subject_id}, "
            f"level={self.qualification_level.value}, "
            f"grades={self.grades})>"
        )
