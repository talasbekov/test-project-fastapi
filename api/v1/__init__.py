from fastapi import APIRouter

from .hr_document import router as hr_document_router
from .role import router as role_router
from .group import router as group_router
from .hr_document_info import router as hr_document_info_router
from .hr_document_step import router as hr_document_step_router
from .hr_document_template import router as hr_document_template_router
from .user_stat import router as user_stat_router
from .position import router as position_router
from .permission import router as permission_router
from .user import router as user_router
from .auth import router as auth_router
from .equipment import router as equipment_router
from .badge import router as badge_router
from .rank import router as rank_router

router = APIRouter(prefix="/v1")

router.include_router(auth_router)
router.include_router(user_router)
router.include_router(hr_document_router)
router.include_router(role_router)
router.include_router(group_router)
router.include_router(hr_document_info_router)
router.include_router(hr_document_step_router)
router.include_router(hr_document_template_router)
router.include_router(user_stat_router)
router.include_router(position_router)
router.include_router(permission_router)
router.include_router(equipment_router)
router.include_router(badge_router)
router.include_router(rank_router)
