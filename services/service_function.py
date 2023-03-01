from sqlalchemy.orm import Session

from models import ServiceFunction
from schemas import ServiceFunctionCreate, ServiceFunctionUpdate, ServiceFunctionTypeRead
from exceptions.client import NotFoundException

from .base import ServiceBase


class ServiceFunctionService(ServiceBase[ServiceFunction, ServiceFunctionCreate, ServiceFunctionUpdate]):

    def get_by_id(self, db: Session, id: str):
        service_function = super().get(db, id)
        if service_function is None:
            raise NotFoundException(detail=f"ServiceFunction with id: {id} is not found!")
        return service_function


service_function_service = ServiceFunctionService(ServiceFunction)
