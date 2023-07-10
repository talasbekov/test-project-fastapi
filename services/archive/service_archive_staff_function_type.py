import uuid

from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import ArchiveServiceFunctionType, ServiceFunctionType
from schemas import (
    ServiceArchiveStaffFunctionTypeCreate,
    ServiceArchiveStaffFunctionTypeUpdate,
    NewServiceArchiveStaffFunctionTypeCreate
)

from services.base import ServiceBase


class ServiceArchiveStaffFunctionTypeService(
        ServiceBase[ArchiveServiceFunctionType,
                    ServiceArchiveStaffFunctionTypeCreate,
                    ServiceArchiveStaffFunctionTypeUpdate]):

    def get_by_id(self, db: Session, id: str) -> ArchiveServiceFunctionType:
        type = super().get(db, id)
        if type is None:
            raise NotFoundException(
                detail="ServiceArchiveStaffFunctionType is not found!")
        return type

    def get_by_origin_id(self, db: Session,
                         origin_id: uuid.UUID) -> ArchiveServiceFunctionType:
        if origin_id is None:
            return None
        return db.query(self.model).filter(
            self.model.origin_id == origin_id
        ).first()

    def exists_by_origin_id(self, db: Session, origin_id: uuid.UUID) -> bool:
        return db.query(self.model).filter(
            self.model.origin_id == origin_id
        ).first() is not None

    def create_based_on_existing_archive_staff_function_type(
            self, db: Session, staff_function_type: ServiceFunctionType):
        if staff_function_type is None:
            return None
        return super().create(db, ServiceArchiveStaffFunctionTypeCreate(
            name=staff_function_type.name,
            nameKZ=staff_function_type.nameKZ,
            origin_id=staff_function_type.id
        )
        )

    def create_archive_staff_function_type(
            self, db: Session, body: NewServiceArchiveStaffFunctionTypeCreate):
        return super().create(db, ServiceArchiveStaffFunctionTypeCreate(
            name=body.name,
            nameKZ=body.nameKZ,
            origin_id=None
        )
        )

    def update_archive_staff_function_type(
            self,
            db: Session,
            type: ArchiveServiceFunctionType,
            body: NewServiceArchiveStaffFunctionTypeCreate):
        return super().update(db,
                              db_obj=type,
                              obj_in=ServiceArchiveStaffFunctionTypeCreate(
            name=body.name,
            nameKZ=body.nameKZ,
            origin_id=None
        )
        )


service_archive_staff_function_type_service = ServiceArchiveStaffFunctionTypeService(
    ArchiveServiceFunctionType)
