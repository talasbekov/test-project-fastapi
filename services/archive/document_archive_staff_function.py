import uuid

from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import ArchiveDocumentStaffFunction, DocumentStaffFunction, User
from schemas import (
    ArchiveDocumentStaffFunctionCreate,
    ArchiveDocumentStaffFunctionUpdate,
    DocumentArchiveStaffFunctionTypeCreate,
    DocumentArchiveStaffFunctionTypeUpdate,
)
from services import ServiceBase

from .document_archive_staff_function_type import (
    document_archive_staff_function_type_service,
)


class DocumentArchiveStaffFunction(ServiceBase[ArchiveDocumentStaffFunction, ArchiveDocumentStaffFunctionCreate, ArchiveDocumentStaffFunctionUpdate]):
    
    def get_by_id(self, db: Session, id: str):
        document_staff_function = super().get(db, id)
        if document_staff_function is None:
            raise NotFoundException(detail=f"DocumentArchiveStaffFunction with id: {id} is not found!")
        return document_staff_function
    
    def create_archive_staff_function(self, db: Session, staff_function: DocumentStaffFunction, role_id: uuid.UUID):
        return super().create(db, ArchiveDocumentStaffFunctionCreate(
            name=staff_function.name,
            hours_per_week=staff_function.hours_per_week,
            role_id=role_id,
            jurisdiction_id=staff_function.jurisdiction_id,
            priority=staff_function.priority,
            origin_id=staff_function.id
        ))


document_archive_staff_function_service = DocumentArchiveStaffFunction(ArchiveDocumentStaffFunction)
