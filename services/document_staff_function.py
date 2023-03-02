from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import DocumentStaffFunction
from schemas import (DocumentStaffFunctionRead, DocumentStaffFunctionCreate,
                     DocumentStaffFunctionUpdate)

from .base import ServiceBase


class DocumentStaffFunctionService(ServiceBase[DocumentStaffFunction, DocumentStaffFunctionCreate, DocumentStaffFunctionUpdate]):

    def get_by_id(self, db: Session, id: str):
        service_staff_function = super().get(db, id)
        if service_staff_function is None:
            raise NotFoundException(detail=f"DocumentStaffFunction with id: {id} is not found!")
        return service_staff_function


document_staff_function_service = DocumentStaffFunctionService(DocumentStaffFunction)