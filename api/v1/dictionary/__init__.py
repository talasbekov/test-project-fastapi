from fastapi import APIRouter

from .dictionary_operations import router as operations_router

router_dictionary = APIRouter(prefix="/dictionary")

router_dictionary.include_router(operations_router)
