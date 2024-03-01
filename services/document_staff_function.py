import datetime
import uuid
from typing import List

from sqlalchemy.orm import Session

from exceptions.client import NotFoundException, BadRequestException
from models import DocumentStaffFunction, HrDocumentStep, User, StaffUnit
from schemas import (
    DocumentStaffFunctionAdd,
    DocumentStaffFunctionCreate,
    DocumentStaffFunctionUpdate,
    DocumentStaffFunctionConstructorAdd,
    DocumentStaffFunctionAppendToStaffUnit,
)
from .base import ServiceBase


class DocumentStaffFunctionService(
        ServiceBase[DocumentStaffFunction,
                    DocumentStaffFunctionCreate,
                    DocumentStaffFunctionUpdate]):

    def get_by_id(self, db: Session, id: str) -> DocumentStaffFunction:
        service_staff_function = super().get(db, id)
        if service_staff_function is None:
            raise NotFoundException(
                detail=f"DocumentStaffFunction with id: {id} is not found!")
        return service_staff_function

    def get_by_user(self, db: Session,
                    user: User) -> List[DocumentStaffFunction]:
        staff_functions = []

        for func in user.staff_unit.staff_functions:

            if func.discriminator == self.model.__mapper_args__[
                    'polymorphic_identity']:
                staff_functions.append(func)

        return staff_functions

    def duplicate(self, db: Session, id: str):
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
            staff_function_id=res.id
        )

        db.add(new_step)
        db.add(res)
        db.flush()

        return res

    def create_function(self, db: Session, body: DocumentStaffFunctionAdd):

        function: DocumentStaffFunction = super().create(
            db,
            DocumentStaffFunctionCreate(
                role_id=body.role_id,
                name=body.name,
                jurisdiction_id=body.jurisdiction_id,
                hours_per_week=body.hours_per_week,
                priority=body.priority,
                is_active=True
            )
        )

        new_step = HrDocumentStep(
            hr_document_template_id=body.hr_document_template_id,
            staff_function_id=function.id,
            created_at=datetime.datetime.now(),
            is_direct_supervisor=body.is_direct_supervisor,
            category=body.category,
        )

        db.add(function)
        db.add(new_step)
        db.flush()
        return function

    def create_function_for_constructor(
            self, db: Session, body: DocumentStaffFunctionConstructorAdd):
        res = self.create_function(db, DocumentStaffFunctionAdd(**body.dict()))
        staff_unit = db.query(StaffUnit).filter(
            StaffUnit.id == body.staff_unit_id).first()
        if staff_unit is None:
            raise NotFoundException(
                detail=f"StaffUnit with id: {body.staff_unit_id} is not found!")

        for staff_function in staff_unit.staff_functions:
            if staff_function.discriminator != self.model.__mapper_args__[
                    'polymorphic_identity']:
                continue
            if staff_function.hr_document_step is None:
                continue
            if (body.hr_document_template_id
                == staff_function.hr_document_step.hr_document_template_id):

                raise BadRequestException(
                    detail=("StaffFunction with template id:"
                            f" {body.hr_document_template_id} already exists!")
                )

        staff_unit.staff_functions.append(res)
        db.add(staff_unit)
        db.flush()
        return res

    def get_staff_units_by_id(self, db: Session, id: str):
        staff_function = self.get_by_id(db, id)
        return [i.id for i in staff_function.staff_units]

    def append_to_staff_unit(self, db: Session,
                             body: DocumentStaffFunctionAppendToStaffUnit):
        staff_function = self.get_by_id(db, body.staff_function_id)
        staff_units = db.query(StaffUnit).filter(
            StaffUnit.id.in_(body.staff_unit_ids)).all()
        for i in staff_units:
            i.staff_functions.append(staff_function)
            db.add(i)
        db.flush()

    def get_by_staff_unit(self, db: Session, staff_unit: StaffUnit):
        return db.query(self.model).filter(
            self.model.staff_units.contains(staff_unit)).all()


document_staff_function_service = DocumentStaffFunctionService(
    DocumentStaffFunction)
