import random
import tempfile
import urllib.parse
import urllib.request
import uuid
from datetime import datetime
from typing import List

from docxtpl import DocxTemplate
from fastapi.logger import logger as log
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from core import Base
from exceptions import (BadRequestException, ForbiddenException,
                        InvalidOperationException, NotFoundException)
from models import (HrDocument, HrDocumentInfo, HrDocumentStatusEnum,
                    HrDocumentStep, StaffUnit, User, DocumentStaffFunction, StaffDivision, JurisdictionEnum,
                    HrDocumentStatus, StaffDivisionEnum)
from schemas import (BadgeRead, HrDocumentCreate, HrDocumentInit,
                     HrDocumentRead, HrDocumentSign, HrDocumentUpdate,
                     RankRead, StaffDivisionOptionRead, StaffDivisionRead,
                     StaffUnitRead, DocumentStaffFunctionRead)
from services import (badge_service, document_staff_function_service,
                      document_staff_function_type_service,
                      hr_document_info_service, hr_document_step_service,
                      hr_document_template_service, rank_service,
                      staff_division_service, staff_unit_service, user_service,
                      jurisdiction_service, hr_document_status_service)

from .base import ServiceBase

options = {
    "staff_unit": staff_unit_service,
    "actual_staff_unit": staff_unit_service,
    "staff_division": staff_division_service,
    "rank": rank_service,
    "badges": badge_service,
}

responses = {
    "staff_unit": StaffUnitRead,
    "actual_staff_unit": StaffUnitRead,
    "staff_division": StaffDivisionOptionRead,
    "rank": RankRead,
    "badges": BadgeRead,
}


