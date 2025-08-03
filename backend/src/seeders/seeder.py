"""Main database seeder for development data."""

import logging
from typing import Any

from sqlalchemy.orm import Session

from src.models.class_ import Class
from src.models.schedule import Schedule
from src.models.subject import Subject
from src.models.teacher import Teacher
from src.models.teacher_subject import TeacherSubject
from src.models.timeslot import TimeSlot
from src.seeders.schedule import seed_schedule
from src.seeders.teacher_subject_seeder import TeacherSubjectSeeder
from src.seeders.timeslot_seeder import seed_timeslots

logger = logging.getLogger(__name__)


class DatabaseSeeder:
    """Handles seeding of development data into the database."""

    def __init__(self, db: Session):
        """Initialize the seeder with a database session."""
        self.db = db

    def seed_all(self) -> dict[str, Any]:
        """Seed all data and return statistics."""
        stats = {
            "teachers": 0,
            "classes": 0,
            "subjects": 0,
            "teacher_subjects": 0,
            "timeslots": 0,
            "schedules": 0,
        }

        try:
            # Seed teachers
            teachers = self.seed_teachers()
            stats["teachers"] = len(teachers)
            logger.info(f"Seeded {len(teachers)} teachers")

            # Seed classes
            classes = self.seed_classes()
            stats["classes"] = len(classes)
            logger.info(f"Seeded {len(classes)} classes")

            # Seed subjects
            subjects = self.seed_subjects()
            stats["subjects"] = len(subjects)
            logger.info(f"Seeded {len(subjects)} subjects")

            # Seed teacher-subject assignments
            TeacherSubjectSeeder.seed(self.db)
            stats["teacher_subjects"] = self.db.query(TeacherSubject).count()
            logger.info(
                f"Seeded {stats['teacher_subjects']} teacher-subject assignments"
            )

            # Seed timeslots
            seed_timeslots(self.db)
            stats["timeslots"] = self.db.query(TimeSlot).count()
            logger.info(f"Seeded {stats['timeslots']} timeslots")

            # Seed schedule entries
            schedule_count = seed_schedule(self.db)
            stats["schedules"] = schedule_count
            logger.info(f"Seeded {schedule_count} schedule entries")

            self.db.commit()
            logger.info("Database seeding completed successfully")
            return stats

        except Exception as e:
            self.db.rollback()
            logger.error(f"Error during seeding: {e}")
            raise

    def seed_teachers(self) -> list[Teacher]:
        """Seed sample teachers."""
        teachers_data = [
            {
                "first_name": "Maria",
                "last_name": "Schmidt",
                "email": "maria.schmidt@schule.de",
                "abbreviation": "SCH",
                "max_hours_per_week": 28,
                "is_part_time": False,
            },
            {
                "first_name": "Hans",
                "last_name": "Weber",
                "email": "hans.weber@schule.de",
                "abbreviation": "WEB",
                "max_hours_per_week": 28,
                "is_part_time": False,
            },
            {
                "first_name": "Anna",
                "last_name": "Meyer",
                "email": "anna.meyer@schule.de",
                "abbreviation": "MEY",
                "max_hours_per_week": 28,
                "is_part_time": False,
            },
            {
                "first_name": "Peter",
                "last_name": "Müller",
                "email": "peter.mueller@schule.de",
                "abbreviation": "MUL",
                "max_hours_per_week": 28,
                "is_part_time": False,
            },
            {
                "first_name": "Julia",
                "last_name": "Becker",
                "email": "julia.becker@schule.de",
                "abbreviation": "BEC",
                "max_hours_per_week": 28,
                "is_part_time": False,
            },
            {
                "first_name": "Thomas",
                "last_name": "Wagner",
                "email": "thomas.wagner@schule.de",
                "abbreviation": "WAG",
                "max_hours_per_week": 28,
                "is_part_time": False,
            },
            {
                "first_name": "Laura",
                "last_name": "Schmidt",
                "email": "laura.schmidt@schule.de",
                "abbreviation": "LSC",
                "max_hours_per_week": 28,
                "is_part_time": False,
            },
            {
                "first_name": "Max",
                "last_name": "Fischer",
                "email": "max.fischer@schule.de",
                "abbreviation": "FIS",
                "max_hours_per_week": 28,
                "is_part_time": False,
            },
            {
                "first_name": "Sophie",
                "last_name": "Klein",
                "email": "sophie.klein@schule.de",
                "abbreviation": "KLE",
                "max_hours_per_week": 28,
                "is_part_time": False,
            },
        ]

        teachers = []
        for data in teachers_data:
            # Check if teacher already exists
            existing = self.db.query(Teacher).filter_by(email=data["email"]).first()
            if not existing:
                teacher = Teacher(**data)
                self.db.add(teacher)
                teachers.append(teacher)
            else:
                teachers.append(existing)

        self.db.flush()  # Get IDs without committing
        return teachers

    def seed_classes(self) -> list[Class]:
        """Seed sample classes."""
        classes_data = [
            # Grade 1
            {
                "name": "1a",
                "grade": 1,
                "size": 22,
                "home_room": "Raum 101",
            },
            {
                "name": "1b",
                "grade": 1,
                "size": 21,
                "home_room": "Raum 102",
            },
            # Grade 2
            {
                "name": "2a",
                "grade": 2,
                "size": 24,
                "home_room": "Raum 201",
            },
            {
                "name": "2b",
                "grade": 2,
                "size": 23,
                "home_room": "Raum 202",
            },
            # Grade 3
            {
                "name": "3a",
                "grade": 3,
                "size": 25,
                "home_room": "Raum 301",
            },
            {
                "name": "3b",
                "grade": 3,
                "size": 24,
                "home_room": "Raum 302",
            },
            # Grade 4
            {
                "name": "4a",
                "grade": 4,
                "size": 26,
                "home_room": "Raum 401",
            },
            {
                "name": "4b",
                "grade": 4,
                "size": 25,
                "home_room": "Raum 402",
            },
        ]

        classes = []
        for data in classes_data:
            # Check if class already exists
            existing = self.db.query(Class).filter_by(name=data["name"]).first()
            if not existing:
                class_ = Class(**data)
                self.db.add(class_)
                classes.append(class_)
            else:
                classes.append(existing)

        self.db.flush()  # Get IDs without committing
        return classes

    def seed_subjects(self) -> list[Subject]:
        """Seed sample subjects common in German Grundschule."""
        subjects_data = [
            {
                "name": "Deutsch",
                "code": "DE",
                "color": "#DC2626",  # Red
            },
            {
                "name": "Mathematik",
                "code": "MA",
                "color": "#2563EB",  # Blue
            },
            {
                "name": "Sachunterricht",
                "code": "SU",
                "color": "#7C3AED",  # Purple
            },
            {
                "name": "Englisch",
                "code": "EN",
                "color": "#059669",  # Emerald
            },
            {
                "name": "Sport",
                "code": "SP",
                "color": "#16A34A",  # Green
            },
            {
                "name": "Musik",
                "code": "MU",
                "color": "#F59E0B",  # Amber
            },
            {
                "name": "Kunst",
                "code": "KU",
                "color": "#EC4899",  # Pink
            },
            {
                "name": "Religion",
                "code": "REL",
                "color": "#8B5CF6",  # Violet
            },
            {
                "name": "Ethik",
                "code": "ETH",
                "color": "#06B6D4",  # Cyan
            },
            {
                "name": "Werken",
                "code": "WE",
                "color": "#A16207",  # Yellow-700
            },
        ]

        subjects = []
        for data in subjects_data:
            # Check if subject already exists
            existing = self.db.query(Subject).filter_by(name=data["name"]).first()
            if not existing:
                subject = Subject(**data)
                self.db.add(subject)
                subjects.append(subject)
            else:
                subjects.append(existing)

        self.db.flush()  # Get IDs without committing
        return subjects

    def clear_all(self) -> dict[str, int]:
        """Clear all seeded data (use with caution)."""
        stats = {
            "teachers": 0,
            "classes": 0,
            "subjects": 0,
            "teacher_subjects": 0,
            "timeslots": 0,
            "schedules": 0,
        }

        try:
            # Clear in reverse order of dependencies
            # Clear schedules first (depends on everything)
            stats["schedules"] = self.db.query(Schedule).delete()

            # Clear timeslots
            stats["timeslots"] = self.db.query(TimeSlot).delete()

            # Clear teacher-subject assignments
            stats["teacher_subjects"] = self.db.query(TeacherSubject).delete()

            # Clear subjects
            stats["subjects"] = self.db.query(Subject).delete()

            # Clear classes
            stats["classes"] = self.db.query(Class).delete()

            # Clear teachers
            stats["teachers"] = self.db.query(Teacher).delete()

            self.db.commit()
            logger.info("Database cleared successfully")
            return stats

        except Exception as e:
            self.db.rollback()
            logger.error(f"Error during clearing: {e}")
            raise
