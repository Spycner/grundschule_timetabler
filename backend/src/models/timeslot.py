"""TimeSlot model definition."""

from datetime import UTC, datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, Time, UniqueConstraint

from src.models.database import Base


class TimeSlot(Base):
    """TimeSlot model for storing weekly schedule grid structure."""

    __tablename__ = "timeslots"
    __table_args__ = (UniqueConstraint("day", "period", name="uq_timeslot_day_period"),)

    id = Column(Integer, primary_key=True, index=True)
    day = Column(Integer, nullable=False)  # 1=Monday, 2=Tuesday, ..., 5=Friday
    period = Column(Integer, nullable=False)  # 1=first period, 2=second, etc.
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    is_break = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )
