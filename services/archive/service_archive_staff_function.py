import uuid

from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import ArchiveServiceStaffFunction, User, StaffFunction
from schemas import ArchiveServiceStaffFunctionCreate, ArchiveServiceStaffFunctionUpdate

from services.base import ServiceBase


class ArchiveServiceStaffFunctionService(ServiceBase[ArchiveServiceStaffFunction, ArchiveServiceStaffFunctionCreate, ArchiveServiceStaffFunctionUpdate]):

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
        copy = super().create(db, ArchiveServiceStaffFunctionCreate(
            name=func.name,
            hours_per_week=func.hours_per_week,
            type_id=func.type_id
        ))

        return copy
    
    def create_archive_staff_function(self, db: Session, staff_function: StaffFunction, staff_list_id: uuid.UUID):
        return super().create(db, ArchiveServiceStaffFunctionCreate(
            name=staff_function.name,
            hours_per_week=staff_function.hours_per_week,
            type_id=staff_function.type_id,
            origin_id=staff_function.id
        ))


service_archive_staff_function_service = ArchiveServiceStaffFunctionService(ArchiveServiceStaffFunction)
