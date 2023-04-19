import uuid

from sqlalchemy.orm import Session

from exceptions import NotFoundException
from models import HrDocumentTemplate, HrDocumentStep, DocumentStaffFunction, User
from schemas import HrDocumentTemplateCreate, HrDocumentTemplateUpdate
from .base import ServiceBase

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
        return db.query(HrDocumentTemplate).filter(
            HrDocumentTemplate.name.ilike(f'%{name}%')
        ).offset(skip).limit(limit).all()

hr_document_template_service = HrDocumentTemplateService(HrDocumentTemplate)
