import os
import uuid
import tempfile
from datetime import datetime

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from fastapi.logger import logger as log
from fastapi.responses import FileResponse
from docxtpl import DocxTemplate

from .base import ServiceBase

from core import Base
from models import HrDocument, HrDocumentStatus, User
from schemas import HrDocumentCreate, HrDocumentUpdate, HrDocumentInfoCreate
from exceptions import NotFoundException, ForbiddenException

from services import (
    hr_document_template_service,
    hr_document_info_service,
    hr_document_step_service,
    user_service,
    position_service,
    rank_service,
    group_service,
    badge_service
)

options = {
    'position': position_service.get_by_id,
    'actual_position': position_service.get_by_id,
    'group': group_service.get_by_id,
    'rank': rank_service.get_by_id,
    'badges': badge_service.get_by_id
}

class HrDocumentService(ServiceBase[HrDocument, HrDocumentCreate, HrDocumentUpdate]):

    def get_by_id(self, db: Session, id: str) -> HrDocument:
        document = super().get(db, id)
        if document is None:
            raise NotFoundException(detail="Document is not found!")
        return document
        
    def initialize(self, db: Session, body: HrDocumentCreate, user_id: str, role: str):

        user: User = user_service.get_by_id(db, user_id)

        template = hr_document_template_service.get_by_id(db, body.hr_document_template_id)
        document: HrDocument = super().create(db, body)

        step = hr_document_step_service.get_initial_step_for_template(db, template.id)

        if role != step.position.name:
            raise ForbiddenException(detail=f'Вы не можете инициализировать этот документ!')
        
        next_step = hr_document_step_service.get_next_step_from_id(db, step.id)

        if next_step is None:
            return self._finish_document(db, document)

        hr_document_info_service.create_info_for_step(db, document.id, step.id, user.id)
        hr_document_info_service.create_next_info_for_step(db, document.id, next_step.id)

        return document
    
    def get_not_signed_documents(self, db: Session, user_id: str, skip: int, limit: int):

        user = user_service.get_by_id(db, user_id)

        infos = hr_document_info_service.get_not_signed_by_position(db, user.position_id)

        return [i.hr_document for i in infos]
    
    def sign(self, db: Session, id: str, comment: str, user_id: str):

        document = self.get_by_id(db, id)
        info = hr_document_info_service.get_last_signed_step_info(db, id)
        
        hr_document_info_service.sign(db, info, user_id,  comment, True)

        next_step = hr_document_step_service.get_next_step_from_id(db, info.hr_document_step_id)
        
        if next_step is None:
            return self._finish_document(db, document, document.user)

        hr_document_info_service.create_next_info_for_step(db, document.id, next_step.id)
        document.status = HrDocumentStatus.IN_PROGRESS

        db.add(document)
        db.commit()
        db.refresh(document)

        return document
    
    def generate(self, db: Session, id: str):
        
        document = self.get_by_id(db, id)
        document_template = hr_document_template_service.get_by_id(db, document.hr_document_template_id)

        # if os.path.exists(document_template.path):
        #     raise NotFoundException(detail=f'Template file is not found! Check if this is correct: {document_template.path}')
        
        template = DocxTemplate(document_template.path)

        print(os.stat(document_template.path))
        print(os.path.exists(document_template.path))

        context = {
            'document_id': document.id,
            'document_template_id': document.hr_document_template_id,
        }

        template.render(document.properties)
        template.render(context)

        with tempfile.NamedTemporaryFile(delete=False) as file_path:

            file_path = document_template.path
            file_name = file_path
            template.save(file_name)

            return FileResponse(
                path=file_name,
                media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                filename=document_template.name + '.docx'
            )

    def _finish_document(self, db: Session, document: HrDocument, user: User):

        document.status = HrDocumentStatus.COMPLETED

        fields = user_service.get_fields()

        keys = list(document.details)

        for key in keys:
            if key in fields:
                self._set_attr(db, user, key, keys[key])

        db.add(document)
        db.commit()
        db.refresh(document)

        return document
    
    def _set_attr(self,db: Session, user: User, key: str, value):

        attr = getattr(user, key)

        if isinstance(attr, Base):
            res = options[key](db, value)
            log.info(res)
            setattr(user, key, res)

        elif isinstance(attr, list):
            res = options[key](db, value)
            attr.append(res)
            setattr(user, key, attr)

        else:
            setattr(user, key, value)

        db.add(user)
        db.commit()
        db.refresh(user)
        return user


hr_document_service = HrDocumentService(HrDocument)
