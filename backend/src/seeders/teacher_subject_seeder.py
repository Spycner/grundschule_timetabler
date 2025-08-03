"""Seeder for teacher-subject assignments with realistic German school data."""

from datetime import UTC, date, datetime

from sqlalchemy.orm import Session

from src.models.subject import Subject
from src.models.teacher import Teacher
from src.models.teacher_subject import QualificationLevel, TeacherSubject


class TeacherSubjectSeeder:
    """Seeder class for creating realistic teacher-subject assignments."""

    @staticmethod
    def seed(db: Session) -> None:
        """Seed teacher-subject assignments with realistic data."""
        print("Seeding teacher-subject assignments...")

        # Get all teachers and subjects
        teachers = db.query(Teacher).all()
        subjects = db.query(Subject).all()

        if not teachers or not subjects:
            print(
                "No teachers or subjects found. Please seed teachers and subjects first."
            )
            return

        # Subject name to code mapping for easy lookup
        subject_map = {subject.name: subject for subject in subjects}

        # Define realistic German school teacher-subject assignments
        assignments = [
            # Klassenlehrer (Class Teachers) - typically qualified for core subjects
            {
                "teacher_filter": {"first_name": "Maria", "last_name": "Schmidt"},
                "subjects": [
                    {
                        "name": "Deutsch",
                        "level": QualificationLevel.PRIMARY,
                        "grades": [1, 2],
                        "hours": 12,
                    },
                    {
                        "name": "Mathematik",
                        "level": QualificationLevel.PRIMARY,
                        "grades": [1, 2],
                        "hours": 8,
                    },
                    {
                        "name": "Sachunterricht",
                        "level": QualificationLevel.PRIMARY,
                        "grades": [1, 2],
                        "hours": 6,
                    },
                    {
                        "name": "Kunst",
                        "level": QualificationLevel.SECONDARY,
                        "grades": [1, 2, 3, 4],
                        "hours": 2,
                    },
                ],
            },
            {
                "teacher_filter": {"first_name": "Hans", "last_name": "Weber"},
                "subjects": [
                    {
                        "name": "Sport",
                        "level": QualificationLevel.PRIMARY,
                        "grades": [1, 2, 3, 4],
                        "hours": 10,
                        "cert_date": date(2020, 9, 1),
                        "cert_expires": date(2025, 8, 31),
                        "cert_doc": "Sport Teaching Certificate",
                    },
                    {
                        "name": "Deutsch",
                        "level": QualificationLevel.SECONDARY,
                        "grades": [3, 4],
                        "hours": 4,
                    },
                ],
            },
            {
                "teacher_filter": {"first_name": "Anna", "last_name": "Meyer"},
                "subjects": [
                    {
                        "name": "Deutsch",
                        "level": QualificationLevel.PRIMARY,
                        "grades": [3, 4],
                        "hours": 12,
                    },
                    {
                        "name": "Englisch",
                        "level": QualificationLevel.PRIMARY,
                        "grades": [3, 4],
                        "hours": 6,
                    },
                    {
                        "name": "Kunst",
                        "level": QualificationLevel.SECONDARY,
                        "grades": [1, 2, 3, 4],
                        "hours": 4,
                    },
                ],
            },
            {
                "teacher_filter": {"first_name": "Peter", "last_name": "Müller"},
                "subjects": [
                    {
                        "name": "Mathematik",
                        "level": QualificationLevel.PRIMARY,
                        "grades": [3, 4],
                        "hours": 10,
                    },
                    {
                        "name": "Sachunterricht",
                        "level": QualificationLevel.PRIMARY,
                        "grades": [3, 4],
                        "hours": 8,
                    },
                    {
                        "name": "Deutsch",
                        "level": QualificationLevel.SUBSTITUTE,
                        "grades": [1, 2, 3, 4],
                        "hours": 0,
                    },
                ],
            },
            {
                "teacher_filter": {"first_name": "Julia", "last_name": "Becker"},
                "subjects": [
                    {
                        "name": "Musik",
                        "level": QualificationLevel.PRIMARY,
                        "grades": [1, 2, 3, 4],
                        "hours": 8,
                        "cert_date": date(2019, 8, 15),
                        "cert_doc": "Music Education Certificate",
                    },
                    {
                        "name": "Deutsch",
                        "level": QualificationLevel.SECONDARY,
                        "grades": [1, 2],
                        "hours": 4,
                    },
                ],
            },
            {
                "teacher_filter": {"first_name": "Thomas", "last_name": "Wagner"},
                "subjects": [
                    {
                        "name": "Religion",
                        "level": QualificationLevel.PRIMARY,
                        "grades": [1, 2, 3, 4],
                        "hours": 6,
                        "cert_date": date(2018, 6, 1),
                        "cert_expires": date(2028, 5, 31),
                        "cert_doc": "Religious Education Certificate",
                    },
                    {
                        "name": "Ethik",
                        "level": QualificationLevel.SECONDARY,
                        "grades": [1, 2, 3, 4],
                        "hours": 2,
                    },
                ],
            },
            # Additional Fachlehrer (Subject Teachers)
            {
                "teacher_filter": {"first_name": "Laura", "last_name": "Schmidt"},
                "subjects": [
                    {
                        "name": "Englisch",
                        "level": QualificationLevel.PRIMARY,
                        "grades": [1, 2],
                        "hours": 8,
                    },
                    {
                        "name": "Deutsch",
                        "level": QualificationLevel.SECONDARY,
                        "grades": [1, 2, 3, 4],
                        "hours": 6,
                    },
                ],
            },
            {
                "teacher_filter": {"first_name": "Max", "last_name": "Fischer"},
                "subjects": [
                    {
                        "name": "Mathematik",
                        "level": QualificationLevel.SECONDARY,
                        "grades": [1, 2],
                        "hours": 6,
                    },
                    {
                        "name": "Sachunterricht",
                        "level": QualificationLevel.SECONDARY,
                        "grades": [1, 2, 3, 4],
                        "hours": 8,
                    },
                    {
                        "name": "Sport",
                        "level": QualificationLevel.SUBSTITUTE,
                        "grades": [1, 2, 3, 4],
                        "hours": 0,
                    },
                ],
            },
            {
                "teacher_filter": {"first_name": "Sophie", "last_name": "Klein"},
                "subjects": [
                    {
                        "name": "Kunst",
                        "level": QualificationLevel.PRIMARY,
                        "grades": [1, 2, 3, 4],
                        "hours": 8,
                    },
                    {
                        "name": "Werken",
                        "level": QualificationLevel.PRIMARY,
                        "grades": [3, 4],
                        "hours": 4,
                    },
                    {
                        "name": "Musik",
                        "level": QualificationLevel.SUBSTITUTE,
                        "grades": [1, 2, 3, 4],
                        "hours": 0,
                    },
                ],
            },
        ]

        # Create assignments
        created_count = 0
        for assignment_group in assignments:
            # Find the teacher
            teacher_filter = assignment_group["teacher_filter"]
            teacher = (
                db.query(Teacher)
                .filter(
                    Teacher.first_name == teacher_filter["first_name"],
                    Teacher.last_name == teacher_filter["last_name"],
                )
                .first()
            )

            if not teacher:
                print(
                    f"Teacher {teacher_filter['first_name']} {teacher_filter['last_name']} not found, skipping"
                )
                continue

            for subject_data in assignment_group["subjects"]:
                subject_name = subject_data["name"]
                if subject_name not in subject_map:
                    print(f"Subject '{subject_name}' not found, skipping")
                    continue

                subject = subject_map[subject_name]

                # Check if assignment already exists
                existing = (
                    db.query(TeacherSubject)
                    .filter(
                        TeacherSubject.teacher_id == teacher.id,
                        TeacherSubject.subject_id == subject.id,
                    )
                    .first()
                )

                if existing:
                    continue

                # Create the assignment
                assignment = TeacherSubject(
                    teacher_id=teacher.id,
                    subject_id=subject.id,
                    qualification_level=subject_data["level"],
                    grades=subject_data["grades"],
                    max_hours_per_week=subject_data.get("hours"),
                    certification_date=subject_data.get("cert_date"),
                    certification_expires=subject_data.get("cert_expires"),
                    certification_document=subject_data.get("cert_doc"),
                    created_at=datetime.now(UTC),
                    updated_at=datetime.now(UTC),
                )

                db.add(assignment)
                created_count += 1

        db.commit()
        print(f"Created {created_count} teacher-subject assignments")

    @staticmethod
    def clear(db: Session) -> None:
        """Clear all teacher-subject assignments."""
        print("Clearing teacher-subject assignments...")
        db.query(TeacherSubject).delete()
        db.commit()
        print("Teacher-subject assignments cleared")

    @staticmethod
    def get_stats(db: Session) -> dict:
        """Get statistics about teacher-subject assignments."""
        total = db.query(TeacherSubject).count()
        primary = (
            db.query(TeacherSubject)
            .filter(TeacherSubject.qualification_level == QualificationLevel.PRIMARY)
            .count()
        )
        secondary = (
            db.query(TeacherSubject)
            .filter(TeacherSubject.qualification_level == QualificationLevel.SECONDARY)
            .count()
        )
        substitute = (
            db.query(TeacherSubject)
            .filter(TeacherSubject.qualification_level == QualificationLevel.SUBSTITUTE)
            .count()
        )
        with_certification = (
            db.query(TeacherSubject)
            .filter(TeacherSubject.certification_date.isnot(None))
            .count()
        )

        return {
            "total_assignments": total,
            "primary_qualifications": primary,
            "secondary_qualifications": secondary,
            "substitute_qualifications": substitute,
            "with_certification": with_certification,
        }
