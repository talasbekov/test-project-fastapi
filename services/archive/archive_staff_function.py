import uuid

from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import ArchiveStaffFunction, User
from schemas import ArchiveStaffFunctionCreate, ArchiveStaffFunctionUpdate

from services.base import ServiceBase

from .service_archive_staff_function_type import service_archive_staff_function_type_service


class ArchiveStaffFunctionService(ServiceBase[ArchiveStaffFunction, ArchiveStaffFunctionCreate, ArchiveStaffFunctionUpdate]):

    def get_by_id(self, db: Session, id: str):
        service_staff_function = super().get(db, id)
        if service_staff_function is None:
            raise NotFoundException(detail=f"ArchiveStaffFunction with id: {id} is not found!")
        return service_staff_function

    def exists_by_origin_id(self, db: Session, origin_id: uuid.UUID):
        return db.query(self.model).filter(
            self.model.origin_id == origin_id
            ).first() is not None


archive_staff_function_service = ArchiveStaffFunctionService(ArchiveStaffFunction)
