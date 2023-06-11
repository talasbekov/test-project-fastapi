import uuid

from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import (ServiceStaffFunction, User, StaffUnit,
                    ArchiveServiceStaffFunction,)
from schemas import ServiceStaffFunctionCreate, ServiceStaffFunctionUpdate
from .base import ServiceBase


class ServiceStaffFunctionService(
        ServiceBase[ServiceStaffFunction, ServiceStaffFunctionCreate, ServiceStaffFunctionUpdate]):

    def get_by_id(self, db: Session, id: str):
        service_staff_function = super().get(db, id)
        if service_staff_function is None:
            raise NotFoundException(
                detail=f"ServiceStaffFunction with id: {id} is not found!")
        return service_staff_function

    def get_by_staff_unit(self, db: Session, staff_unit: StaffUnit):
        return db.query(
            self.model).filter(
            self.model.staff_units.contains(staff_unit)).all()

    def get_by_user(self, db: Session, user: User):
        l = []

        for func in user.actual_staff_unit.staff_functions:

            if func.discriminator == self.model.__mapper_args__[
                    'polymorphic_identity']:
                l.append(func)

        return l

    def duplicate(self, db: Session, id: uuid.UUID):
        func = self.get_by_id(db, id)
        copy = super().create(db, ServiceStaffFunctionCreate(
            name=func.name,
            nameKZ=func.nameKZ,
            hours_per_week=func.hours_per_week,
            type_id=func.type_id
        ))

        return copy

    def _update_from_archive(
            self,
            db,
            archive_staff_function: ArchiveServiceStaffFunction):
        service_staff_function = self.get_by_id(db, archive_staff_function.origin_id)

        res = super().update(
            db,
            db_obj=service_staff_function,
            obj_in=ServiceStaffFunctionUpdate(
                name=archive_staff_function.name,
                nameKZ=archive_staff_function.nameKZ,
                hours_per_week=archive_staff_function.hours_per_week,
                type_id=None,
            )
        )
        return res

    def _create_from_archive(
            self,
            db,
            archive_staff_function: ArchiveServiceStaffFunction):
        res = super().create(
            db, ServiceStaffFunctionCreate(
                name=archive_staff_function.name,
                nameKZ=archive_staff_function.nameKZ,
                hours_per_week=archive_staff_function.hours_per_week,
                type_id=None,
            )
        )
        return res

    def create_or_update_from_archive(
            self,
            db: Session,
            archive_service_staff_function: ArchiveServiceStaffFunction):
        if archive_service_staff_function.origin_id is None:
            return self._create_from_archive(db,
                                             archive_service_staff_function)
        return self._update_from_archive(db,
                                         archive_service_staff_function)


service_staff_function_service = ServiceStaffFunctionService(
    ServiceStaffFunction)
