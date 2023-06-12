import uuid

from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import ArchiveDocumentFunctionType, DocumentFunctionType
from schemas import DocumentArchiveStaffFunctionTypeCreate, DocumentArchiveStaffFunctionTypeUpdate, \
    NewDocumentArchiveStaffFunctionTypeCreate

from services.base import ServiceBase


class DocumentArchiveStaffFunctionTypeService(ServiceBase[ArchiveDocumentFunctionType, DocumentArchiveStaffFunctionTypeCreate, DocumentArchiveStaffFunctionTypeUpdate]):

    def get_by_id(self, db: Session, id: str) -> ArchiveDocumentFunctionType:
        type = super().get(db, id)
        if type is None:
            raise NotFoundException(detail="DocumentArchiveStaffFunctionType is not found!")
        return type
    
    def get_by_origin_id(self, db: Session, origin_id: uuid.UUID) -> ArchiveDocumentFunctionType:
        return db.query(self.model).filter(
            self.model.origin_id == origin_id
            ).first()
    
    def create_based_on_existing_archive_staff_function_type(self, db: Session, staff_function_type: DocumentFunctionType):
        if staff_function_type is None:
            return None
        return super().create(db, DocumentArchiveStaffFunctionTypeCreate(
                name=staff_function_type.name,
                origin_id=staff_function_type.id,
                can_cancel=staff_function_type.can_cancel
            )
        )

    def create_staff_function_type(self, db: Session, body: NewDocumentArchiveStaffFunctionTypeCreate):
        return super().create(db, DocumentArchiveStaffFunctionTypeCreate(
                name=body.name,
                origin_id=None,
                can_cancel=body.can_cancel
            )
        )

    def create_staff_function_type(self, db: Session, type: ArchiveDocumentFunctionType, body: NewDocumentArchiveStaffFunctionTypeCreate):
        return super().update(db, db_obj=type, obj_in=DocumentArchiveStaffFunctionTypeCreate(
                name=body.name,
                origin_id=None,
                can_cancel=body.can_cancel
            )
        )


document_archive_staff_function_type_service = DocumentArchiveStaffFunctionTypeService(ArchiveDocumentFunctionType)
