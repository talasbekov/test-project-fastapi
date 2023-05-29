from fastapi import APIRouter

from .family import router as families_router
from .family_relation import router as family_relation_router
from .family_profile import router as family_profile_router

family_router = APIRouter(prefix="/family")

family_router.include_router(families_router)
family_router.include_router(family_relation_router)
family_router.include_router(family_profile_router)
 