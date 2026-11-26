"""Profile management API endpoints."""

from fastapi import APIRouter

from app.schemas.profile import StudentProfile
from app.storage import store

router = APIRouter(prefix="/api/profile", tags=["profile"])


@router.get("", response_model=StudentProfile)
def get_profile() -> StudentProfile:
    """Returns the active student profile."""
    return store.profile


@router.post("", response_model=StudentProfile)
def update_profile(profile: StudentProfile) -> StudentProfile:
    """Updates the active student profile."""
    store.profile = profile
    return store.profile
