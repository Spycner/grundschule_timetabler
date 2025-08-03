"""Schedule template schemas for reusable schedule patterns."""

from datetime import datetime

from pydantic import BaseModel, Field


class ScheduleTemplateEntry(BaseModel):
    """Individual entry in a schedule template."""

    class_name: str = Field(..., description="Class name (for template matching)")
    subject_name: str = Field(..., description="Subject name")
    teacher_name: str | None = Field(
        None, description="Preferred teacher name (optional)"
    )
    day: int = Field(..., ge=1, le=5, description="Day of week (1=Monday, 5=Friday)")
    period: int = Field(..., ge=1, le=8, description="Period number")
    week_type: str = Field(default="ALL", pattern="^(ALL|A|B)$")
    room: str | None = Field(None, description="Preferred room")


class ScheduleTemplateCreate(BaseModel):
    """Schema for creating a schedule template."""

    name: str = Field(..., min_length=1, max_length=100, description="Template name")
    description: str | None = Field(
        None, max_length=500, description="Template description"
    )
    grade_levels: list[int] = Field(
        default_factory=list, description="Applicable grade levels"
    )
    entries: list[ScheduleTemplateEntry] = Field(
        ..., min_items=1, description="Template entries"
    )


class ScheduleTemplateResponse(ScheduleTemplateCreate):
    """Schema for schedule template response."""

    id: int
    created_at: datetime
    updated_at: datetime
    usage_count: int = Field(default=0, description="Number of times template was used")


class ScheduleTemplateApplication(BaseModel):
    """Schema for applying a template to generate schedules."""

    template_id: int = Field(..., description="Template to apply")
    class_mappings: dict[str, int] = Field(
        ..., description="Map template class names to actual class IDs"
    )
    teacher_preferences: dict[str, int] = Field(
        default_factory=dict, description="Preferred teacher mappings"
    )
    override_existing: bool = Field(
        default=False, description="Override existing schedule entries"
    )


class PartialScheduleRequest(BaseModel):
    """Schema for incremental schedule building."""

    target_classes: list[int] | None = Field(
        None, description="Specific classes to schedule (all if empty)"
    )
    target_subjects: list[int] | None = Field(
        None, description="Specific subjects to schedule (all if empty)"
    )
    target_days: list[int] | None = Field(
        None, description="Specific days to schedule (all if empty)"
    )
    preserve_existing: bool = Field(default=True, description="Keep existing schedules")
    time_limit_seconds: int = Field(
        default=60, ge=10, le=300, description="Maximum solving time"
    )


class ScheduleValidationReport(BaseModel):
    """Comprehensive validation report for schedules."""

    total_entries: int
    valid_entries: int
    conflicts: list[dict]
    missing_requirements: list[str]
    quality_metrics: dict
    recommendations: list[str]
