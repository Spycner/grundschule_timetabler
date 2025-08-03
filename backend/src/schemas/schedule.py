"""Schedule Pydantic schemas for API validation."""

from datetime import datetime
from datetime import time as time_type

from pydantic import BaseModel, Field, field_validator


class ScheduleBase(BaseModel):
    """Base schedule schema with shared fields."""

    class_id: int = Field(..., gt=0)
    teacher_id: int = Field(..., gt=0)
    subject_id: int = Field(..., gt=0)
    timeslot_id: int = Field(..., gt=0)
    room: str | None = Field(None, max_length=50)
    week_type: str = Field(default="ALL", pattern="^(ALL|A|B)$")

    @field_validator("week_type")
    @classmethod
    def validate_week_type(cls, v: str) -> str:
        """Ensure week_type is valid."""
        v = v.upper()
        if v not in ["ALL", "A", "B"]:
            raise ValueError("week_type must be 'ALL', 'A', or 'B'")
        return v


class ScheduleCreate(ScheduleBase):
    """Schema for creating a new schedule entry."""


class ScheduleUpdate(BaseModel):
    """Schema for updating a schedule entry (all fields optional)."""

    class_id: int | None = Field(None, gt=0)
    teacher_id: int | None = Field(None, gt=0)
    subject_id: int | None = Field(None, gt=0)
    timeslot_id: int | None = Field(None, gt=0)
    room: str | None = Field(None, max_length=50)
    week_type: str | None = Field(None, pattern="^(ALL|A|B)$")

    @field_validator("week_type")
    @classmethod
    def validate_week_type(cls, v: str | None) -> str | None:
        """Ensure week_type is valid if provided."""
        if v is not None:
            v = v.upper()
            if v not in ["ALL", "A", "B"]:
                raise ValueError("week_type must be 'ALL', 'A', or 'B'")
        return v


class TeacherSummary(BaseModel):
    """Minimal teacher info for nested responses."""

    id: int
    first_name: str
    last_name: str
    abbreviation: str

    class Config:
        """Pydantic config."""

        from_attributes = True


class ClassSummary(BaseModel):
    """Minimal class info for nested responses."""

    id: int
    name: str
    grade: int

    class Config:
        """Pydantic config."""

        from_attributes = True


class SubjectSummary(BaseModel):
    """Minimal subject info for nested responses."""

    id: int
    name: str
    code: str
    color: str

    class Config:
        """Pydantic config."""

        from_attributes = True


class TimeSlotSummary(BaseModel):
    """Minimal timeslot info for nested responses."""

    id: int
    day: int
    period: int
    start_time: time_type | str
    end_time: time_type | str
    is_break: bool

    class Config:
        """Pydantic config."""

        from_attributes = True

    @field_validator("start_time", "end_time", mode="before")
    @classmethod
    def serialize_time(cls, v):
        """Convert time objects to string for API response."""
        if isinstance(v, time_type):
            return v.strftime("%H:%M")
        return v


class ScheduleResponse(BaseModel):
    """Schema for schedule API response with nested objects."""

    id: int
    class_: ClassSummary = Field(alias="class")
    teacher: TeacherSummary
    subject: SubjectSummary
    timeslot: TimeSlotSummary
    room: str | None
    week_type: str
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic config."""

        from_attributes = True
        populate_by_name = True


class ConflictDetail(BaseModel):
    """Details about a scheduling conflict."""

    type: str  # teacher_conflict, class_conflict, room_conflict, break_conflict
    message: str
    existing_entry_id: int | None = None


class ConflictResponse(BaseModel):
    """Schema for conflict validation response."""

    valid: bool
    conflicts: list[ConflictDetail]


class BulkScheduleCreate(BaseModel):
    """Schema for bulk schedule creation."""

    entries: list[ScheduleCreate]


class ScheduleQueryParams(BaseModel):
    """Query parameters for filtering schedules."""

    week_type: str | None = Field(None, pattern="^(ALL|A|B)$")
    day: int | None = Field(None, ge=1, le=5)
    include_breaks: bool = Field(default=True)
