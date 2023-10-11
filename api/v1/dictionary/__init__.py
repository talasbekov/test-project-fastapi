from fastapi import APIRouter

from .dictionary_operations import router as operations_router

router_education = APIRouter(prefix="/dictionary")

router_education.include_router(operations_router)
