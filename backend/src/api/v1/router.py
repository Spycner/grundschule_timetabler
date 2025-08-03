"""API v1 main router."""

from fastapi import APIRouter

from src.api.v1.routes import health, teachers

router = APIRouter()

# Include health routes
router.include_router(health.router, prefix="", tags=["health"])

# Include teachers routes
router.include_router(teachers.router, prefix="/teachers", tags=["teachers"])
