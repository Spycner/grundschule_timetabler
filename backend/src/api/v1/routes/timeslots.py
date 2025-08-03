"""TimeSlot API endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.models.database import get_db
from src.schemas.timeslot import (
    GenerateDefaultResponse,
    TimeSlotCreate,
    TimeSlotResponse,
    TimeSlotUpdate,
)
from src.services.timeslot import TimeSlotService

router = APIRouter()


@router.post("", response_model=TimeSlotResponse, status_code=status.HTTP_201_CREATED)
def create_timeslot(
    timeslot: TimeSlotCreate, db: Session = Depends(get_db)
) -> TimeSlotResponse:
    """Create a new timeslot."""
    try:
        db_timeslot = TimeSlotService.create_timeslot(db, timeslot)
        return TimeSlotResponse.model_validate(db_timeslot)
    except ValueError as e:
        if "already exists" in str(e):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(e),
            ) from e
        if "overlap" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(e),
            ) from e
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e


@router.get("", response_model=list[TimeSlotResponse])
def get_timeslots(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> list[TimeSlotResponse]:
    """Get all timeslots ordered by day and period."""
    timeslots = TimeSlotService.get_timeslots(db, skip=skip, limit=limit)
    return [TimeSlotResponse.model_validate(timeslot) for timeslot in timeslots]


@router.get("/{timeslot_id}", response_model=TimeSlotResponse)
def get_timeslot(timeslot_id: int, db: Session = Depends(get_db)) -> TimeSlotResponse:
    """Get a specific timeslot by ID."""
    db_timeslot = TimeSlotService.get_timeslot(db, timeslot_id)
    if db_timeslot is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="TimeSlot not found"
        )
    return TimeSlotResponse.model_validate(db_timeslot)


@router.put("/{timeslot_id}", response_model=TimeSlotResponse)
def update_timeslot(
    timeslot_id: int, timeslot: TimeSlotUpdate, db: Session = Depends(get_db)
) -> TimeSlotResponse:
    """Update a timeslot."""
    try:
        db_timeslot = TimeSlotService.update_timeslot(db, timeslot_id, timeslot)
        if db_timeslot is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="TimeSlot not found"
            )
        return TimeSlotResponse.model_validate(db_timeslot)
    except ValueError as e:
        if "already exists" in str(e):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(e),
            ) from e
        if "overlap" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(e),
            ) from e
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e


@router.delete("/{timeslot_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_timeslot(timeslot_id: int, db: Session = Depends(get_db)) -> None:
    """Delete a timeslot."""
    if not TimeSlotService.delete_timeslot(db, timeslot_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="TimeSlot not found"
        )


@router.post(
    "/generate-default",
    response_model=GenerateDefaultResponse,
    status_code=status.HTTP_201_CREATED,
)
def generate_default_schedule(
    db: Session = Depends(get_db),
) -> GenerateDefaultResponse:
    """Generate a default weekly schedule for a German Grundschule."""
    count = TimeSlotService.generate_default_schedule(db)
    return GenerateDefaultResponse(
        message=f"Successfully generated {count} timeslots for the weekly schedule",
        count=count,
    )
