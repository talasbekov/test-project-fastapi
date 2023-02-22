import datetime
import os
import tempfile
from typing import List

from docxtpl import DocxTemplate
from fastapi.logger import logger as log
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from core import Base
from exceptions import (BadRequestException, ForbiddenException,
                        InvalidOperationException, NotFoundException)
from models import HrDocument, HrDocumentInfo, HrDocumentStatus, User
from schemas import (HrDocumentCreate, HrDocumentInit, HrDocumentRead,
                     HrDocumentSign, HrDocumentUpdate)
from services import (badge_service, hr_document_info_service,
                      hr_document_step_service, hr_document_template_service,
                      rank_service, staff_division_service, staff_unit_service,
                      user_service)

from .base import ServiceBase

options = {
    'position': staff_unit_service,
    'actual_position': staff_unit_service,
    'group': staff_division_service,
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

        document.users = users

        next_step = hr_document_step_service.get_next_step_from_id(db, step.id)

        if next_step is None:
            return self._finish_document(db, document, document.users)

        hr_document_info_service.create_info_for_step(db, document.id, step.id, user.id, True)
        hr_document_info_service.create_next_info_for_step(db, document.id, next_step.id)

        db.add(document)
        db.flush()

        return document

    def get_all(self, db: Session, user_id, skip: int, limit: int):

        user = user_service.get_by_id(db, user_id)

        infos = hr_document_info_service.get_all(db, user.staff_unit_id, skip, limit)

        s = set()

        l = []

        for i in infos:
            if i.hr_document_id not in s:
                s.add(i.hr_document_id)
                l.append(self._to_response(i))

        return l
    
    def get_not_signed_documents(self, db: Session, user_id: str, skip: int, limit: int):

        user = user_service.get_by_id(db, user_id)

        infos = hr_document_info_service.get_not_signed_by_position(db, user.staff_unit_id, skip, limit)

        s = set()

        l = []

        for i in infos:
            if i.hr_document_id not in s:
                s.add(i.hr_document_id)
                l.append(self._to_response(i))

        return l

    def sign(self, db: Session, id: str, body: HrDocumentSign, user_id: str, role: str):

        document = self.get_by_id(db, id)

        info = hr_document_info_service.get_last_unsigned_step_info(db, id)

        if role != info.hr_document_step.position.name:
            raise ForbiddenException(detail=f'Вы не можете подписать этот документ!')

        user: User = user_service.get_by_id(db, user_id)

        if not info.hr_document_step.role.can_cancel:
            body.is_signed = True

        hr_document_info_service.sign(db, info, user_id, body.comment, body.is_signed)

        if body.is_signed:
            next_step = hr_document_step_service.get_next_step_from_id(db, info.hr_document_step_id)

            if next_step is None:
                return self._finish_document(db, document, document.users)

            hr_document_info_service.create_next_info_for_step(db, document.id, next_step.id)
            document.status = HrDocumentStatus.IN_PROGRESS

        else:

            step = hr_document_step_service.get_initial_step_for_template(db, document.document_template.id)

            info = hr_document_info_service.create_info_for_step(db, document.id, step.id, None, None)

            document.status = HrDocumentStatus.ON_REVISION

        db.add(document)
        db.flush()

        return document

    def generate(self, db: Session, id: str):

        document = self.get_by_id(db, id)
        document_template = hr_document_template_service.get_by_id(db, document.hr_document_template_id)

        template = DocxTemplate(document_template.path)

        context = {}

        for i in list(document.properties):
            if isinstance(document.properties[i], dict):
                context[i] = document.properties[i]['name']
            else:
                context[i] = document.properties[i]

        template.render(context)

        with tempfile.NamedTemporaryFile(delete=False) as temp_file:

            file_name = temp_file.name + ".docx"

            template.save(file_name)

        return FileResponse(
            path=file_name,
            media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            filename=document_template.name + '.docx'
        )

    def get_all_by_option(self, db: Session, option: str):
        service = options.get(option)
        if service is None:
            raise InvalidOperationException(
                f'Работа с {option} еще не поддерживается! Обратитесь к администратору для получения информации!')
        return service.get_multi(db)

    def _finish_document(self, db: Session, document: HrDocument, users: List[User]):

        document.status = HrDocumentStatus.COMPLETED

        fields = user_service.get_fields()
        print("fields:  ", fields)

        props = document.document_template.properties
        print("properties:  ", props)

        for key in list(props):

            value = props[key]
            print("value:  ", value)

            if value['type'] == 'read':
                continue

            if value['field_name'] not in fields:
                raise InvalidOperationException(f'Operation on {value["field_name"]} is not supported yet!')

            for user in users:
                if value['data_taken'] == "auto":
                    self._set_attr(db, user, value['field_name'], value['value'])

                else:
                    if key in document.properties:
                        val = document.properties.get(key)
                        print("val:  ", val)
                        if val is None:
                            raise BadRequestException(f'Нет ключа {val} в document.properties')
                        if not type(val) == dict:
                            if value["data_taken"] == "datetime":  # change me
                                date_time = datetime.datetime.strptime(val, "%Y-%m-%d")
                                self._set_attr(db, user, value['field_name'], date_time)
                            else:
                                self._set_attr(db, user, value['field_name'], val)
                        else:
                            if val['value'] == None:
                                raise BadRequestException(f'Обьект {key} должен иметь value!')
                            self._set_attr(db, user, value['field_name'], val['value'])

        document.signed_at = datetime.datetime.now()

        db.add(document)
        db.flush()

        return document

    def _set_attr(self, db: Session, user: User, key: str, value):

        attr = getattr(user, key)

        if isinstance(attr, Base):
            res = self._get_service(key).get_by_id(db, value)
            setattr(user, key, res)

        elif isinstance(attr, list):
            res = self._get_service(key).get_by_id(db, value)
            attr.append(res)
            setattr(user, key, attr)

        elif isinstance(value, str) and datetime.date.strftime("%Y-%m-%d"):
            res = self._get_service(key).get_by_id(db, value)
            setattr(user, key, res)
            print("res:  ", res)

        else:
            setattr(user, key, value)

        db.add(user)
        db.flush()

        return user

    def _get_service(self, key):
        service = options.get(key)
        if service is None:
            raise InvalidOperationException(f'New state is encountered! Cannot change {key}!')
        return service

    def _to_response(self, info: HrDocumentInfo) -> HrDocumentRead:

        response = HrDocumentRead.from_orm(info.hr_document)
        response.can_cancel = info.hr_document_step.role.can_cancel

        return response


hr_document_service = HrDocumentService(HrDocument)
