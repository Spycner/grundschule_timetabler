"""API v1 main router."""

from fastapi import APIRouter

from src.api.v1.routes import (
    classes,
    health,
    schedule,
    subjects,
    teacher_availability,
    teacher_subjects,
    teachers,
    timeslots,
)

router = APIRouter()

# Include health routes
router.include_router(health.router, prefix="", tags=["health"])

# Include teachers routes
router.include_router(teachers.router, prefix="/teachers", tags=["teachers"])

# Include teacher availability routes (must be after teachers to avoid conflicts)
router.include_router(
    teacher_availability.router, prefix="/teachers", tags=["teacher-availability"]
)

# Include teacher-subject routes
router.include_router(
    teacher_subjects.router, prefix="/teachers", tags=["teacher-subjects"]
)
router.include_router(
    teacher_subjects.subjects_router, prefix="/subjects", tags=["teacher-subjects"]
)
router.include_router(
    teacher_subjects.matrix_router,
    prefix="/teacher-subjects",
    tags=["teacher-subjects"],
)

# Include classes routes
router.include_router(classes.router, prefix="/classes", tags=["classes"])

# Include subjects routes
router.include_router(subjects.router, prefix="/subjects", tags=["subjects"])

# Include timeslots routes
router.include_router(timeslots.router, prefix="/timeslots", tags=["timeslots"])

# Include schedule routes
router.include_router(schedule.router, prefix="/schedule", tags=["schedule"])
