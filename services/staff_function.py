from fastapi import HTTPException, status
from fastapi.logger import logger as log
from sqlalchemy.orm import Session

from exceptions import NotFoundException
from models import StaffFunction
from schemas import StaffFunctionCreate, StaffFunctionRead, StaffFunctionUpdate

from .base import ServiceBase


class StaffFunctionService(ServiceBase[StaffFunction, StaffFunctionCreate, StaffFunctionUpdate]):

    def get_by_id(self, db: Session, id: str):
        role = super().get(db, id)
        if role is None:
            raise NotFoundException(detail=f"StaffFunction with id: {id} is not found!")
        return role


staff_function_service = StaffFunctionService(StaffFunction)
