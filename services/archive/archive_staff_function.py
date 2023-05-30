import uuid

from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import ArchiveStaffFunction, StaffFunction
from schemas import ArchiveStaffFunctionCreate, ArchiveStaffFunctionUpdate, NewArchiveStaffFunctionCreate, \
    NewArchiveStaffFunctionUpdate

from services.base import ServiceBase

from .service_archive_staff_function_type import service_archive_staff_function_type_service


class ArchiveStaffFunctionService(ServiceBase[ArchiveStaffFunction, ArchiveStaffFunctionCreate, ArchiveStaffFunctionUpdate]):

    def get_all_staff_functions(self, db: Session, skip: int, limit: int):
        staff_functions = (
            db.query(ArchiveStaffFunction)
            .filter(ArchiveStaffFunction.discriminator != ''
                    )
            .offset(skip)
            .limit(limit)
            .all()
        )
        return staff_functions

    def get_by_id(self, db: Session, id: str):
        service_staff_function = super().get(db, id)
        if service_staff_function is None:
            raise NotFoundException(detail=f"ArchiveStaffFunction with id: {id} is not found!")
        return service_staff_function

    def exists_by_origin_id(self, db: Session, origin_id: uuid.UUID):
        return db.query(self.model).filter(
            self.model.origin_id == origin_id
            ).first() is not None

    def create_based_on_existing_staff_function(self, db: Session, staff_function: StaffFunction):
        return super().create(db, ArchiveStaffFunctionCreate(
            name=staff_function.name,
            hours_per_week=staff_function.hours_per_week,
            origin_id=staff_function.id
        ))

    def create_staff_function(self, db: Session, body: NewArchiveStaffFunctionCreate):
        return super().create(db, ArchiveStaffFunctionCreate(
            name=body.name,
            hours_per_week=body.hours_per_week,
            origin_id=None
        ))

    def update_staff_function(self, db: Session, staff_function: ArchiveStaffFunction, body: NewArchiveStaffFunctionUpdate):
        return super().update(db, db_obj=staff_function, obj_in=ArchiveStaffFunctionUpdate(
            name=body.name,
            hours_per_week=body.hours_per_week,
            origin_id=None
        ))


archive_staff_function_service = ArchiveStaffFunctionService(ArchiveStaffFunction)
