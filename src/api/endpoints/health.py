"""Health check endpoints."""

from fastapi import APIRouter
from datetime import datetime

router = APIRouter()


@router.get("/health")
async def health_check():
    """Basic health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/health/ready")
async def readiness_check():
    """Readiness check for deployment."""
    # TODO: Add checks for model loading, service availability
    return {
        "status": "ready",
        "timestamp": datetime.utcnow().isoformat()
    }