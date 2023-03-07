import datetime
import uuid
from typing import List

from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import DocumentStaffFunction, HrDocumentStep, User
from schemas import (DocumentStaffFunctionAdd, DocumentStaffFunctionCreate,
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
            jurisdiction_id=func.jurisdiction_id,
            priority=func.priority,
            role_id=func.role_id
        ))

        new_step = HrDocumentStep(
            hr_document_template_id=func.hr_document_step.hr_document_template_id,
            staff_function_id=res.id,
            created_at=datetime.datetime.now()
        )

        db.add(new_step)
        db.add(res)
        db.flush()

        return res

    def create_function(self, db: Session, body: DocumentStaffFunctionAdd):

        create_function: DocumentStaffFunction = super().create(db, DocumentStaffFunctionCreate(
            role_id=body.role_id,
            name=body.name,
            jurisdiction_id=body.jurisdiction_id,
            hours_per_week=body.hours_per_week,
            priority=body.priority
        ))
        new_step = HrDocumentStep(
            hr_document_template_id=body.hr_document_template_id,
            staff_function_id=create_function.id,
            created_at=datetime.datetime.now()
        )

        db.add(new_step)
        db.add(create_function)
        db.flush()
        return create_function


document_staff_function_service = DocumentStaffFunctionService(DocumentStaffFunction)
