"""Teacher-Subject assignment API endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.models.database import get_db
from src.schemas.teacher_subject import (
    QualificationMatrix,
    TeacherSubjectCreate,
    TeacherSubjectResponse,
    TeacherSubjectUpdate,
    TeacherSubjectWithDetails,
    TeacherWorkload,
)
from src.services.teacher_subject import TeacherSubjectService

router = APIRouter()


# Teacher-centric endpoints
@router.post(
    "/{teacher_id}/subjects",
    response_model=TeacherSubjectResponse,
    status_code=status.HTTP_201_CREATED,
)
def assign_subject_to_teacher(
    teacher_id: int,
    assignment: TeacherSubjectCreate,
    db: Session = Depends(get_db),
) -> TeacherSubjectResponse:
    """Assign a subject to a teacher."""
    try:
        db_assignment = TeacherSubjectService.create_assignment(
            db, teacher_id, assignment
        )
        return TeacherSubjectResponse.model_validate(db_assignment)
    except ValueError as e:
        if "not found" in str(e):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
            ) from e
        if "already assigned" in str(e):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail=str(e)
            ) from e
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e


@router.get("/{teacher_id}/subjects", response_model=list[TeacherSubjectWithDetails])
def get_teacher_subjects(
    teacher_id: int, db: Session = Depends(get_db)
) -> list[TeacherSubjectWithDetails]:
    """Get all subjects assigned to a teacher."""
    assignments = TeacherSubjectService.get_teacher_subjects(db, teacher_id)
    return [TeacherSubjectWithDetails.model_validate(a) for a in assignments]


@router.put(
    "/{teacher_id}/subjects/{subject_id}",
    response_model=TeacherSubjectResponse,
)
def update_teacher_subject_assignment(
    teacher_id: int,
    subject_id: int,
    assignment_update: TeacherSubjectUpdate,
    db: Session = Depends(get_db),
) -> TeacherSubjectResponse:
    """Update a teacher-subject assignment."""
    try:
        updated_assignment = TeacherSubjectService.update_assignment(
            db, teacher_id, subject_id, assignment_update
        )
        return TeacherSubjectResponse.model_validate(updated_assignment)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e


@router.delete(
    "/{teacher_id}/subjects/{subject_id}", status_code=status.HTTP_204_NO_CONTENT
)
def remove_subject_from_teacher(
    teacher_id: int, subject_id: int, db: Session = Depends(get_db)
) -> None:
    """Remove a subject assignment from a teacher."""
    try:
        TeacherSubjectService.delete_assignment(db, teacher_id, subject_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e


@router.get("/{teacher_id}/workload", response_model=TeacherWorkload)
def get_teacher_workload(
    teacher_id: int, db: Session = Depends(get_db)
) -> TeacherWorkload:
    """Get teacher's workload calculation across all subjects."""
    try:
        workload = TeacherSubjectService.get_teacher_workload(db, teacher_id)
        return TeacherWorkload.model_validate(workload)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e


# Subject-centric endpoints (should be mounted under /subjects)
subjects_router = APIRouter()


@subjects_router.get(
    "/{subject_id}/teachers", response_model=list[TeacherSubjectWithDetails]
)
def get_qualified_teachers(
    subject_id: int, db: Session = Depends(get_db)
) -> list[TeacherSubjectWithDetails]:
    """Get all teachers qualified for a subject."""
    assignments = TeacherSubjectService.get_subject_teachers(db, subject_id)
    return [TeacherSubjectWithDetails.model_validate(a) for a in assignments]


@subjects_router.get(
    "/{subject_id}/teachers/by-grade/{grade}",
    response_model=list[TeacherSubjectWithDetails],
)
def get_teachers_by_grade(
    subject_id: int, grade: int, db: Session = Depends(get_db)
) -> list[TeacherSubjectWithDetails]:
    """Get teachers qualified for a subject at a specific grade level."""
    if not 1 <= grade <= 4:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Grade must be between 1 and 4",
        )

    assignments = TeacherSubjectService.get_subject_teachers(db, subject_id, grade)
    return [TeacherSubjectWithDetails.model_validate(a) for a in assignments]


# Matrix and overview endpoints
matrix_router = APIRouter()


@matrix_router.get("/matrix", response_model=QualificationMatrix)
def get_qualification_matrix(db: Session = Depends(get_db)) -> QualificationMatrix:
    """Get the full teacher-subject qualification matrix."""
    matrix_data = TeacherSubjectService.get_qualification_matrix(db)
    return QualificationMatrix.model_validate(matrix_data)
