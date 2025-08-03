"""Subject service layer for business logic."""

from sqlalchemy.orm import Session

from src.models.subject import Subject
from src.schemas.subject import SubjectCreate, SubjectUpdate


class SubjectService:
    """Service class for Subject CRUD operations."""

    @staticmethod
    def create_subject(db: Session, subject: SubjectCreate) -> Subject:
        """Create a new subject."""
        # Check for duplicate name
        existing_name = db.query(Subject).filter(Subject.name == subject.name).first()
        if existing_name:
            raise ValueError("Name already exists")

        # Check for duplicate code
        existing_code = db.query(Subject).filter(Subject.code == subject.code).first()
        if existing_code:
            raise ValueError("Code already exists")

        db_subject = Subject(**subject.model_dump())
        db.add(db_subject)
        db.commit()
        db.refresh(db_subject)
        return db_subject

    @staticmethod
    def get_subjects(db: Session, skip: int = 0, limit: int = 100) -> list[Subject]:
        """Get all subjects with pagination."""
        return db.query(Subject).offset(skip).limit(limit).all()

    @staticmethod
    def get_subject(db: Session, subject_id: int) -> Subject | None:
        """Get a subject by ID."""
        return db.query(Subject).filter(Subject.id == subject_id).first()

    @staticmethod
    def update_subject(
        db: Session, subject_id: int, subject_update: SubjectUpdate
    ) -> Subject | None:
        """Update a subject."""
        db_subject = db.query(Subject).filter(Subject.id == subject_id).first()
        if not db_subject:
            return None

        update_data = subject_update.model_dump(exclude_unset=True)

        # Check for duplicate name if updating name
        if "name" in update_data and update_data["name"] != db_subject.name:
            existing = (
                db.query(Subject)
                .filter(Subject.name == update_data["name"], Subject.id != subject_id)
                .first()
            )
            if existing:
                raise ValueError("Name already exists")

        # Check for duplicate code if updating code
        if "code" in update_data and update_data["code"] != db_subject.code:
            existing = (
                db.query(Subject)
                .filter(Subject.code == update_data["code"], Subject.id != subject_id)
                .first()
            )
            if existing:
                raise ValueError("Code already exists")

        for key, value in update_data.items():
            setattr(db_subject, key, value)

        db.commit()
        db.refresh(db_subject)
        return db_subject

    @staticmethod
    def delete_subject(db: Session, subject_id: int) -> bool:
        """Delete a subject."""
        db_subject = db.query(Subject).filter(Subject.id == subject_id).first()
        if not db_subject:
            return False

        db.delete(db_subject)
        db.commit()
        return True
