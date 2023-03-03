from sqlalchemy.orm import Session

from .base import ServiceBase

from models import ServiceFunctionType
from schemas import ServiceStaffFunctionTypeCreate, ServiceStaffFunctionTypeUpdate, ServiceStaffFunctionTypeRead
from exceptions.client import NotFoundException


class ServiceFunctionTypeService(ServiceBase[ServiceFunctionType, ServiceStaffFunctionTypeCreate, ServiceStaffFunctionTypeUpdate]):

    def get_by_id(self, db: Session, id: str):
        service_function_type = super().get(db, id)
        if service_function_type is None:
            raise NotFoundException(detail=f"ServiceFunctionType with id: {id} is not found!")
        return service_function_type


service_staff_function_type_service = ServiceFunctionTypeService(ServiceFunctionType)