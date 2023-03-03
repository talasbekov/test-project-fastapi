import uuid
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

    def duplicate(self, db: Session, id: uuid.UUID):
        func = self.get_by_id(db, id)

        res = super().create(db, DocumentStaffFunctionCreate(
            name=func.name,
            hours_per_week=func.hours_per_week,
            priority=func.priority,
            role_id=func.role_id
        ))

        return res


document_staff_function_service = DocumentStaffFunctionService(DocumentStaffFunction)
