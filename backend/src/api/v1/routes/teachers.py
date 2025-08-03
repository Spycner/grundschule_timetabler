"""Teacher API endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.models.database import get_db
from src.schemas.teacher import (
    TeacherCreate,
    TeacherResponse,
    TeacherUpdate,
)
from src.services.teacher import TeacherService

router = APIRouter()


@router.post("", response_model=TeacherResponse, status_code=status.HTTP_201_CREATED)
def create_teacher(
    teacher: TeacherCreate, db: Session = Depends(get_db)
) -> TeacherResponse:
    """Create a new teacher."""
    try:
        db_teacher = TeacherService.create_teacher(db, teacher)
        return TeacherResponse.model_validate(db_teacher)
    except ValueError as e:
        if "Email already exists" in str(e):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Teacher with this email already exists",
            ) from e
        if "Abbreviation already exists" in str(e):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Teacher with this abbreviation already exists",
            ) from e
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e


@router.get("", response_model=list[TeacherResponse])
def get_teachers(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> list[TeacherResponse]:
    """Get all teachers."""
    teachers = TeacherService.get_teachers(db, skip=skip, limit=limit)
    return [TeacherResponse.model_validate(teacher) for teacher in teachers]


@router.get("/{teacher_id}", response_model=TeacherResponse)
def get_teacher(teacher_id: int, db: Session = Depends(get_db)) -> TeacherResponse:
    """Get a specific teacher by ID."""
    db_teacher = TeacherService.get_teacher(db, teacher_id)
    if db_teacher is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Teacher not found"
        )
    return TeacherResponse.model_validate(db_teacher)


@router.put("/{teacher_id}", response_model=TeacherResponse)
def update_teacher(
    teacher_id: int, teacher_update: TeacherUpdate, db: Session = Depends(get_db)
) -> TeacherResponse:
    """Update a teacher."""
    try:
        db_teacher = TeacherService.update_teacher(db, teacher_id, teacher_update)
        if db_teacher is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Teacher not found"
            )
        return TeacherResponse.model_validate(db_teacher)
    except ValueError as e:
        if "Email already exists" in str(e):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Teacher with this email already exists",
            ) from e
        if "Abbreviation already exists" in str(e):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Teacher with this abbreviation already exists",
            ) from e
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e


@router.delete("/{teacher_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_teacher(teacher_id: int, db: Session = Depends(get_db)) -> None:
    """Delete a teacher."""
    success = TeacherService.delete_teacher(db, teacher_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Teacher not found"
        )
