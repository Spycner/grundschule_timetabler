"""Teacher Availability API endpoints."""

from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from src.models.database import get_db
from src.schemas.teacher_availability import (
    TeacherAvailabilityBulkCreate,
    TeacherAvailabilityBulkResponse,
    TeacherAvailabilityCreate,
    TeacherAvailabilityOverview,
    TeacherAvailabilityResponse,
    TeacherAvailabilityUpdate,
    TeacherAvailabilityValidation,
)
from src.services.teacher_availability import TeacherAvailabilityService

router = APIRouter()


@router.post(
    "/{teacher_id}/availability",
    response_model=TeacherAvailabilityResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_teacher_availability(
    teacher_id: int,
    availability: TeacherAvailabilityCreate,
    db: Session = Depends(get_db),
) -> TeacherAvailabilityResponse:
    """Create a new availability entry for a teacher."""
    try:
        db_availability = TeacherAvailabilityService.create_availability(
            db, teacher_id, availability
        )
        return TeacherAvailabilityResponse.model_validate(db_availability)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e


@router.get(
    "/{teacher_id}/availability",
    response_model=list[TeacherAvailabilityResponse],
)
def get_teacher_availability(
    teacher_id: int,
    weekday: int | None = Query(None, ge=0, le=4),
    period: int | None = Query(None, ge=1, le=8),
    active_date: date | None = None,
    db: Session = Depends(get_db),
) -> list[TeacherAvailabilityResponse]:
    """Get all availability entries for a teacher."""
    availabilities = TeacherAvailabilityService.get_teacher_availability(
        db, teacher_id, weekday, period, active_date
    )
    return [TeacherAvailabilityResponse.model_validate(av) for av in availabilities]


@router.put(
    "/{teacher_id}/availability/{availability_id}",
    response_model=TeacherAvailabilityResponse,
)
def update_teacher_availability(
    teacher_id: int,
    availability_id: int,
    availability_update: TeacherAvailabilityUpdate,
    db: Session = Depends(get_db),
) -> TeacherAvailabilityResponse:
    """Update an existing availability entry."""
    # First check if the availability belongs to the teacher
    db_availability = TeacherAvailabilityService.get_availability(db, availability_id)
    if not db_availability:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Availability with ID {availability_id} not found",
        )

    if db_availability.teacher_id != teacher_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Availability does not belong to this teacher",
        )

    try:
        updated_availability = TeacherAvailabilityService.update_availability(
            db, availability_id, availability_update
        )
        return TeacherAvailabilityResponse.model_validate(updated_availability)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e


@router.delete(
    "/{teacher_id}/availability/{availability_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_teacher_availability(
    teacher_id: int,
    availability_id: int,
    db: Session = Depends(get_db),
) -> None:
    """Delete an availability entry."""
    # First check if the availability belongs to the teacher
    db_availability = TeacherAvailabilityService.get_availability(db, availability_id)
    if not db_availability:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Availability with ID {availability_id} not found",
        )

    if db_availability.teacher_id != teacher_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Availability does not belong to this teacher",
        )

    if not TeacherAvailabilityService.delete_availability(db, availability_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Availability with ID {availability_id} not found",
        )


@router.post(
    "/availability/bulk",
    response_model=TeacherAvailabilityBulkResponse,
    status_code=status.HTTP_201_CREATED,
)
def bulk_create_availability(
    bulk_data: TeacherAvailabilityBulkCreate, db: Session = Depends(get_db)
) -> TeacherAvailabilityBulkResponse:
    """Bulk create availability entries for a teacher."""
    try:
        count, entries = TeacherAvailabilityService.bulk_create_availability(
            db, bulk_data.teacher_id, bulk_data.availabilities
        )
        return TeacherAvailabilityBulkResponse(
            created_count=count,
            entries=[TeacherAvailabilityResponse.model_validate(e) for e in entries],
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e


@router.get(
    "/{teacher_id}/availability/overview",
    response_model=TeacherAvailabilityOverview,
)
def get_teacher_availability_overview(
    teacher_id: int,
    active_date: date | None = None,
    db: Session = Depends(get_db),
) -> TeacherAvailabilityOverview:
    """Get an overview of a teacher's availability."""
    try:
        return TeacherAvailabilityService.get_teacher_overview(
            db, teacher_id, active_date
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e


@router.get(
    "/{teacher_id}/availability/validate",
    response_model=TeacherAvailabilityValidation,
)
def validate_teacher_availability(
    teacher_id: int,
    active_date: date | None = None,
    db: Session = Depends(get_db),
) -> TeacherAvailabilityValidation:
    """Validate a teacher's availability against constraints."""
    try:
        return TeacherAvailabilityService.validate_teacher_availability(
            db, teacher_id, active_date
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e


@router.get(
    "/availability/overview",
    response_model=dict,
)
def get_all_teachers_availability_overview(
    active_date: date | None = None, db: Session = Depends(get_db)
) -> dict:
    """Get availability overview for all teachers."""
    overviews = TeacherAvailabilityService.get_all_teacher_overviews(db, active_date)
    return {
        "teachers": [overview.model_dump() for overview in overviews],
        "total": len(overviews),
    }
