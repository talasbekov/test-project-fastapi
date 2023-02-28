import datetime
import random
import tempfile
import urllib.parse
import urllib.request
import uuid
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
    'staff_unit': staff_unit_service,
    'actual_staff_unit': staff_unit_service,
    'staff_division': staff_division_service,
    'rank': rank_service,
    'badges': badge_service
}


class HrDocumentService(ServiceBase[HrDocument, HrDocumentCreate, HrDocumentUpdate]):

    def get_by_id(self, db: Session, id: str) -> HrDocument:
        document = super().get(db, id)
        if document is None:
            raise NotFoundException(detail="Document is not found!")
        return document
    
    def get_all(self, db: Session, user_id, skip: int, limit: int):

        user = user_service.get_by_id(db, user_id)

        infos = hr_document_info_service.get_all(db, user.actual_staff_unit_id, skip, limit)

        return self._return_correctly(db, infos, user)

    def get_not_signed_documents(self, db: Session, user_id: str, skip: int, limit: int):

        user = user_service.get_by_id(db, user_id)

        infos = hr_document_info_service.get_not_signed_by_position(db, user.actual_staff_unit_id, skip, limit)

        return self._return_correctly(db, infos, user)

    def initialize(self, db: Session, body: HrDocumentInit, user_id: str, role: str):

        template = hr_document_template_service.get_by_id(db, body.hr_document_template_id)

        step = hr_document_step_service.get_initial_step_for_template(db, template.id)

        if role != step.staff_unit.name:
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

    def sign(self, db: Session, id: str, body: HrDocumentSign, user_id: str, role: str):

        document = self.get_by_id(db, id)

        info = hr_document_info_service.get_last_unsigned_step_info(db, id)

        if role != info.hr_document_step.staff_unit.name:
            raise ForbiddenException(detail=f'Вы не можете подписать этот документ из-за роли!')

        if not self._check_for_department(db, user_service.get_by_id(db, user_id), document.users[0]):
            raise ForbiddenException(detail=f'Вы не можете подписать документ относящийся не к вашему департаменту!')

        user: User = user_service.get_by_id(db, user_id)

        if not info.hr_document_step.staff_function.can_cancel:
            body.is_signed = True

        hr_document_info_service.sign(db, info, user_id, body.comment, body.is_signed)

        if body.is_signed:

            next_step = hr_document_step_service.get_next_step_from_id(db, info.hr_document_step_id)

            if info.hr_document_step.staff_function.name == "Утверждающий": # Закончить на staff function Утверждающий
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

        with tempfile.NamedTemporaryFile(delete=False) as temp:

            arr = document_template.path.rsplit('.')
            extension = arr[len(arr)-1]
            temp_file_path = temp.name + '.' + extension

            urllib.request.urlretrieve(document_template.path, temp_file_path)

        template = DocxTemplate(temp_file_path)

        context = {}

        for i in list(document.properties):
            if isinstance(document.properties[i], dict):
                context[i] = document.properties[i]['name']
            else:
                context[i] = document.properties[i]
        if document.reg_number is not None:
            context["reg_number"] = document.reg_number
        if document.signed_at is not None:
            context["signed_at"] = document.signed_at.strftime("%Y-%m-%d")

        template.render(context)

        with tempfile.NamedTemporaryFile(delete=False) as temp_file:

            file_name = temp_file.name + extension

            template.save(file_name)

        return FileResponse(
            path=file_name,
            media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            filename=document_template.name + extension
        )

    def get_all_by_option(self, db: Session, option: str, data_taken: str, id: uuid.UUID):
        service = options.get(option)
        if service is None:
            raise InvalidOperationException(f'Работа с {option} еще не поддерживается! Обратитесь к администратору для получения информации!')
        if data_taken is not None and data_taken == "matreshka":
            if id is None:
                return service.get_parents(db)
            else:
                return service.get_by_id(db, id).children
        return service.get_multi(db)
    
    def get_signed_documents(self, db: Session, user_id: uuid.UUID, skip: int, limit: int):

        user = user_service.get_by_id(db, user_id)

        infos = hr_document_info_service.get_signed_by_user_id(db, user_id, skip, limit)

        return self._return_correctly(db, infos, user)

    def _finish_document(self, db: Session, document: HrDocument, users: List[User]):

        document.status = HrDocumentStatus.COMPLETED

        fields = user_service.get_fields()

        props = document.document_template.properties

        for key in list(props):

            value = props[key]

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
                        if val is None:
                            raise BadRequestException(f'Нет ключа {val} в document.properties')
                        if not type(val) == dict:
                            self._set_attr(db, user, value['field_name'], val)
                        else:
                            if val['value'] == None:
                                raise BadRequestException(f'Обьект {key} должен иметь value!')
                            self._set_attr(db, user, value['field_name'], val['value'])

        document.signed_at = datetime.datetime.now()
        document.reg_number = str(random.randint(1, 10000)) + "-" + str(random.randint(1, 10000)) + "қбп/жқ"

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
    
    def _to_response(self, db: Session, info: HrDocumentInfo) -> HrDocumentRead:

        response = HrDocumentRead.from_orm(info.hr_document)
        response.can_cancel = info.hr_document_step.staff_function.can_cancel

        user = response.users[0]

        fields = user_service.get_fields()

        props = info.hr_document.document_template.properties

        new_val = {}

        for key in list(props):
            
            value = props[key]

            if value['type'] == 'read':
                continue

            if value['field_name'] not in fields:
                raise InvalidOperationException(f'Operation on {value["field_name"]} is not supported yet!')
            
            if value['data_taken'] == "auto":
                attr = getattr(user, value['field_name'])
                if isinstance(attr, Base) or isinstance(attr, list):
                    new_val[value['field_name']] = self._get_service(value['field_name']).get(db, value['value'])
                else:
                    new_val[value['field_name']] = value['value']
            
            else:

                val = info.hr_document.properties.get(key)
                
                if val is None:
                    continue
                    # raise BadRequestException(f'Нет ключа {val} в document.properties')
                
                if not type(val) == dict:
                    attr = getattr(user, value['field_name'])
                    if isinstance(attr, Base or isinstance(attr, list)):
                        new_val[value['field_name']] = self._get_service(value['field_name']).get(db, val)
                    else:
                        new_val[value['field_name']] = val
                else:
                    if val['value'] == None:
                        raise BadRequestException(f'Обьект {key} должен иметь value!')
                    new_val[value['field_name']] = self._get_service(value['field_name']).get(db, val['value'])

        response.new_value = new_val

        return response
    
    def _check_for_department(self, db: Session, user: User, subject: User) -> bool:

        department_id = staff_division_service.get_department_id_from_staff_division_id(db, user.staff_division_id)
        
        subject_department_id = staff_division_service.get_department_id_from_staff_division_id(db, subject.staff_division_id)

        print(department_id, subject_department_id)

        if department_id == subject_department_id:
            return True
        return False
    
    def _return_correctly(self,db: Session, infos: List[HrDocumentInfo], user: User) -> List[HrDocumentRead]:

        s = set()

        l = []

        for i in infos:
            if i.hr_document_id not in s:
                print(i.hr_document_id)
                s.add(i.hr_document_id)
                subject = i.hr_document.users[0]
                # print(subject.id)
                if self._check_for_department(db, user, subject):
                    l.append(self._to_response(db, i))

        return l

hr_document_service = HrDocumentService(HrDocument)
