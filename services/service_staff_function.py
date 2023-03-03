import uuid

from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import ServiceStaffFunction, User
from schemas import (ServiceStaffFunctionCreate, ServiceStaffFunctionRead,
                     ServiceStaffFunctionUpdate)

from .base import ServiceBase


class ServiceStaffFunctionService(ServiceBase[ServiceStaffFunction, ServiceStaffFunctionCreate, ServiceStaffFunctionUpdate]):

    def get_by_id(self, db: Session, id: str):
        service_staff_function = super().get(db, id)
        if service_staff_function is None:
            raise NotFoundException(detail=f"ServiceStaffFunction with id: {id} is not found!")
        return service_staff_function

    def get_by_user(self, db: Session, user: User):
        l = []

        for func in user.actual_staff_unit.staff_functions:

            if func.discriminator == self.model.__mapper_args__['polymorphic_identity']:
                l.append(func)

        return l

    def duplicate(self, db: Session, id: uuid.UUID):
        func = self.get_by_id(db, id)
        copy = super().create(db, ServiceStaffFunctionCreate(
            name=func.name,
            hours_per_week=func.name,
            type_id=func.type_id
        ))

        return copy


service_staff_function_service = ServiceStaffFunctionService(ServiceStaffFunction)
