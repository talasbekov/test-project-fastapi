from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import ServiceFunctionType
from schemas import (ServiceFunctionRead, ServiceFunctionTypeCreate,
                     ServiceFunctionTypeUpdate)

from .base import ServiceBase


class ServiceFunctionTypeService(ServiceBase[ServiceFunctionType, ServiceFunctionTypeCreate, ServiceFunctionTypeUpdate]):

    def get_by_id(self, db: Session, id: str):
        service_function_type = super().get(db, id)
        if service_function_type is None:
            raise NotFoundException(detail=f"ServiceFunctionType with id: {id} is not found!")
        return service_function_type


service_function_type_service = ServiceFunctionTypeService(ServiceFunctionType)
