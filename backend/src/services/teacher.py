"""Teacher service for business logic."""

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.models.teacher import Teacher
from src.schemas.teacher import TeacherCreate, TeacherUpdate


class TeacherService:
    """Service class for teacher operations."""

    @staticmethod
    def get_teacher(db: Session, teacher_id: int) -> Teacher | None:
        """Get a teacher by ID."""
        return db.query(Teacher).filter(Teacher.id == teacher_id).first()

    @staticmethod
    def get_teacher_by_email(db: Session, email: str) -> Teacher | None:
        """Get a teacher by email."""
        return db.query(Teacher).filter(Teacher.email == email).first()

    @staticmethod
    def get_teacher_by_abbreviation(db: Session, abbreviation: str) -> Teacher | None:
        """Get a teacher by abbreviation."""
        return db.query(Teacher).filter(Teacher.abbreviation == abbreviation).first()

    @staticmethod
    def get_teachers(db: Session, skip: int = 0, limit: int = 100) -> list[Teacher]:
        """Get all teachers with pagination."""
        return db.query(Teacher).offset(skip).limit(limit).all()

    @staticmethod
    def create_teacher(db: Session, teacher: TeacherCreate) -> Teacher:
        """Create a new teacher."""
        db_teacher = Teacher(**teacher.model_dump())
        db.add(db_teacher)
        try:
            db.commit()
            db.refresh(db_teacher)
            return db_teacher
        except IntegrityError as e:
            db.rollback()
            if "email" in str(e.orig):
                raise ValueError("Email already exists") from e
            if "abbreviation" in str(e.orig):
                raise ValueError("Abbreviation already exists") from e
            raise

    @staticmethod
    def update_teacher(
        db: Session, teacher_id: int, teacher_update: TeacherUpdate
    ) -> Teacher | None:
        """Update a teacher."""
        db_teacher = TeacherService.get_teacher(db, teacher_id)
        if not db_teacher:
            return None

        update_data = teacher_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_teacher, field, value)

        try:
            db.commit()
            db.refresh(db_teacher)
            return db_teacher
        except IntegrityError as e:
            db.rollback()
            if "email" in str(e.orig):
                raise ValueError("Email already exists") from e
            if "abbreviation" in str(e.orig):
                raise ValueError("Abbreviation already exists") from e
            raise

    @staticmethod
    def delete_teacher(db: Session, teacher_id: int) -> bool:
        """Delete a teacher."""
        db_teacher = TeacherService.get_teacher(db, teacher_id)
        if not db_teacher:
            return False

        db.delete(db_teacher)
        db.commit()
        return True
