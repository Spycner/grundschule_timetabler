"""Subject Pydantic schemas for API validation."""

import re
from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class SubjectBase(BaseModel):
    """Base subject schema with shared fields."""

    name: str = Field(..., min_length=1, max_length=100)
    code: str = Field(..., min_length=2, max_length=4)
    color: str = Field(..., pattern=r"^#[0-9A-Fa-f]{6}$")

    @field_validator("code")
    @classmethod
    def validate_code(cls, v: str) -> str:
        """Ensure code is uppercase and 2-4 characters."""
        v = v.upper()
        if len(v) < 2 or len(v) > 4:
            raise ValueError("Code must be 2-4 characters long")
        return v

    @field_validator("color")
    @classmethod
    def validate_color(cls, v: str) -> str:
        """Ensure color is valid hex format (#RRGGBB)."""
        if not re.match(r"^#[0-9A-Fa-f]{6}$", v):
            raise ValueError("Color must be in hex format (#RRGGBB)")
        return v.upper()


class SubjectCreate(SubjectBase):
    """Schema for creating a new subject."""


class SubjectUpdate(BaseModel):
    """Schema for updating a subject (all fields optional)."""

    name: str | None = Field(None, min_length=1, max_length=100)
    code: str | None = Field(None, min_length=2, max_length=4)
    color: str | None = Field(None, pattern=r"^#[0-9A-Fa-f]{6}$")

    @field_validator("code")
    @classmethod
    def validate_code(cls, v: str | None) -> str | None:
        """Ensure code is uppercase and 2-4 characters if provided."""
        if v is not None:
            v = v.upper()
            if len(v) < 2 or len(v) > 4:
                raise ValueError("Code must be 2-4 characters long")
        return v

    @field_validator("color")
    @classmethod
    def validate_color(cls, v: str | None) -> str | None:
        """Ensure color is valid hex format if provided."""
        if v is not None:
            if not re.match(r"^#[0-9A-Fa-f]{6}$", v):
                raise ValueError("Color must be in hex format (#RRGGBB)")
            return v.upper()
        return v


class SubjectResponse(SubjectBase):
    """Schema for subject API response."""

    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic config."""

        from_attributes = True


class SubjectListResponse(BaseModel):
    """Schema for list of subjects response."""

    subjects: list[SubjectResponse]
    total: int
