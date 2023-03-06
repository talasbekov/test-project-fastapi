import uuid

from sqlalchemy.orm import Session

from exceptions import NotFoundException
from models import DocumentStaffFunction, HrDocumentStep
from schemas import HrDocumentStepCreate, HrDocumentStepUpdate

from .base import ServiceBase


class HrDocumentStepService(ServiceBase[HrDocumentStep, HrDocumentStepCreate, HrDocumentStepUpdate]):

    def get_by_id(self, db: Session, id: str) -> HrDocumentStep:

        hr_document_step = super().get(db, id)

        if hr_document_step is None:
            raise NotFoundException(detail=f"Document Step with id: {id} is not found!")

        return hr_document_step

    def get_initial_step_for_template(self, db: Session, template_id: str):

        step = db.query(HrDocumentStep).filter(
            HrDocumentStep.hr_document_template_id == template_id,
            DocumentStaffFunction.priority > 0
        ).first()

        if step is None:
            raise NotFoundException(detail=f'Initial step for template id: {template_id} is not found!')

        return step

    def get_next_step_from_id(self, db: Session, step_id: str) -> HrDocumentStep:
        step = db.query(HrDocumentStep).filter(
            
        ).first()

        return step

    def get_initial_steps(self, db: Session, skip: int, limit: int):

        steps = db.query(self.model).filter(
            self.model.previous_step_id == None
        ).offset(skip).limit(limit).all()

        return steps

    def get_all_by_document_template_id(self, db: Session, template_id: uuid.UUID):

        steps = db.query(self.model).filter(
            self.model.hr_document_template_id == template_id
        ).join(self.model.staff_function).order_by(DocumentStaffFunction.priority.asc()).all()

        return steps

    def get_next_step_from_previous_step(self, db: Session, previous_step: HrDocumentStep):
        priority = previous_step.staff_function.priority

        step = db.query(self.model).join(DocumentStaffFunction).filter(
            self.model.hr_document_template_id == previous_step.hr_document_template_id,
            DocumentStaffFunction.priority > priority
        ).order_by(DocumentStaffFunction.priority.asc()).first()

        return step


hr_document_step_service = HrDocumentStepService(HrDocumentStep)
