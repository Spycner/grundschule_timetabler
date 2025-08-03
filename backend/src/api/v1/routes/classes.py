"""Class API endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.models.database import get_db
from src.schemas.class_ import ClassCreate, ClassResponse, ClassUpdate
from src.services.class_ import ClassService

router = APIRouter()


@router.post("", response_model=ClassResponse, status_code=status.HTTP_201_CREATED)
def create_class(class_: ClassCreate, db: Session = Depends(get_db)) -> ClassResponse:
    """Create a new class."""
    try:
        db_class = ClassService.create_class(db, class_)
        return ClassResponse.model_validate(db_class)
    except ValueError as e:
        if "Class name already exists" in str(e):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Class with this name already exists",
            ) from e
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e


@router.get("", response_model=list[ClassResponse])
def get_classes(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> list[ClassResponse]:
    """Get all classes."""
    classes = ClassService.get_classes(db, skip=skip, limit=limit)
    return [ClassResponse.model_validate(class_) for class_ in classes]


@router.get("/{class_id}", response_model=ClassResponse)
def get_class(class_id: int, db: Session = Depends(get_db)) -> ClassResponse:
    """Get a specific class by ID."""
    db_class = ClassService.get_class(db, class_id)
    if db_class is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Class not found"
        )
    return ClassResponse.model_validate(db_class)


@router.put("/{class_id}", response_model=ClassResponse)
def update_class(
    class_id: int, class_update: ClassUpdate, db: Session = Depends(get_db)
) -> ClassResponse:
    """Update a class."""
    try:
        db_class = ClassService.update_class(db, class_id, class_update)
        if db_class is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Class not found"
            )
        return ClassResponse.model_validate(db_class)
    except ValueError as e:
        if "Class name already exists" in str(e):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Class with this name already exists",
            ) from e
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e


@router.delete("/{class_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_class(class_id: int, db: Session = Depends(get_db)) -> None:
    """Delete a class."""
    success = ClassService.delete_class(db, class_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Class not found"
        )
