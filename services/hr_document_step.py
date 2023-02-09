import uuid

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from fastapi.logger import logger as log

from .base import ServiceBase
from models import HrDocumentStep
from schemas import HrDocumentStepCreate, HrDocumentStepUpdate, HrDocumentStepRead

from exceptions import NotFoundException


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
    


hr_document_step_service = HrDocumentStepService(HrDocumentStep)
