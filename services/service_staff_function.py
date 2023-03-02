from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import ServiceStaffFunction
from schemas import (ServiceStaffFunctionCreate, ServiceStaffFunctionUpdate,
                     ServiceStaffFunctionRead)

from .base import ServiceBase


class ServiceStaffFunctionService(ServiceBase[ServiceStaffFunction, ServiceStaffFunctionCreate, ServiceStaffFunctionUpdate]):

    def get_by_id(self, db: Session, id: str):
        service_staff_function = super().get(db, id)
        if service_staff_function is None:
            raise NotFoundException(detail=f"ServiceStaffFunction with id: {id} is not found!")
        return service_staff_function


service_staff_function_service = ServiceStaffFunctionService(ServiceStaffFunction)