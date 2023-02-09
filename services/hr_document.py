import uuid
from datetime import datetime

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from fastapi.logger import logger as log

from .base import ServiceBase

from models import HrDocument, HrDocumentStatus
from schemas import HrDocumentCreate, HrDocumentUpdate, HrDocumentInfoCreate
from exceptions import NotFoundException

from services import hr_document_template_service, hr_document_info_service, hr_document_step_service, user_service


class HrDocumentService(ServiceBase[HrDocument, HrDocumentCreate, HrDocumentUpdate]):
    def get_by_id(self, db: Session, id: str):
        document = super().get(db, id)
        if document is None:
            raise NotFoundException(detail="Document is not found!")
        return document
        
    def initialize(self, db: Session, body: HrDocumentCreate, user_id: str):

        template = hr_document_template_service.get_by_id(db, body.hr_document_template_id)
        document = super().create(db, body)

        step = hr_document_step_service.get_initial_step_for_template(db, template.id)
        next_step = hr_document_step_service.get_next_step_from_id(db, step.id)

        if next_step is None:
            return self._finish_document(db, document)

        hr_document_info_service.create_info_for_step(db, document.id, step.id, user_id)
        hr_document_info_service.create_next_info_for_step(db, document.id, next_step.id)

        return document
    
    def get_not_signed_documents(self, db: Session, user_id: str, skip: int, limit:int):

        user = user_service.get_by_id(db, user_id)

        infos = hr_document_info_service.get_not_signed_by_position(db, user.position_id)

        return [i.hr_document for i in infos]
    
    def sign(self, db: Session, id: str, comment: str, user_id: str):

        document = self.get_by_id(db, id)
        info = hr_document_info_service.get_last_signed_step_info(db, id)
        
        hr_document_info_service.sign(db, info, user_id,  comment, True)

        next_step = hr_document_step_service.get_next_step_from_id(db, info.hr_document_step_id)
        
        if next_step is None:
            return self._finish_document(db, document)        

        hr_document_info_service.create_next_info_for_step(db, document.id, next_step.id)
        document.status = HrDocumentStatus.IN_PROGRESS

        db.add(document)
        db.commit()
        db.refresh(document)

        return document
    
    def _finish_document(self, db: Session, document: HrDocument):

        document.status = HrDocumentStatus.COMPLETED

        db.add(document)
        db.commit()
        db.refresh(document)

        return document


hr_document_service = HrDocumentService(HrDocument)
