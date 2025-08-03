"""Subject API endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.models.database import get_db
from src.schemas.subject import (
    SubjectCreate,
    SubjectResponse,
    SubjectUpdate,
)
from src.services.subject import SubjectService

router = APIRouter()


@router.post("", response_model=SubjectResponse, status_code=status.HTTP_201_CREATED)
def create_subject(
    subject: SubjectCreate, db: Session = Depends(get_db)
) -> SubjectResponse:
    """Create a new subject."""
    try:
        db_subject = SubjectService.create_subject(db, subject)
        return SubjectResponse.model_validate(db_subject)
    except ValueError as e:
        if "Name already exists" in str(e):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Subject with this name already exists",
            ) from e
        if "Code already exists" in str(e):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Subject with this code already exists",
            ) from e
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e


@router.get("", response_model=list[SubjectResponse])
def get_subjects(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> list[SubjectResponse]:
    """Get all subjects."""
    subjects = SubjectService.get_subjects(db, skip=skip, limit=limit)
    return [SubjectResponse.model_validate(subject) for subject in subjects]


@router.get("/{subject_id}", response_model=SubjectResponse)
def get_subject(subject_id: int, db: Session = Depends(get_db)) -> SubjectResponse:
    """Get a specific subject by ID."""
    db_subject = SubjectService.get_subject(db, subject_id)
    if db_subject is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Subject not found"
        )
    return SubjectResponse.model_validate(db_subject)


@router.put("/{subject_id}", response_model=SubjectResponse)
def update_subject(
    subject_id: int, subject_update: SubjectUpdate, db: Session = Depends(get_db)
) -> SubjectResponse:
    """Update a subject."""
    try:
        db_subject = SubjectService.update_subject(db, subject_id, subject_update)
        if db_subject is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Subject not found"
            )
        return SubjectResponse.model_validate(db_subject)
    except ValueError as e:
        if "Name already exists" in str(e):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Subject with this name already exists",
            ) from e
        if "Code already exists" in str(e):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Subject with this code already exists",
            ) from e
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e


@router.delete("/{subject_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_subject(subject_id: int, db: Session = Depends(get_db)) -> None:
    """Delete a subject."""
    success = SubjectService.delete_subject(db, subject_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Subject not found"
        )
