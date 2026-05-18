from fastapi import APIRouter
from app.core.config import settings

router = APIRouter()

@router.get("/health")
def health_check():
    """System health check endpoint."""
    return {"status": "ok", "service": settings.PROJECT_NAME}

@router.get("/version")
def get_version():
    """Get API version info."""
    return {"version": settings.VERSION}
