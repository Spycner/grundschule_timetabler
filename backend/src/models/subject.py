"""Subject model definition."""

from datetime import UTC, datetime

from sqlalchemy import Column, DateTime, Integer, String

from src.models.database import Base


class Subject(Base):
    """Subject model for storing subject/course information."""

    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    code = Column(String(4), unique=True, index=True, nullable=False)
    color = Column(String(7), nullable=False)  # Hex color format #RRGGBB
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )
