import uuid

from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import ArchiveServiceFunctionType, ServiceFunctionType
from schemas import ServiceArchiveStaffFunctionTypeCreate, ServiceArchiveStaffFunctionTypeUpdate

from services.base import ServiceBase


class ServiceArchiveStaffFunctionTypeService(ServiceBase[ArchiveServiceFunctionType, ServiceArchiveStaffFunctionTypeCreate, ServiceArchiveStaffFunctionTypeUpdate]):

    def get_by_id(self, db: Session, id: str) -> ArchiveServiceFunctionType:
        type = super().get(db, id)
        if type is None:
            raise NotFoundException(detail="ServiceArchiveStaffFunctionType is not found!")
        return type

    def exists_by_origin_id(self, db: Session, origin_id: uuid.UUID) -> bool:
        return db.query(self.model).filter(
            self.model.origin_id == origin_id
            ).first() is not None
        
    def create_archive_staff_function_type(self, db: Session, staff_function_type: ServiceFunctionType):
        return super().create(db, ServiceArchiveStaffFunctionTypeCreate(
                name=staff_function_type.name,
                description=staff_function_type.description,
                origin_id=staff_function_type.id
            )
        )


service_archive_staff_function_type_service = ServiceArchiveStaffFunctionTypeService(ArchiveServiceFunctionType)
