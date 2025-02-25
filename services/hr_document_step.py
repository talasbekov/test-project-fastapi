import uuid

from sqlalchemy.orm import Session

from exceptions import NotFoundException
from models import DocumentStaffFunction, HrDocumentStep
from schemas import HrDocumentStepCreate, HrDocumentStepUpdate
from .base import ServiceBase
from schemas import HrDocumentStepRead
from fastapi import HTTPException


class HrDocumentStepService(
        ServiceBase[HrDocumentStep, HrDocumentStepCreate, HrDocumentStepUpdate]):

    def get_by_id(self, db: Session, id: str) -> HrDocumentStep:

        hr_document_step = super().get(db, id)

        if hr_document_step is None:
            raise NotFoundException(
                detail=f"Document Step with id: {id} is not found!")

        return hr_document_step

    def get_initial_step_for_template(self, db: Session, template_id: str):

        step = db.query(HrDocumentStep).join(HrDocumentStep.staff_function).filter(
            HrDocumentStep.hr_document_template_id == template_id,
            DocumentStaffFunction.priority > 0
        ).order_by(DocumentStaffFunction.priority.asc()).first()

        if step is None:
            raise NotFoundException(
                detail=f'Initial step for template id: {template_id} is not found!')

        return step

    def get_initial_steps(self, db: Session, skip: int, limit: int):

        steps = db.query(self.model)\
            .join(DocumentStaffFunction)\
            .filter(DocumentStaffFunction.priority == 1)\
            .offset(skip)\
            .limit(limit)\
            .all()

        return steps

    def get_all_by_document_template_id(
            self, db: Session, template_id: str, notifiers: bool = True):

        # steps_query = db.query(self.model)\
        #     .filter(self.model.hr_document_template_id == template_id)\
        #     .join(self.model.staff_function)\
        #     .order_by(DocumentStaffFunction.priority.asc())
        steps_query = db.query(self.model).filter(self.model.hr_document_template_id == template_id)

        if not notifiers:
            steps_query = steps_query.filter(
                DocumentStaffFunction.priority != -1)
            
        result = steps_query.all()
        print(str(steps_query))
        print(result)
        if not result:
            raise HTTPException(status_code=404, detail="No steps found for this document template")

        return result

    def get_next_step_from_previous_step(
            self, db: Session, previous_step: HrDocumentStep):
        priority = previous_step.staff_function.priority

        step = db.query(self.model).join(DocumentStaffFunction).filter(
            self.model.hr_document_template_id == previous_step.hr_document_template_id,
            DocumentStaffFunction.priority > priority
        ).order_by(DocumentStaffFunction.priority.asc()).first()

        return step

    def get_all_notifiers_by_template_id(
            self, db: Session, template_id: str):
        return (
            db.query(self.model)
            .join(DocumentStaffFunction)
            .filter(
                self.model.hr_document_template_id == template_id,
                DocumentStaffFunction.priority == -1
            )
            .all()
        )

    def get_all_by_document_template_id_without_notifiers(
            self, db: Session, template_id: str):
        return (
            db.query(self.model)
            .join(DocumentStaffFunction)
            .filter(
                self.model.hr_document_template_id == template_id,
                DocumentStaffFunction.priority > 0
            )
            .all()
        )

    def get_last_step_document_template_id(
            self, db: Session, template_id: str):
        res = (
            db.query(self.model)
            .join(DocumentStaffFunction)
            .filter(
                self.model.hr_document_template_id == template_id,
                DocumentStaffFunction.priority == 100
            ).first()
        )
        if res is None:
            raise NotFoundException(
                detail=f'Last step for template id: {template_id} is not found!')
        return res


hr_document_step_service = HrDocumentStepService(HrDocumentStep)
