"""Class Pydantic schemas for API validation."""

from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class ClassBase(BaseModel):
    """Base class schema with shared fields."""

    name: str = Field(..., min_length=1, max_length=50)
    grade: int = Field(..., ge=1, le=4)
    size: int = Field(..., ge=1, le=35)
    home_room: str | None = Field(None, max_length=50)

    @field_validator("grade")
    @classmethod
    def validate_grade(cls, v: int) -> int:
        """Ensure grade is between 1 and 4 for Grundschule."""
        if v < 1 or v > 4:
            raise ValueError("Grade must be between 1 and 4")
        return v

    @field_validator("size")
    @classmethod
    def validate_size(cls, v: int) -> int:
        """Ensure class size is reasonable."""
        if v < 1 or v > 35:
            raise ValueError("Class size must be between 1 and 35")
        return v


class ClassCreate(ClassBase):
    """Schema for creating a new class."""


class ClassUpdate(BaseModel):
    """Schema for updating a class (all fields optional)."""

    name: str | None = Field(None, min_length=1, max_length=50)
    grade: int | None = Field(None, ge=1, le=4)
    size: int | None = Field(None, ge=1, le=35)
    home_room: str | None = Field(None, max_length=50)

    @field_validator("grade")
    @classmethod
    def validate_grade(cls, v: int | None) -> int | None:
        """Ensure grade is between 1 and 4 for Grundschule if provided."""
        if v is not None and (v < 1 or v > 4):
            raise ValueError("Grade must be between 1 and 4")
        return v

    @field_validator("size")
    @classmethod
    def validate_size(cls, v: int | None) -> int | None:
        """Ensure class size is reasonable if provided."""
        if v is not None and (v < 1 or v > 35):
            raise ValueError("Class size must be between 1 and 35")
        return v


class ClassResponse(ClassBase):
    """Schema for class API response."""

    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic config."""

        from_attributes = True


class ClassListResponse(BaseModel):
    """Schema for list of classes response."""

    classes: list[ClassResponse]
    total: int