class HrDocumentService(ServiceBase[HrDocument, HrDocumentCreate, HrDocumentUpdate]):
    def get_by_id(self, db: Session, id: str) -> HrDocument:
        document = super().get(db, id)
        if document is None:
            raise NotFoundException(detail="Document is not found!")
        return document

    def get_initialized_documents(self, db: Session, user_id: uuid.UUID, skip: int, limit: int):

        user = user_service.get_by_id(db, user_id)

        documents = [i.hr_document for i in
                     hr_document_info_service.get_initialized_by_user_id(db, user_id, skip, limit)]

        return self._return_correctly(db, documents, user)

    def get_not_signed_documents(
            self, db: Session, user_id: str, skip: int, limit: int
    ):
        user = user_service.get_by_id(db, user_id)

        staff_unit = staff_unit_service.get_by_id(db, user.actual_staff_unit_id)

        staff_function_ids = [i.id for i in staff_unit.staff_functions]

        documents = (
            db.query(self.model)
            .join(HrDocumentStep)
            .filter(HrDocumentStep.staff_function_id.in_(staff_function_ids))
            .offset(skip)
            .limit(limit)
            .all()
        )

        return self._return_correctly(db, documents, user)

    def initialize(self, db: Session, body: HrDocumentInit, user_id: str, role: str):
        template = hr_document_template_service.get_by_id(
            db, body.hr_document_template_id
        )

        step: HrDocumentStep = hr_document_step_service.get_initial_step_for_template(
            db, template.id
        )

        staff_unit: StaffUnit = staff_unit_service.get_by_id(db, role)

        if step.staff_function not in staff_unit.staff_functions:
            raise ForbiddenException(
                detail=f"Вы не можете инициализировать этот документ!"
            )

        document_staff_function: DocumentStaffFunction = document_staff_function_service.get_by_id(db,
                                                                                                   step.staff_function_id)

        if not self._check_jurisdiction(db, staff_unit, document_staff_function, body.user_ids):
            raise ForbiddenException(
                detail=f"Вы не можете инициализировать этот документ из-за юрисдикции!"
            )

        all_steps: list = hr_document_step_service.get_all_by_document_template_id(
            db, template.id
        )
        all_steps.remove(step)

        if len(all_steps) < 2:
            raise BadRequestException(detail="Документ должен иметь хотя бы 2 шага!")

        users = [v for _, v in body.document_step_users_ids.items()]

        if len(users) != len(all_steps):
            raise BadRequestException(
                detail="Количество пользователей не соответствует количеству шагов!"
            )
        current_user = user_service.get_by_id(db, user_id)

        status = hr_document_status_service.get_by_name(db, HrDocumentStatusEnum.IN_PROGRESS.value)

        document: HrDocument = super().create(
            db,
            HrDocumentCreate(
                hr_document_template_id=body.hr_document_template_id,
                status_id=status.id,
                due_date=body.due_date,
                properties=body.properties,
            ),
        )
        # comm = ""

        # for key in list(template.properties):
        #     value = template.properties[key]

        #     if value['type'] != "read" and value['data_taken'] != "manual":
        #         continue

        #     if comm != "":
        #         comm = ", " + comm + value['alias_name'] + ": " + document.properties[key]
        #     else:
        #         comm = comm + value['alias_name'] + ": " + document.properties[key] + ", "

        document_info_initiator = hr_document_info_service.create_info_for_step(
            db, document.id, step.id, user_id, True, None, datetime.now()
        )

        hr_document_info_service.sign(
            db, document_info_initiator, current_user, None, True
        )

        for step, user_id in zip(all_steps, users):
            hr_document_info_service.create_info_for_step(
                db, document.id, step.id, user_id, None, None, None
            )

        users_document = [
            user_service.get_by_id(db, user_id) for user_id in body.user_ids
        ]

        document.last_step_id = all_steps[0].id
        document.users = users_document

        db.add(document)
        db.flush()

        return document

    def sign(
            self,
            db: Session,
            document_id: str,
            body: HrDocumentSign,
            user_id: str,
            role: str,
    ):
        document = self.get_by_id(db, document_id)

        completed_status: HrDocumentStatus = hr_document_status_service.get_by_name(db,
                                                                                    HrDocumentStatusEnum.COMPLETED.value)

        if document.last_step is None and document.status_id is completed_status.id:
            raise InvalidOperationException(detail=f'Document is already signed!')

        info = hr_document_info_service.get_by_document_id_and_step_id(
            db, document_id, document.last_step_id
        )

        staff_unit = staff_unit_service.get_by_id(db, role)

        if info.hr_document_step.staff_function not in staff_unit.staff_functions:
            raise ForbiddenException(
                detail=f"Вы не можете подписать этот документ из-за роли!"
            )

        step: HrDocumentStep = hr_document_step_service.get_initial_step_for_template(
            db, document.hr_document_template_id
        )

        document_staff_function: DocumentStaffFunction = document_staff_function_service.get_by_id(db,
                                                                                                   step.staff_function_id)

        user_ids = []
        for user in document.users:
            user_ids.append(user.id)

        if not self._check_jurisdiction(db, staff_unit, document_staff_function, user_ids):
            raise ForbiddenException(
                detail=f"Вы не можете инициализировать этот документ из-за юрисдикции!"
            )

        user: User = user_service.get_by_id(db, user_id)

        if not self._check_for_department(db, user, document.users[0]):
            raise ForbiddenException(
                detail=f"Вы не можете подписать документ относящийся не к вашему департаменту!"
            )

        hr_document_info_service.sign(db, info, user, body.comment, body.is_signed)

        if body.is_signed:
            next_step = hr_document_step_service.get_next_step_from_previous_step(
                db, info.hr_document_step
            )

            if next_step is None:
                return self._finish_document(db, document, document.users)

            document.last_step_id = next_step.id

            in_progress_status: HrDocumentStatus = hr_document_status_service.get_by_name(db,
                                                                                          HrDocumentStatusEnum.IN_PROGRESS.value)

            document.status_id = in_progress_status.id

        else:
            steps = hr_document_step_service.get_all_by_document_template_id(
                db, document.hr_document_template_id
            )

            for step in steps:

                signed_info = hr_document_info_service.get_signed_by_document_id_and_step_id(db, document.id, step.id)

                hr_document_info_service.create_info_for_step(
                    db, document.id, step.id, signed_info.assigned_to_id, None, None, None
                )

                if step == info.hr_document_step:
                    break

            document.last_step = steps[0]

            on_revision_status: HrDocumentStatus = hr_document_status_service.get_by_name(db,
                                                                                          HrDocumentStatusEnum.ON_REVISION.value)

            document.status_id = on_revision_status.id

        db.add(document)
        db.flush()

        return document

    def generate(self, db: Session, id: str):
        document = self.get_by_id(db, id)
        document_template = hr_document_template_service.get_by_id(
            db, document.hr_document_template_id
        )

        with tempfile.NamedTemporaryFile(delete=False) as temp:
            arr = document_template.path.rsplit(".")
            extension = arr[len(arr) - 1]
            temp_file_path = temp.name + "." + extension

            urllib.request.urlretrieve(document_template.path, temp_file_path)

        template = DocxTemplate(temp_file_path)

        context = {}

        for i in list(document.properties):
            if isinstance(document.properties[i], dict):
                context[i] = document.properties[i]["name"]
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
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            filename=document_template.name + extension,
        )

    def get_all_by_option(
            self, db: Session, option: str, data_taken: str, id: uuid.UUID
    ):
        service = options.get(option)
        if service is None:
            raise InvalidOperationException(
                f"Работа с {option} еще не поддерживается! Обратитесь к администратору для получения информации!"
            )
        if data_taken is not None and data_taken == "matreshka":
            if id is None:
                return [responses.get(option).from_orm(i) for i in service.get_parents(db)]
            else:
                return [responses.get(option).from_orm(i) for i in service.get_by_id(db, id).children]
        return [responses.get(option).from_orm(i) for i in service.get_multi(db)]

    def _finish_document(self, db: Session, document: HrDocument, users: List[User]):
        completed_status = hr_document_status_service.get_by_name(db, HrDocumentStatusEnum.COMPLETED.value)
        document.status_id = completed_status.id

        fields = user_service.get_fields()

        props = document.document_template.properties

        for key in list(props):
            value = props[key]

            if value["type"] == "read":
                continue

            if value["field_name"] not in fields:
                raise InvalidOperationException(
                    f'Operation on {value["field_name"]} is not supported yet!'
                )

            for user in users:
                if value["data_taken"] == "auto":
                    self._set_attr(db, user, value["field_name"], value["value"])

                else:
                    if key in document.properties:
                        val = document.properties.get(key)
                        if val is None:
                            raise BadRequestException(
                                f"Нет ключа {val} в document.properties"
                            )
                        if not type(val) == dict:
                            self._set_attr(db, user, value["field_name"], val)
                        else:
                            if val["value"] == None:
                                raise BadRequestException(
                                    f"Обьект {key} должен иметь value!"
                                )
                            self._set_attr(db, user, value["field_name"], val["value"])

        document.signed_at = datetime.now()
        document.reg_number = (
                str(random.randint(1, 10000))
                + "-"
                + str(random.randint(1, 10000))
                + "қбп/жқ"
        )

        document.last_step_id = None

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
            raise InvalidOperationException(
                f"New state is encountered! Cannot change {key}!"
            )
        return service

    def _to_response(self, db: Session, document: HrDocument) -> HrDocumentRead:
        response = HrDocumentRead.from_orm(document)
        if document.last_step_id is not None:
            response.can_cancel = document.last_step.staff_function.role.can_cancel

        user = response.users[0]

        fields = user_service.get_fields()

        props = document.document_template.properties

        new_val = {}

        for key in list(props):
            value = props[key]

            if value["type"] == "read":
                continue

            if value["field_name"] not in fields:
                raise InvalidOperationException(
                    f'Operation on {value["field_name"]} is not supported yet!'
                )

            if value["data_taken"] == "auto":
                attr = getattr(user, value["field_name"])
                if isinstance(attr, Base) or isinstance(attr, list):
                    new_val[value["field_name"]] = self._get_service(
                        value["field_name"]
                    ).get(db, value["value"])
                else:
                    new_val[value["field_name"]] = value["value"]

            else:
                val = document.properties.get(key)

                if val is None:
                    continue
                    # raise BadRequestException(f'Нет ключа {val} в document.properties')

                if not type(val) == dict:
                    attr = getattr(user, value["field_name"])
                    if isinstance(attr, Base or isinstance(attr, list)):
                        new_val[value["field_name"]] = responses.get(value['field_name']).from_orm(self._get_service(
                            value["field_name"]
                        ).get(db, val))
                    else:
                        new_val[value["field_name"]] = val
                else:
                    if val["value"] == None:
                        raise BadRequestException(f"Обьект {key} должен иметь value!")
                    new_val[value["field_name"]] = responses.get(value['field_name']).from_orm(self._get_service(
                        value["field_name"]
                    ).get(db, val["value"]))

        response.new_value = new_val

        return response

    def _check_for_department(self, db: Session, user: User, subject: User) -> bool:
        department_id = staff_division_service.get_department_id_from_staff_division_id(
            db, user.staff_unit.staff_division_id
        )

        subject_department_id = (
            staff_division_service.get_department_id_from_staff_division_id(
                db, subject.staff_unit.staff_division_id
            )
        )

        if department_id == subject_department_id:
            return True
        return False

    def _return_correctly(
            self, db: Session, documents: List[HrDocument], user: User
    ) -> List[HrDocumentRead]:
        s = set()

        l = []

        for i in documents:
            if i is None:
                continue
            if i.id not in s:
                s.add(i.id)
                subject = i.users[0]
                # print(subject.id)
                if self._check_for_department(db, user, subject):
                    l.append(self._to_response(db, i))

        return l

    def _check_jurisdiction(
            self, db: Session, staff_unit: StaffUnit, document_staff_function: DocumentStaffFunction,
            subject_user_ids: List[uuid.UUID]
    ) -> bool:
        jurisdiction = jurisdiction_service.get_by_id(db, document_staff_function.jurisdiction_id)

        # Проверка на вид юрисдикции "Вся служба"
        if jurisdiction.name == JurisdictionEnum.ALL_SERVICE.value:
            return True

        staff_division = staff_division_service.get_by_id(db, staff_unit.staff_division_id)

        # Проверка на вид юрисдикции "Боевое подразделение"
        if jurisdiction.name == JurisdictionEnum.COMBAT_UNIT.value:
            return staff_division.is_combat_unit

        # Проверка на вид юрисдикции "Штатное подразделение"
        if jurisdiction.name == JurisdictionEnum.STAFF_UNIT.value:
            return not staff_division.is_combat_unit

        subject_users: List[User] = []

        for i in subject_user_ids:
            subject_users.append(user_service.get_by_id(db, i))

        # Проверка на вид юрисдикции "Личное дело"
        if jurisdiction.name == JurisdictionEnum.PERSONNEL.value:
            self._check_personnel_jurisdiction(db, staff_unit=staff_unit, staff_division=staff_division, subject_users=subject_users)

        # Проверка на вид юрисдикции Курируемые сотрудники
        if jurisdiction.name == JurisdictionEnum.SUPERVISED_EMPLOYEES.value:
            self._check_supervised_jurisdiction(subject_users=subject_users)

        # Проверка на вид юрисдикции Кандидаты
        if jurisdiction.name == JurisdictionEnum.CANDIDATES.value:
            self._check_candidates_jurisdiction(db, subject_users=subject_users)

        return False

    def _check_personnel_jurisdiction(self, db: Session, staff_unit: StaffUnit, staff_division: StaffDivision,
                                      subject_users: List[User]) -> bool:
        # Получаем все дочерние штатные группы пользователя, включая саму группу
        staff_divisions: List[StaffDivision] = staff_division_service.get_child_groups(db, staff_unit.staff_division_id)
        staff_divisions.append(staff_division)

        # Получаем все staff unit из staff divisions
        staff_units: List[StaffUnit] = []
        for i in staff_divisions:
            staff_units.extend(staff_unit_service.get_by_staff_division_id(db, i.id))

        # Проверка субъекта на присутствие в штатной единице
        # Метод возвращает True если все из субъектов относятся к штатной единице
        # Если один из субъектов не относится к штатной единице то метод выбрасывает False
        for i in subject_users:
            if i.actual_staff_unit not in staff_units:
                return False

        return True

    def _check_supervised_jurisdiction(self, subject_users: List[User]) -> bool:
        for i in subject_users:
            if i.supervised_by is None:
                return False

        return True

    def _check_candidates_jurisdiction(self, db: Session, subject_users: List[User]):
        staff_units: List[StaffUnit] = []
        for i in subject_users:
            staff_units.append(i.staff_unit)

        candidates_staff_division = staff_division_service.get_by_name(db, StaffDivisionEnum.CANDIDATES.value)

        for i in staff_units:
            if not i.staff_division_id == candidates_staff_division.id:
                return False

        return True


hr_document_service = HrDocumentService(HrDocument)
