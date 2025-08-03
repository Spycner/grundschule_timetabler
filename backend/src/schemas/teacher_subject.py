"""Teacher-Subject Pydantic schemas for API validation."""

from datetime import UTC, date, datetime

from pydantic import BaseModel, Field, field_validator

from src.models.teacher_subject import QualificationLevel
from src.schemas.subject import SubjectResponse
from src.schemas.teacher import TeacherResponse


class TeacherSubjectBase(BaseModel):
    """Base teacher-subject schema with shared fields."""

    subject_id: int
    qualification_level: QualificationLevel = Field(default=QualificationLevel.PRIMARY)
    grades: list[int] | None = Field(default=None)
    max_hours_per_week: int | None = Field(default=None, ge=1, le=30)
    certification_date: date | None = None
    certification_expires: date | None = None
    certification_document: str | None = Field(default=None, max_length=500)

    @field_validator("grades")
    @classmethod
    def validate_grades(cls, v: list[int] | None) -> list[int] | None:
        """Ensure grades are valid for Grundschule (1-4)."""
        if v is not None:
            if not v:
                raise ValueError("Grades list cannot be empty")
            for grade in v:
                if not 1 <= grade <= 4:
                    raise ValueError(f"Grade must be between 1 and 4, got {grade}")
            # Sort and deduplicate
            v = sorted(set(v))
        return v

    @field_validator("certification_expires")
    @classmethod
    def validate_certification_expiry(cls, v: date | None, values) -> date | None:
        """Ensure certification expiry is after certification date."""
        if v and "certification_date" in values.data:
            cert_date = values.data["certification_date"]
            if cert_date and v < cert_date:
                raise ValueError(
                    "Certification expiry must be after certification date"
                )
        return v


class TeacherSubjectCreate(TeacherSubjectBase):
    """Schema for creating a new teacher-subject assignment."""


class TeacherSubjectUpdate(BaseModel):
    """Schema for updating a teacher-subject assignment (all fields optional)."""

    qualification_level: QualificationLevel | None = None
    grades: list[int] | None = None
    max_hours_per_week: int | None = Field(default=None, ge=1, le=30)
    certification_date: date | None = None
    certification_expires: date | None = None
    certification_document: str | None = Field(default=None, max_length=500)

    @field_validator("grades")
    @classmethod
    def validate_grades(cls, v: list[int] | None) -> list[int] | None:
        """Ensure grades are valid for Grundschule (1-4) if provided."""
        if v is not None:
            if not v:
                raise ValueError("Grades list cannot be empty")
            for grade in v:
                if not 1 <= grade <= 4:
                    raise ValueError(f"Grade must be between 1 and 4, got {grade}")
            # Sort and deduplicate
            v = sorted(set(v))
        return v


class TeacherSubjectResponse(BaseModel):
    """Schema for teacher-subject assignment responses."""

    id: int
    teacher_id: int
    subject_id: int
    qualification_level: QualificationLevel
    grades: list[int] | None
    max_hours_per_week: int | None
    certification_date: date | None
    certification_expires: date | None
    certification_document: str | None
    created_at: datetime
    updated_at: datetime
    warnings: list[str] | None = None

    model_config = {"from_attributes": True}

    @field_validator("warnings", mode="before")
    @classmethod
    def check_certification_validity(cls, _v, values) -> list[str] | None:
        """Add warning if certification is expired."""
        warnings = []
        if "certification_expires" in values.data:
            expires = values.data["certification_expires"]
            if expires and expires < datetime.now(UTC).date():
                warnings.append("Certification has expired")
        return warnings if warnings else None


class TeacherSubjectWithDetails(TeacherSubjectResponse):
    """Extended response with teacher and subject details."""

    teacher: TeacherResponse
    subject: SubjectResponse

    model_config = {"from_attributes": True}


class TeacherWorkload(BaseModel):
    """Schema for teacher workload calculation."""

    teacher_id: int
    total_assigned_hours: int
    max_hours_per_week: int
    available_hours: int
    subjects: list[dict]


class QualificationMatrix(BaseModel):
    """Schema for qualification matrix overview."""

    teachers: list[TeacherResponse]
    subjects: list[SubjectResponse]
    assignments: list[TeacherSubjectResponse]
    summary: dict
