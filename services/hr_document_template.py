import uuid

from sqlalchemy.orm import Session

from exceptions import NotFoundException
from models import HrDocumentTemplate, HrDocumentStep, DocumentStaffFunction, User, StaffUnit
from schemas import (
    HrDocumentTemplateCreate,
    HrDocumentTemplateUpdate,
    DocumentStaffFunctionCreate,
    HrDocumentStepCreate,
)
from .base import ServiceBase
from services import hr_document_step_service, document_staff_function_service

"""
{
  "1": "uuid",
  "2": "uuid"
}
"""


class HrDocumentTemplateService(ServiceBase[HrDocumentTemplate, HrDocumentTemplateCreate, HrDocumentTemplateUpdate]):

    def get_by_id(self, db: Session, id: str) -> HrDocumentTemplate:
        hr_document_template = super().get(db, id)
        if hr_document_template is None:
            raise NotFoundException(detail=f'HrDocumentTemplate with id: {id} is not found!')
        return hr_document_template

    def get_steps_by_document_template_id(self, db: Session, document_template_id: str) -> dict[str, uuid.UUID]:
        
        all_steps = db.query(DocumentStaffFunction).filter(
            HrDocumentStep.hr_document_template_id == document_template_id,
            DocumentStaffFunction.priority != 1
        ).join(HrDocumentStep.staff_function).order_by(DocumentStaffFunction.priority.asc()).all()
         
        steps = {}
        for function in all_steps:
            function: DocumentStaffFunction
            staff_units_ids = [unit.id for unit in function.staff_units]

            user = db.query(User).filter(
                User.staff_unit_id.in_(staff_units_ids)
            ).first()
            steps[str(function.priority)] = str(user.id)
        print(steps)
        return steps

    def get_all_by_name(self, db: Session, name: str, skip: int, limit: int):
        if name:
            return db.query(HrDocumentTemplate).filter(
                HrDocumentTemplate.name.ilike(f'%{name}%')
            ).offset(skip).limit(limit).all()
        return super().get_multi(db, skip, limit)

    def get_all_archived(self, db: Session, skip: int, limit: int):
        return (
            db.query(self.model)
            .filter(self.model.is_active == False)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def duplicate(self, db: Session, id: str):
        template = self.get_by_id(db, id)
        new_template =self.create(
            db,
            HrDocumentTemplateCreate(
                name=template.name if template.name is None else template.name + " (Копия)",
                nameKZ=template.nameKZ + " (Копия)",
                path=template.path,
                pathKZ=template.pathKZ,
                subject_type=template.subject_type,
                properties=template.properties,
                description=template.description,
                actions=template.actions,
            )
        )
        print(new_template.id)
        steps = hr_document_step_service.get_all_by_document_template_id(db, template.id)
        for step in steps:
            staff_function: DocumentStaffFunction = step.staff_function
            new_staff_function = document_staff_function_service.create(
                db,
                DocumentStaffFunctionCreate(
                    name=staff_function.name + " (Копия)",
                    nameKZ=staff_function.nameKZ if staff_function.nameKZ is None else staff_function.nameKZ + " (Копия)",
                    hours_per_week=staff_function.hours_per_week,
                    priority=staff_function.priority,
                    role_id=staff_function.role_id,
                    jurisdiction_id=staff_function.jurisdiction_id,
                )
            )
            new_staff_function.staff_units = staff_function.staff_units
            new_step = hr_document_step_service.create(
                db,
                HrDocumentStepCreate(
                    hr_document_template_id=new_template.id,
                    staff_function_id=new_staff_function.id,
                )
            )
            db.add(new_staff_function)
        db.add(new_template)
        return new_template


hr_document_template_service = HrDocumentTemplateService(HrDocumentTemplate)
