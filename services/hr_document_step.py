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

hr_document_step_service = HrDocumentStepService(HrDocumentStep)
