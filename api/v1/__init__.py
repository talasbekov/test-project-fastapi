from fastapi import APIRouter

from core import configs

from .hr_document import router as hr_document_router
from .role import router as role_router
from .group import router as group_router
from .hr_document_info import router as hr_document_info_router
from .hr_document_step import router as hr_document_step_router
from .hr_document_template import router as hr_document_template_router

router = APIRouter(prefix="/v1")

router.include_router(hr_document_router)
router.include_router(role_router)
router.include_router(group_router)
router.include_router(hr_document_info_router)
router.include_router(hr_document_step_router)
router.include_router(hr_document_template_router)
