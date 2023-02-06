from fastapi import APIRouter

from core import configs
from .hr_document import router as hr_document_router

router = APIRouter(prefix="/v1")

router.include_router(hr_document_router)
