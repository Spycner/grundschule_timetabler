"""Teacher Pydantic schemas for API validation."""

from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, field_validator


class TeacherBase(BaseModel):
    """Base teacher schema with shared fields."""

    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    abbreviation: str = Field(..., min_length=2, max_length=3)
    max_hours_per_week: int = Field(default=28, ge=1, le=40)
    is_part_time: bool = Field(default=False)

    @field_validator("abbreviation")
    @classmethod
    def validate_abbreviation(cls, v: str) -> str:
        """Ensure abbreviation is uppercase and 2-3 characters."""
        v = v.upper()
        if len(v) < 2 or len(v) > 3:
            raise ValueError("Abbreviation must be 2-3 characters long")
        return v


class TeacherCreate(TeacherBase):
    """Schema for creating a new teacher."""


class TeacherUpdate(BaseModel):
    """Schema for updating a teacher (all fields optional)."""

    first_name: str | None = Field(None, min_length=1, max_length=100)
    last_name: str | None = Field(None, min_length=1, max_length=100)
    email: EmailStr | None = None
    abbreviation: str | None = Field(None, min_length=2, max_length=3)
    max_hours_per_week: int | None = Field(None, ge=1, le=40)
    is_part_time: bool | None = None

    @field_validator("abbreviation")
    @classmethod
    def validate_abbreviation(cls, v: str | None) -> str | None:
        """Ensure abbreviation is uppercase and 2-3 characters if provided."""
        if v is not None:
            v = v.upper()
            if len(v) < 2 or len(v) > 3:
                raise ValueError("Abbreviation must be 2-3 characters long")
        return v


class TeacherResponse(TeacherBase):
    """Schema for teacher API response."""

    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic config."""

        from_attributes = True


class TeacherListResponse(BaseModel):
    """Schema for list of teachers response."""

    teachers: list[TeacherResponse]
    total: int
