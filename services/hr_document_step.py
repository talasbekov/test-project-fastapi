import uuid

from fastapi import HTTPException, status
from fastapi.logger import logger as log
from sqlalchemy.orm import Session

from exceptions import BadRequestException, NotFoundException
from models import HrDocumentStep, HrDocumentTemplate
from schemas import (HrDocumentStepCreate, HrDocumentStepRead,
                     HrDocumentStepUpdate)
from services import hr_document_template_service

from .base import ServiceBase


class HrDocumentStepService(ServiceBase[HrDocumentStep, HrDocumentStepCreate, HrDocumentStepUpdate]):
    
    def get_by_id(self, db: Session, id: str):
        
        hr_document_step = super().get(db, id)

        if hr_document_step is None:
            raise NotFoundException(detail=f"Document Step with id: {id} is not found!")

        return hr_document_step
        
    def get_initial_step_for_template(self, db: Session, template_id: str):
        
        step = db.query(HrDocumentStep).filter(
            HrDocumentStep.hr_document_template_id == template_id,
            HrDocumentStep.previous_step_id == None
        ).first()
        
        if step is None:
            raise NotFoundException(detail=f'Initial step for template id: {template_id} is not found!')
        
        return step
    
    def get_next_step_from_id(self, db: Session, step_id: str):
        step = db.query(HrDocumentStep).filter(
            HrDocumentStep.previous_step_id == step_id
        ).first()

        return step

    def get_initial_steps(self, db: Session, skip: int, limit: int):

        steps = db.query(self.model).filter(
            self.model.previous_step_id == None
        ).offset(skip).limit(limit).all()

        return steps

    def update_step(self, db: Session, step_id: str, obj_in: HrDocumentStepUpdate):

        step = self.get_by_id(db, step_id)

        # if user is trying to change hr_document_template_id
        if step.hr_document_template_id != obj_in.hr_document_template_id:

            template = hr_document_template_service.get_by_id(db, obj_in.hr_document_template_id)

            # Change hr_document_template_id to child step is impossible
            if step.previous_step_id is not None:
                raise BadRequestException(f"Child steps can not change template type")

            steps = db.query(self.model).filter(
                self.model.hr_document_template_id == template.id
            ).all()

            for e in steps:
                e.hr_document_template_id = template.id
                db.add(e)


            db.flush()
            return self.get_by_id(db, step_id)

        else:
            return super().update(db=db, db_obj=step, obj_in=obj_in)


hr_document_step_service = HrDocumentStepService(HrDocumentStep)
