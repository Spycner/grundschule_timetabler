"""Teacher Availability model definition."""

import enum
from datetime import UTC, date, datetime

from sqlalchemy import (
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


class AvailabilityType(enum.Enum):
    """Availability type enumeration."""

    AVAILABLE = "AVAILABLE"  # Teacher is available to teach
    BLOCKED = "BLOCKED"  # Teacher cannot teach (meetings, other duties)
    PREFERRED = "PREFERRED"  # Teacher prefers to teach (soft constraint)


class TeacherAvailability(Base):
    """Teacher availability model for tracking when teachers can teach."""

    __tablename__ = "teacher_availability"
    __table_args__ = (
        # Unique constraint: One entry per teacher/weekday/period/effective_from
        UniqueConstraint(
            "teacher_id",
            "weekday",
            "period",
            "effective_from",
            name="uq_teacher_availability",
        ),
        # Check constraints for valid ranges
        CheckConstraint("weekday >= 0 AND weekday <= 4", name="ck_weekday_range"),
        CheckConstraint("period >= 1 AND period <= 8", name="ck_period_range"),
    )

    id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=False, index=True)
    weekday = Column(Integer, nullable=False, index=True)  # 0=Monday, 4=Friday
    period = Column(Integer, nullable=False, index=True)  # 1-8
    availability_type = Column(
        Enum(AvailabilityType), nullable=False, default=AvailabilityType.AVAILABLE
    )
    effective_from = Column(Date, nullable=False, index=True)
    effective_until = Column(Date, nullable=True, index=True)  # NULL = no end date
    reason = Column(String, nullable=True)  # Optional reason for blocked/preferred
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )

    # Relationships
    teacher = relationship("Teacher", backref="availabilities")

    @validates("weekday")
    def validate_weekday(self, key, weekday):  # noqa: ARG002
        """Validate weekday is between 0 (Monday) and 4 (Friday)."""
        if not 0 <= weekday <= 4:
            raise ValueError(f"Weekday must be between 0 and 4, got {weekday}")
        return weekday

    @validates("period")
    def validate_period(self, key, period):  # noqa: ARG002
        """Validate period is between 1 and 8."""
        if not 1 <= period <= 8:
            raise ValueError(f"Period must be between 1 and 8, got {period}")
        return period

    @validates("effective_until")
    def validate_date_range(self, key, effective_until):  # noqa: ARG002
        """Validate that effective_until is after effective_from if set."""
        if (
            effective_until
            and self.effective_from
            and effective_until < self.effective_from
        ):
            raise ValueError("effective_until must be after effective_from")
        return effective_until

    def is_active_on(self, check_date: date) -> bool:
        """Check if this availability entry is active on a given date."""
        if check_date < self.effective_from:
            return False
        return not (self.effective_until and check_date > self.effective_until)

    def __repr__(self):
        """String representation of TeacherAvailability."""
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        return (
            f"<TeacherAvailability("
            f"teacher_id={self.teacher_id}, "
            f"day={days[self.weekday]}, "
            f"period={self.period}, "
            f"type={self.availability_type.value})>"
        )
