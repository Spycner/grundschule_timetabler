"""Teacher model definition."""

from datetime import UTC, datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String

from src.models.database import Base


class Teacher(Base):
    """Teacher model for storing teacher information."""

    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    abbreviation = Column(String(3), unique=True, index=True, nullable=False)
    max_hours_per_week = Column(Integer, default=28, nullable=False)
    is_part_time = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )
