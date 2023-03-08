from fastapi import APIRouter

from .family import router as family_router
from .family_profile import router as family_profile_router

router = APIRouter(prefix="/family")

router.include_router(family_router)
router.include_router(family_profile_router)
