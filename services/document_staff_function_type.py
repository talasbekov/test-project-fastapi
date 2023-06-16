from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import DocumentFunctionType, DocumentFunctionTypeEnum
from schemas import DocumentStaffFunctionTypeUpdate, DocumentStaffFunctionTypeCreate
from .base import ServiceBase


class DocumentStaffFunctionTypeService(
        ServiceBase[DocumentFunctionType, DocumentStaffFunctionTypeCreate, DocumentStaffFunctionTypeUpdate]):
    def get_by_id(self, db: Session, id: str) -> DocumentFunctionType:
        document_staff_function_type = super().get(db, id)
        if document_staff_function_type is None:
            raise NotFoundException(
                detail=f"DocumentFunctionType with id: {id} is not found!")
        return document_staff_function_type

    def get_initiator(self, db: Session) -> DocumentFunctionType:
        res = db.query(
            self.model).filter(
            self.model.name == DocumentFunctionTypeEnum.INITIATOR.value).first()
        if not res:
            raise NotFoundException(
                detail=f"DocumentFunctionType with name: {DocumentFunctionTypeEnum.INITIATOR.value} is not found!")
        return res


document_staff_function_type_service = DocumentStaffFunctionTypeService(
    DocumentFunctionType)
