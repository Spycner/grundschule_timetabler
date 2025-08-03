"""Class service for business logic."""

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.models.class_ import Class
from src.schemas.class_ import ClassCreate, ClassUpdate


class ClassService:
    """Service class for class operations."""

    @staticmethod
    def get_class(db: Session, class_id: int) -> Class | None:
        """Get a class by ID."""
        return db.query(Class).filter(Class.id == class_id).first()

    @staticmethod
    def get_class_by_name(db: Session, name: str) -> Class | None:
        """Get a class by name."""
        return db.query(Class).filter(Class.name == name).first()

    @staticmethod
    def get_classes(db: Session, skip: int = 0, limit: int = 100) -> list[Class]:
        """Get all classes with pagination."""
        return db.query(Class).offset(skip).limit(limit).all()

    @staticmethod
    def create_class(db: Session, class_: ClassCreate) -> Class:
        """Create a new class."""
        db_class = Class(**class_.model_dump())
        db.add(db_class)
        try:
            db.commit()
            db.refresh(db_class)
            return db_class
        except IntegrityError as e:
            db.rollback()
            if "name" in str(e.orig):
                raise ValueError("Class name already exists") from e
            raise

    @staticmethod
    def update_class(
        db: Session, class_id: int, class_update: ClassUpdate
    ) -> Class | None:
        """Update a class."""
        db_class = ClassService.get_class(db, class_id)
        if not db_class:
            return None

        update_data = class_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_class, field, value)

        try:
            db.commit()
            db.refresh(db_class)
            return db_class
        except IntegrityError as e:
            db.rollback()
            if "name" in str(e.orig):
                raise ValueError("Class name already exists") from e
            raise

    @staticmethod
    def delete_class(db: Session, class_id: int) -> bool:
        """Delete a class."""
        db_class = ClassService.get_class(db, class_id)
        if not db_class:
            return False

        db.delete(db_class)
        db.commit()
        return True
