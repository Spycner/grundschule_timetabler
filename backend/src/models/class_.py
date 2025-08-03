"""Class model definition."""

from datetime import UTC, datetime

from sqlalchemy import Column, DateTime, Integer, String

from src.models.database import Base


class Class(Base):
    """Class model for storing class information."""

    __tablename__ = "classes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    grade = Column(Integer, nullable=False)
    size = Column(Integer, nullable=False)
    home_room = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )
