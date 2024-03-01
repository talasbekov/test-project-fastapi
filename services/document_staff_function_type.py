from sqlalchemy.orm import Session
from typing import List

from exceptions.client import NotFoundException
from models import DocumentFunctionType, DocumentFunctionTypeEnum
from schemas import DocumentStaffFunctionTypeUpdate, DocumentStaffFunctionTypeCreate
from .base import ServiceBase


class DocumentStaffFunctionTypeService(
        ServiceBase[DocumentFunctionType,
                     DocumentStaffFunctionTypeCreate,
                     DocumentStaffFunctionTypeUpdate]):
    def get_multi(
        self, db: Session, skip: int = 0, limit: int = 100
    ) -> List[DocumentFunctionType]:
        return db.query(self.model).order_by(self.model.show_order).offset(skip).limit(limit).all()
    
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
                detail=("DocumentFunctionType with name:"
                        f" {DocumentFunctionTypeEnum.INITIATOR.value} is not found!"))
        return res


document_staff_function_type_service = DocumentStaffFunctionTypeService(
    DocumentFunctionType)
