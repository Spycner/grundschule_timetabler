"""API v1 main router."""

from fastapi import APIRouter

from src.api.v1.routes import classes, health, subjects, teachers

router = APIRouter()

# Include health routes
router.include_router(health.router, prefix="", tags=["health"])

# Include teachers routes
router.include_router(teachers.router, prefix="/teachers", tags=["teachers"])

# Include classes routes
router.include_router(classes.router, prefix="/classes", tags=["classes"])

# Include subjects routes
router.include_router(subjects.router, prefix="/subjects", tags=["subjects"])
