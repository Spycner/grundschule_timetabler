"""Schedule model definition."""

from datetime import UTC, datetime

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from src.models.database import Base


class Schedule(Base):
    """Schedule model for storing timetable entries."""

    __tablename__ = "schedules"
    __table_args__ = (
        # Prevent double-booking of classes
        UniqueConstraint(
            "class_id", "timeslot_id", "week_type", name="uq_schedule_class_timeslot"
        ),
        # Prevent double-booking of teachers
        UniqueConstraint(
            "teacher_id",
            "timeslot_id",
            "week_type",
            name="uq_schedule_teacher_timeslot",
        ),
    )

    id = Column(Integer, primary_key=True, index=True)
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=False, index=True)
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=False, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False, index=True)
    timeslot_id = Column(
        Integer, ForeignKey("timeslots.id"), nullable=False, index=True
    )
    room = Column(String, nullable=True, index=True)  # Optional room assignment
    week_type = Column(String(3), nullable=False, default="ALL")  # ALL, A, or B
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )

    # Relationships
    class_ = relationship("Class", backref="schedules")
    teacher = relationship("Teacher", backref="schedules")
    subject = relationship("Subject", backref="schedules")
    timeslot = relationship("TimeSlot", backref="schedules")
