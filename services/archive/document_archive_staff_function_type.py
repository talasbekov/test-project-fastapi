import uuid

from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import ArchiveDocumentFunctionType, DocumentFunctionType
from schemas import DocumentArchiveStaffFunctionTypeCreate, DocumentArchiveStaffFunctionTypeUpdate

from services.base import ServiceBase


class DocumentArchiveStaffFunctionType(ServiceBase[ArchiveDocumentFunctionType, DocumentArchiveStaffFunctionTypeCreate, DocumentArchiveStaffFunctionTypeUpdate]):

    def get_by_id(self, db: Session, id: str) -> ArchiveDocumentFunctionType:
        type = super().get(db, id)
        if type is None:
            raise NotFoundException(detail="StaffUnit is not found!")
        return type
    
    def get_by_origin_id(self, db: Session, origin_id: uuid.UUID) -> ArchiveDocumentFunctionType:
        return db.query(self.model).filter(
            self.model.origin_id == origin_id
            ).first()
    
    def create_archive_staff_function_type(self, db: Session, staff_function_type: DocumentFunctionType):
        return super().create(db, DocumentArchiveStaffFunctionTypeCreate(
                name=staff_function_type.name,
                origin_id=staff_function_type.id
            )
        )

document_archive_staff_function_type_service = DocumentArchiveStaffFunctionType(ArchiveDocumentFunctionType)
