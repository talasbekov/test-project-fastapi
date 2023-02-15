import os
import uuid
import tempfile
from datetime import datetime

from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from fastapi.logger import logger as log
from fastapi.responses import FileResponse
from docxtpl import DocxTemplate

from .base import ServiceBase

from core import Base
from models import HrDocument, HrDocumentStatus, User
from schemas import (
    HrDocumentCreate,
    HrDocumentUpdate,
    HrDocumentInfoCreate,
    HrDocumentInit,
    HrDocumentSign
)

from exceptions import (
    NotFoundException,
    ForbiddenException,
    InvalidOperationException,
    BadRequestException
)

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
    'position': position_service,
    'actual_position': position_service,
    'group': group_service,
    'rank': rank_service,
    'badges': badge_service
}

class HrDocumentService(ServiceBase[HrDocument, HrDocumentCreate, HrDocumentUpdate]):

    def get_by_id(self, db: Session, id: str) -> HrDocument:
        document = super().get(db, id)
        if document is None:
            raise NotFoundException(detail="Document is not found!")
        return document
        
    def initialize(self, db: Session, body: HrDocumentInit, user_id: str, role: str):

        template = hr_document_template_service.get_by_id(db, body.hr_document_template_id)

        step = hr_document_step_service.get_initial_step_for_template(db, template.id)

        if role != step.position.name:
            raise ForbiddenException(detail=f'Вы не можете инициализировать этот документ!')

        user: User = user_service.get_by_id(db, user_id)


        document: HrDocument = super().create(db, HrDocumentCreate(
            hr_document_template_id=body.hr_document_template_id,
            status=HrDocumentStatus.INITIALIZED,
            due_date=body.due_date,
            properties=body.properties
        ))

        users = [user_service.get_by_id(db, i) for i in body.user_ids]

        document.user = users

        next_step = hr_document_step_service.get_next_step_from_id(db, step.id)

        if next_step is None:
            return self._finish_document(db, document, document.user)

        hr_document_info_service.create_info_for_step(db, document.id, step.id, user.id, True)
        hr_document_info_service.create_next_info_for_step(db, document.id, next_step.id)
 
        db.add(document)
        db.commit()
        db.refresh(document)
        return document
    
    def get_not_signed_documents(self, db: Session, user_id: str, skip: int, limit: int):

        user = user_service.get_by_id(db, user_id)

        infos = hr_document_info_service.get_not_signed_by_position(db, user.position_id)

        return [i.hr_document for i in infos]

    def sign(self, db: Session, id: str, body: HrDocumentSign, user_id: str, role: str):

        document = self.get_by_id(db, id)

        info = hr_document_info_service.get_last_unsigned_step_info(db, id)

        if role != info.hr_document_step.position.name:
            raise ForbiddenException(detail=f'Вы не можете подписать этот документ!')

        user: User = user_service.get_by_id(db, user_id)

        hr_document_info_service.sign(db, info, user_id, body.comment, body.is_signed)

        if body.is_signed:

            next_step = hr_document_step_service.get_next_step_from_id(db, info.hr_document_step_id)

            if next_step is None:
                return self._finish_document(db, document, document.user)

            hr_document_info_service.create_next_info_for_step(db, document.id, next_step.id)
            document.status = HrDocumentStatus.IN_PROGRESS

        else:

            step = hr_document_step_service.get_initial_step_for_template(db, document.document_template.id)

            info = hr_document_info_service.create_info_for_step(db, document.id, step.id, None, None)

            document.status = HrDocumentStatus.ON_REVISION

        db.add(document)
        db.commit()
        db.refresh(document)

        return document

    def generate(self, db: Session, id: str):
        
        document = self.get_by_id(db, id)
        document_template = hr_document_template_service.get_by_id(db, document.hr_document_template_id)

        if os.path.exists(document_template.path):
            raise NotFoundException(detail=f'Template file is not found! Check if this is correct: {document_template.path}')
        
        template = DocxTemplate(document_template.path)
        template.render(document.properties)

        with tempfile.NamedTemporaryFile(delete=False) as file_path:

            file_name = file_path + ".docx"
            template.save(file_name)

            return FileResponse(
                path=file_name,
                media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                filename=document_template.name + '.docx'
            )

    def _finish_document(self, db: Session, document: HrDocument, users: List[User]):

        document.status = HrDocumentStatus.COMPLETED

        fields = user_service.get_fields()

        props = document.document_template.properties

        for key in list(props):

            value = props[key]

            if value['type'] == 'read':
                continue

            if key not in fields:
                raise InvalidOperationException(f'Operation on {key} is not supported yet!')
            
            for user in users:

                if value['data_taken'] == "auto":
                    self._set_attr(db, user, value['field_name'], value['value'])

                else:
                    if key in document.properties:
                        val = document.properties.get(key)
                        if val is None:
                            raise BadRequestException(f'Нет ключа {val} в document.properties')
                        if not type(val) == dict:
                            self._set_attr(db, user, value['field_name'], val)
                        else:
                            if val['value'] == None:
                                raise BadRequestException(f'Обьект {key} должен иметь value!')
                            self._set_attr(db, user, value['field_name'], val['value'])

        db.add(document)
        db.commit()
        db.refresh(document)

        return document

    def _set_attr(self,db: Session, user: User, key: str, value):

        attr = getattr(user, key)

        if isinstance(attr, Base):
            res = self._get_service(key).get_by_id(db, value)
            setattr(user, key, res)

        elif isinstance(attr, list):
            res = self._get_service(key).get_by_id(db, value)
            attr.append(res)
            setattr(user, key, attr)

        else:
            setattr(user, key, value)

        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    def _get_service(self, key):
        service = options.get(key)
        if service is None:
            raise InvalidOperationException(f'New state is encountered! Cannot change {key}!')
        return service


hr_document_service = HrDocumentService(HrDocument)
