from sqlalchemy.orm import Session

from .base import ServiceBase

from models import DocumentFunctionType
from schemas import DocumentStaffFunctionTypeRead, DocumentStaffFunctionTypeUpdate, DocumentStaffFunctionTypeCreate
from exceptions.client import NotFoundException


class DocumentStaffFunctionTypeService(ServiceBase[DocumentFunctionType, DocumentStaffFunctionTypeCreate, DocumentStaffFunctionTypeUpdate]):

    def get_by_id(self, db: Session, id: str):
        document_staff_function_type = super().get(db, id)
        if document_staff_function_type is None:
            raise NotFoundException(detail=f"DocumentFunctionType with id: {id} is not found!")
        return document_staff_function_type


document_staff_function_type_service = DocumentStaffFunctionTypeService(DocumentFunctionType)