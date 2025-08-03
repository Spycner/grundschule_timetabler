"""TimeSlot Pydantic schemas for API validation."""

from datetime import datetime, time

from pydantic import BaseModel, Field, field_validator, model_validator


class TimeSlotBase(BaseModel):
    """Base timeslot schema with shared fields."""

    day: int = Field(..., ge=1, le=5, description="Day of week (1=Monday to 5=Friday)")
    period: int = Field(..., ge=1, description="Period number (must be positive)")
    start_time: time
    end_time: time
    is_break: bool = Field(default=False, description="Whether this is a break period")

    @field_validator("day")
    @classmethod
    def validate_day(cls, v: int) -> int:
        """Ensure day is between 1 and 5 (Monday to Friday)."""
        if v < 1 or v > 5:
            raise ValueError("Day must be between 1 (Monday) and 5 (Friday)")
        return v

    @field_validator("period")
    @classmethod
    def validate_period(cls, v: int) -> int:
        """Ensure period is a positive integer."""
        if v < 1:
            raise ValueError("Period must be a positive integer")
        return v

    @model_validator(mode="after")
    def validate_time_range(self) -> "TimeSlotBase":
        """Ensure end_time is after start_time."""
        if self.end_time <= self.start_time:
            raise ValueError("end_time must be after start_time")
        return self


class TimeSlotCreate(TimeSlotBase):
    """Schema for creating a new timeslot."""


class TimeSlotUpdate(BaseModel):
    """Schema for updating a timeslot (all fields optional)."""

    day: int | None = Field(None, ge=1, le=5)
    period: int | None = Field(None, ge=1)
    start_time: time | None = None
    end_time: time | None = None
    is_break: bool | None = None

    @field_validator("day")
    @classmethod
    def validate_day(cls, v: int | None) -> int | None:
        """Ensure day is between 1 and 5 if provided."""
        if v is not None and (v < 1 or v > 5):
            raise ValueError("Day must be between 1 (Monday) and 5 (Friday)")
        return v

    @field_validator("period")
    @classmethod
    def validate_period(cls, v: int | None) -> int | None:
        """Ensure period is positive if provided."""
        if v is not None and v < 1:
            raise ValueError("Period must be a positive integer")
        return v

    @model_validator(mode="after")
    def validate_time_range(self) -> "TimeSlotUpdate":
        """Ensure end_time is after start_time if both are provided."""
        if (
            self.start_time is not None
            and self.end_time is not None
            and self.end_time <= self.start_time
        ):
            raise ValueError("end_time must be after start_time")
        return self


class TimeSlotResponse(TimeSlotBase):
    """Schema for timeslot API response."""

    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic config."""

        from_attributes = True


class TimeSlotListResponse(BaseModel):
    """Schema for list of timeslots response."""

    timeslots: list[TimeSlotResponse]
    total: int


class GenerateDefaultResponse(BaseModel):
    """Schema for generate default schedule response."""

    message: str
    count: int
