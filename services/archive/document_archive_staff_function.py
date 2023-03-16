import uuid

from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import ArchiveDocumentStaffFunction, User, StaffFunction
from schemas import ArchiveDocumentStaffFunctionCreate, ArchiveDocumentStaffFunctionUpdate

from services.base import ServiceBase


class DocumentArchiveStaffFunction(ServiceBase[ArchiveDocumentStaffFunction, ArchiveDocumentStaffFunctionCreate, ArchiveDocumentStaffFunctionUpdate]):
    
    def get_by_id(self, db: Session, id: str):
        document_staff_function = super().get(db, id)
        if document_staff_function is None:
            raise NotFoundException(detail=f"DocumentArchiveStaffFunction with id: {id} is not found!")
        return document_staff_function
    
    def create_archive_staff_function(self, db: Session, staff_function: StaffFunction, staff_list_id: uuid.UUID):
        return super().create(db, ArchiveDocumentStaffFunctionCreate(
            name=staff_function.name,
            hours_per_week=staff_function.hours_per_week,
            role_id=staff_function.role_id,
            staff_list_id=staff_list_id,
            jurisdiction_id=staff_function.jurisdiction_id,
            priority=staff_function.priority,
            origin_id=staff_function.id
        ))


document_archive_staff_function_service = DocumentArchiveStaffFunction(ArchiveDocumentStaffFunction)
