from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import ServiceStaffFunction
from schemas import (ServiceFunctionCreate, ServiceFunctionTypeRead,
                     ServiceFunctionUpdate)

from .base import ServiceBase


class ServiceFunctionService(ServiceBase[ServiceStaffFunction, ServiceFunctionCreate, ServiceFunctionUpdate]):

    def get_by_id(self, db: Session, id: str):
        service_function = super().get(db, id)
        if service_function is None:
            raise NotFoundException(detail=f"ServiceFunction with id: {id} is not found!")
        return service_function


service_function_service = ServiceFunctionService(ServiceStaffFunction)
