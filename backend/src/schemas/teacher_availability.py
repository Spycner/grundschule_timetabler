"""Teacher Availability Pydantic schemas for API validation."""

from datetime import date, datetime

from pydantic import BaseModel, Field, field_validator

from src.models.teacher_availability import AvailabilityType


class TeacherAvailabilityBase(BaseModel):
    """Base teacher availability schema with shared fields."""

    weekday: int = Field(..., ge=0, le=4, description="Weekday (0=Monday, 4=Friday)")
    period: int = Field(..., ge=1, le=8, description="Period (1-8)")
    availability_type: AvailabilityType = Field(
        default=AvailabilityType.AVAILABLE,
        description="Type of availability",
    )
    effective_from: date = Field(..., description="Start date for this availability")
    effective_until: date | None = Field(
        None, description="End date for this availability (optional)"
    )
    reason: str | None = Field(
        None, max_length=255, description="Reason for blocked/preferred periods"
    )

    @field_validator("effective_until")
    @classmethod
    def validate_date_range(cls, v: date | None, info) -> date | None:
        """Ensure effective_until is after effective_from if provided."""
        if v and "effective_from" in info.data and v < info.data["effective_from"]:
            raise ValueError("effective_until must be after effective_from")
        return v


class TeacherAvailabilityCreate(TeacherAvailabilityBase):
    """Schema for creating a new teacher availability entry."""


class TeacherAvailabilityUpdate(BaseModel):
    """Schema for updating teacher availability (all fields optional)."""

    weekday: int | None = Field(None, ge=0, le=4)
    period: int | None = Field(None, ge=1, le=8)
    availability_type: AvailabilityType | None = None
    effective_from: date | None = None
    effective_until: date | None = None
    reason: str | None = Field(None, max_length=255)

    @field_validator("effective_until")
    @classmethod
    def validate_date_range(cls, v: date | None, info) -> date | None:
        """Ensure effective_until is after effective_from if both provided."""
        if (
            v
            and "effective_from" in info.data
            and info.data["effective_from"]
            and v < info.data["effective_from"]
        ):
            raise ValueError("effective_until must be after effective_from")
        return v


class TeacherAvailabilityResponse(TeacherAvailabilityBase):
    """Schema for teacher availability API response."""

    id: int
    teacher_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic config."""

        from_attributes = True


class TeacherAvailabilityBulkCreate(BaseModel):
    """Schema for bulk creating teacher availability entries."""

    teacher_id: int = Field(..., description="Teacher ID")
    availabilities: list[TeacherAvailabilityCreate] = Field(
        ..., description="List of availability entries to create"
    )


class TeacherAvailabilityBulkResponse(BaseModel):
    """Response for bulk availability operations."""

    created_count: int = Field(..., description="Number of entries created")
    entries: list[TeacherAvailabilityResponse] = Field(
        ..., description="Created availability entries"
    )


class TeacherAvailabilityOverview(BaseModel):
    """Overview of a teacher's availability."""

    teacher_id: int
    teacher_name: str
    is_part_time: bool
    max_hours_per_week: int
    available_hours: int = Field(
        ..., description="Total available teaching hours per week"
    )
    blocked_hours: int = Field(..., description="Total blocked hours per week")
    preferred_hours: int = Field(..., description="Total preferred hours per week")
    availability_by_day: dict[int, dict[str, int]] = Field(
        ..., description="Breakdown by weekday"
    )


class TeacherAvailabilityValidation(BaseModel):
    """Validation result for teacher availability."""

    teacher_id: int
    max_hours_per_week: int
    available_hours: int
    scheduled_hours: int = Field(0, description="Currently scheduled teaching hours")
    is_valid: bool = Field(..., description="Whether availability meets constraints")
    warnings: list[str] = Field(
        default_factory=list, description="Any validation warnings"
    )
    conflicts: list[str] = Field(
        default_factory=list, description="Any scheduling conflicts"
    )
