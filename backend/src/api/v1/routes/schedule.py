"""Schedule API endpoints."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from src.models.database import get_db
from src.schemas.schedule import (
    ConflictResponse,
    ScheduleCreate,
    ScheduleResponse,
    ScheduleUpdate,
)
from src.services.schedule import ScheduleService

router = APIRouter()


@router.post("", response_model=ScheduleResponse, status_code=status.HTTP_201_CREATED)
def create_schedule(
    schedule: ScheduleCreate, db: Session = Depends(get_db)
) -> ScheduleResponse:
    """Create a new schedule entry."""
    try:
        db_schedule = ScheduleService.create_schedule(db, schedule)
        return ScheduleResponse.model_validate(db_schedule)
    except ValueError as e:
        error_msg = str(e).lower()
        if "break" in error_msg:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot schedule during break periods",
            ) from e
        if "not available" in error_msg:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Teacher is not available during this period",
            ) from e
        if "teacher" in error_msg:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Teacher is already scheduled at this time",
            ) from e
        if "class" in error_msg:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Class already has a subject scheduled at this time",
            ) from e
        if "room" in error_msg:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Room is already booked at this time",
            ) from e
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e


@router.get("", response_model=list[ScheduleResponse])
def get_schedules(
    skip: int = 0,
    limit: int = 100,
    week_type: str | None = Query(None, pattern="^(ALL|A|B)$"),
    day: int | None = Query(None, ge=1, le=5),
    include_breaks: bool = True,
    db: Session = Depends(get_db),
) -> list[ScheduleResponse]:
    """Get all schedules with optional filters."""
    schedules = ScheduleService.get_schedules(
        db,
        skip=skip,
        limit=limit,
        week_type=week_type,
        day=day,
        include_breaks=include_breaks,
    )
    return [ScheduleResponse.model_validate(schedule) for schedule in schedules]


@router.get("/{schedule_id}", response_model=ScheduleResponse)
def get_schedule(schedule_id: int, db: Session = Depends(get_db)) -> ScheduleResponse:
    """Get a specific schedule entry by ID."""
    db_schedule = ScheduleService.get_schedule(db, schedule_id)
    if db_schedule is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Schedule entry not found"
        )
    return ScheduleResponse.model_validate(db_schedule)


@router.put("/{schedule_id}", response_model=ScheduleResponse)
def update_schedule(
    schedule_id: int, schedule_update: ScheduleUpdate, db: Session = Depends(get_db)
) -> ScheduleResponse:
    """Update a schedule entry."""
    try:
        db_schedule = ScheduleService.update_schedule(db, schedule_id, schedule_update)
        if db_schedule is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Schedule entry not found"
            )
        return ScheduleResponse.model_validate(db_schedule)
    except ValueError as e:
        error_msg = str(e).lower()
        if "break" in error_msg:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot schedule during break periods",
            ) from e
        if "not available" in error_msg:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Teacher is not available during this period",
            ) from e
        if "teacher" in error_msg:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Teacher is already scheduled at this time",
            ) from e
        if "class" in error_msg:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Class already has a subject scheduled at this time",
            ) from e
        if "room" in error_msg:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Room is already booked at this time",
            ) from e
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e


@router.delete("/{schedule_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_schedule(schedule_id: int, db: Session = Depends(get_db)) -> None:
    """Delete a schedule entry."""
    if not ScheduleService.delete_schedule(db, schedule_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Schedule entry not found"
        )


# View endpoints
@router.get("/class/{class_id}", response_model=list[ScheduleResponse])
def get_schedule_by_class(
    class_id: int,
    week_type: str | None = Query(None, pattern="^(ALL|A|B)$"),
    db: Session = Depends(get_db),
) -> list[ScheduleResponse]:
    """Get schedule for a specific class."""
    schedules = ScheduleService.get_schedules_by_class(db, class_id, week_type)
    return [ScheduleResponse.model_validate(schedule) for schedule in schedules]


@router.get("/teacher/{teacher_id}", response_model=list[ScheduleResponse])
def get_schedule_by_teacher(
    teacher_id: int,
    week_type: str | None = Query(None, pattern="^(ALL|A|B)$"),
    db: Session = Depends(get_db),
) -> list[ScheduleResponse]:
    """Get schedule for a specific teacher."""
    schedules = ScheduleService.get_schedules_by_teacher(db, teacher_id, week_type)
    return [ScheduleResponse.model_validate(schedule) for schedule in schedules]


@router.get("/room/{room}", response_model=list[ScheduleResponse])
def get_schedule_by_room(
    room: str,
    week_type: str | None = Query(None, pattern="^(ALL|A|B)$"),
    db: Session = Depends(get_db),
) -> list[ScheduleResponse]:
    """Get schedule for a specific room."""
    schedules = ScheduleService.get_schedules_by_room(db, room, week_type)
    return [ScheduleResponse.model_validate(schedule) for schedule in schedules]


@router.get("/timeslot/{timeslot_id}", response_model=list[ScheduleResponse])
def get_schedule_by_timeslot(
    timeslot_id: int,
    week_type: str | None = Query(None, pattern="^(ALL|A|B)$"),
    db: Session = Depends(get_db),
) -> list[ScheduleResponse]:
    """Get all schedules at a specific timeslot."""
    schedules = ScheduleService.get_schedules_by_timeslot(db, timeslot_id, week_type)
    return [ScheduleResponse.model_validate(schedule) for schedule in schedules]


# Validation endpoints
@router.post("/validate", response_model=ConflictResponse)
def validate_schedule(
    schedule: ScheduleCreate, db: Session = Depends(get_db)
) -> ConflictResponse:
    """Validate a schedule entry for conflicts without saving."""
    conflicts = ScheduleService.validate_schedule(db, schedule)
    return ConflictResponse(valid=len(conflicts) == 0, conflicts=conflicts)


@router.get("/conflicts", response_model=list[dict])
def get_all_conflicts(db: Session = Depends(get_db)) -> list[dict]:
    """Get all conflicts in the current schedule."""
    conflicts = ScheduleService.get_all_conflicts(db)
    result = []
    for schedule, conflict_list in conflicts:
        result.append(
            {
                "schedule_id": schedule.id,
                "conflicts": [conflict.model_dump() for conflict in conflict_list],
            }
        )
    return result


# Bulk operations
@router.post(
    "/bulk", response_model=list[ScheduleResponse], status_code=status.HTTP_201_CREATED
)
def create_bulk_schedules(
    schedules: list[ScheduleCreate], db: Session = Depends(get_db)
) -> list[ScheduleResponse]:
    """Create multiple schedule entries at once."""
    try:
        db_schedules = ScheduleService.create_bulk_schedules(db, schedules)
        return [ScheduleResponse.model_validate(schedule) for schedule in db_schedules]
    except ValueError as e:
        error_msg = str(e).lower()
        if "break" in error_msg:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot schedule during break periods",
            ) from e
        if "teacher" in error_msg:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Teacher conflict detected in bulk creation",
            ) from e
        if "class" in error_msg:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Class conflict detected in bulk creation",
            ) from e
        if "room" in error_msg:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Room conflict detected in bulk creation",
            ) from e
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e
