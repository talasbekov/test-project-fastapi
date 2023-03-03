from typing import List

from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import DocumentStaffFunction, StaffUnit, User
from schemas import (DocumentStaffFunctionCreate, DocumentStaffFunctionRead,
                     DocumentStaffFunctionUpdate)

from .base import ServiceBase


class DocumentStaffFunctionService(ServiceBase[DocumentStaffFunction, DocumentStaffFunctionCreate, DocumentStaffFunctionUpdate]):

    def get_by_id(self, db: Session, id: str) -> DocumentStaffFunction:
        service_staff_function = super().get(db, id)
        if service_staff_function is None:
            raise NotFoundException(detail=f"DocumentStaffFunction with id: {id} is not found!")
        return service_staff_function

    def get_by_user(self, db: Session, user: User) -> List[DocumentStaffFunction]:
        l = []

        for func in user.actual_staff_unit.staff_functions:

            if func.discriminator == self.model.__mapper_args__['polymorphic_identity']:
                l.append(func)

        return l


document_staff_function_service = DocumentStaffFunctionService(DocumentStaffFunction)
