import pdfkit
import random
import tempfile
import urllib.parse
import urllib.request
import uuid
from datetime import datetime
from typing import List

from docxtpl import DocxTemplate
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy import func, or_

from core import Base, jinja_env, download_file_to_tempfile, wkhtmltopdf_path
from exceptions import (
    BadRequestException,
    ForbiddenException,
    InvalidOperationException,
    NotFoundException,
)
from models import (
    HrDocument,
    HrDocumentStatusEnum,
    HrDocumentStep,
    StaffUnit,
    User,
    DocumentStaffFunction,
    StaffDivision,
    JurisdictionEnum,
    HrDocumentStatus,
    StaffDivisionEnum,
    HrDocumentTemplate,
    HrDocumentInfo,
    LanguageEnum,
    DocumentFunctionTypeEnum,
)
from schemas import (
    BadgeRead,
    HrDocumentCreate,
    HrDocumentInit,
    HrDocumentRead,
    HrDocumentSign,
    HrDocumentUpdate,
    RankRead,
    StaffDivisionOptionRead,
    StaffUnitRead,
    DraftHrDocumentCreate,
    DraftHrDocumentInit,
    BadgeTypeRead,
    StatusTypeRead,
    CoolnessTypeRead,
    PenaltyTypeRead,
    ContractTypeRead,
    NotificationCreate,
)
from services import (
    badge_service,
    document_staff_function_service,
    hr_document_info_service,
    hr_document_step_service,
    hr_document_template_service,
    rank_service,
    staff_division_service,
    staff_unit_service,
    user_service,
    jurisdiction_service,
    hr_document_status_service,
    history_service,
    status_service,
    secondment_service,
    coolness_service,
    penalty_service,
    contract_service,
    notification_service,
)
from .base import ServiceBase
from ws import notification_manager

options = {
    "staff_unit": staff_unit_service,
    "actual_staff_unit": staff_unit_service,
    "staff_division": staff_division_service,
    "rank": rank_service,
    "badges": badge_service,
    'statuses': status_service,
    'secondments': secondment_service,
    'coolnesses': coolness_service,
    'penalties': penalty_service,
    'contracts': contract_service,
}

responses = {
    "staff_unit": StaffUnitRead,
    "actual_staff_unit": StaffUnitRead,
    "staff_division": StaffDivisionOptionRead,
    "rank": RankRead,
    "badges": BadgeTypeRead,
    'statuses': StatusTypeRead,
    'secondments': StaffDivisionOptionRead,
    'coolnesses': CoolnessTypeRead,
    'penalties': PenaltyTypeRead,
    'contracts': ContractTypeRead,
}

from .constructor import *

handlers = {
    "add_badge": add_badge_handler,
    "delete_badge": delete_badge_handler,
    "increase_rank": increase_rank_handler,
    "add_black_beret": add_black_beret_handler,
    "decrease_rank": decrease_rank_handler,
    "renew_contract": renew_contract_handler,
    "stop_status": stop_status_handler,
    "temporary_status_change": temporary_status_change_handler,
    "status_change": status_change_handler,
    "add_penalty": add_penalty_handler,
    "delete_penalty": delete_penalty_handler,
    "delete_black_beret": delete_black_beret_handler,
    "add_coolness": add_coolness_handler,
    "decrease_coolness": decrease_coolness_handler,
    "delete_coolness": delete_coolness_handler,
    "add_secondment": add_secondment_handler,
    "position_change": position_change_handler,
}


class HrDocumentService(ServiceBase[HrDocument, HrDocumentCreate, HrDocumentUpdate]):
    def get_by_id(self, db: Session, id: str) -> HrDocument:
        document = super().get(db, id)
        if document is None:
            raise NotFoundException(detail="Document is not found!")
        return document

    def get_initialized_documents(self, db: Session, user_id: uuid.UUID, filter: str, skip: int, limit: int):
        user = user_service.get_by_id(db, user_id)
        if filter is not None:
            key_words = filter.lower().split()
            documents = (
                db.query(self.model)
                .join(self.model.hr_document_infos)
                .join(HrDocumentStep)
                .join(DocumentStaffFunction)
                .filter(
                    HrDocumentInfo.assigned_to_id == user_id,
                    DocumentStaffFunction.priority == 1
                    )
                .join(self.model.users)
                .join(self.model.document_template)
                .filter((or_(*[func.lower(User.first_name).contains(name) for name in key_words])) |
                        (or_(*[func.lower(User.last_name).contains(name) for name in key_words])) |
                        (or_(*[func.lower(User.father_name).contains(name) for name in key_words]) |
                         (or_(*[func.lower(HrDocumentTemplate.name).contains(name) for name in key_words])))
                        )
                .order_by(self.model.due_date.asc())
                .offset(skip)
                .limit(limit)
                .all()
            )
        else:
            documents = [i.hr_document for i in
                         hr_document_info_service.get_initialized_by_user_id(db, user_id, skip, limit)]

        return self._return_correctly(db, documents, user)

    def get_not_signed_documents(
            self, db: Session, user_id: str, filter: str, skip: int, limit: int
    ):
        user = user_service.get_by_id(db, user_id)

        staff_unit = staff_unit_service.get_by_id(db, user.actual_staff_unit_id)

        staff_function_ids = [i.id for i in staff_unit.staff_functions]

        draft_status = hr_document_status_service.get_by_name(db, HrDocumentStatusEnum.DRAFT.value)

        if filter is not None:
            key_words = filter.lower().split()

            documents = (
                db.query(self.model)
                .filter(self.model.status_id != draft_status.id)
                .join(HrDocumentStep)
                .join(self.model.users)
                .filter(
                    HrDocumentStep.staff_function_id.in_(staff_function_ids) & (
                            (or_(*[func.lower(User.first_name).contains(name) for name in key_words])) |
                            (or_(*[func.lower(User.last_name).contains(name) for name in key_words])) |
                            (or_(*[func.lower(User.father_name).contains(name) for name in key_words])) |
                            (or_(*[func.lower(HrDocumentTemplate.name).contains(name) for name in key_words]))
                    )
                )
                .order_by(self.model.due_date.asc())
                .offset(skip)
                .limit(limit)
                .all()
            )
        else:
            documents = (
                db.query(self.model)
                .filter(self.model.status_id != draft_status.id)
                .join(HrDocumentStep)
                .filter(HrDocumentStep.staff_function_id.in_(staff_function_ids))
                .order_by(self.model.due_date.asc())
                .offset(skip)
                .limit(limit)
                .all()
            )

        return self._return_correctly(db, documents, user)

    def get_draft_documents(self, db: Session, user_id: str, skip: int = 0, limit: int = 100):
        status = hr_document_status_service.get_by_name(db, HrDocumentStatusEnum.DRAFT.value)

        return db.query(self.model).filter(
            self.model.status_id == status.id,
            self.model.initialized_by_id == user_id
        ).offset(skip).limit(limit).all()

    def save_to_draft(self, db: Session, user_id: str, body: DraftHrDocumentCreate, role: str):
        template = hr_document_template_service.get_by_id(
            db, body.hr_document_template_id
        )

        step: HrDocumentStep = hr_document_step_service.get_initial_step_for_template(
            db, template.id
        )

        self._validate_document(db, body=body, role=role, step=step)

        status = hr_document_status_service.get_by_name(db, HrDocumentStatusEnum.DRAFT.value)

        document: HrDocument = super().create(
            db,
            HrDocumentCreate(
                hr_document_template_id=body.hr_document_template_id,
                status_id=status.id,
                due_date=body.due_date,
                properties=body.properties,
            ),
        )

        users_document = [
            user_service.get_by_id(db, user_id) for user_id in body.user_ids
        ]

        document.users = users_document
        document.initialized_by_id = user_id

        db.add(document)
        db.flush()

        return document

    def initialize_draft_document(self, db: Session, body: DraftHrDocumentInit, document_id: str, user_id: str, role: str):
        document = hr_document_service.get_by_id(db, document_id)

        print(document.hr_document_template_id)

        template = hr_document_template_service.get_by_id(
            db, document.hr_document_template_id
        )

        step: HrDocumentStep = hr_document_step_service.get_initial_step_for_template(
            db, template.id
        )

        all_steps: list = hr_document_step_service.get_all_by_document_template_id(
            db, template.id
        )

        users = [v for _, v in body.document_step_users_ids.items()]
        subject_users_ids: List[uuid.UUID] = []

        for user in document.users:
            subject_users_ids.append(user.id)

        hr_document_init = HrDocumentInit(
            properties=document.properties,
            due_date=document.due_date,
            hr_document_template_id=document.hr_document_template_id,
            user_ids=subject_users_ids,
            document_step_users_ids=body.document_step_users_ids
        )

        self._validate_document(db, hr_document_init, role=role, step=step)
        self._validate_document_for_steps(step=step, all_steps=all_steps, users=users)

        current_user = user_service.get_by_id(db, user_id)

        status = hr_document_status_service.get_by_name(db, HrDocumentStatusEnum.IN_PROGRESS.value)

        document_info_initiator = hr_document_info_service.create_info_for_step(
            db, document_id, step.id, user_id, True, None, datetime.now()
        )

        hr_document_info_service.sign(
            db, document_info_initiator, current_user, None, True
        )

        for step, user_id in zip(all_steps, users):
            hr_document_info_service.create_info_for_step(
                db, document.id, step.id, user_id, None, None, None
            )

        document.last_step_id = all_steps[0].id
        document.status_id = status.id

        db.add(document)
        db.flush()

        return document

    async def initialize(self, db: Session, body: HrDocumentInit, user_id: str, role: str):
        template = hr_document_template_service.get_by_id(
            db, body.hr_document_template_id
        )

        step: HrDocumentStep = hr_document_step_service.get_initial_step_for_template(
            db, template.id
        )

        all_steps: list = hr_document_step_service.get_all_by_document_template_id(
            db, template.id
        )

        users = [v for _, v in body.document_step_users_ids.items()]

        self._validate_document(db, body=body, role=role, step=step)
        self._validate_document_for_steps(step=step, all_steps=all_steps, users=users)

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

        users_document = [
            user_service.get_by_id(db, user_id) for user_id in body.user_ids
        ]
        document.users = users_document

        if len(all_steps) == 0:
            self._finish_document(db, document, document.users, user_id)

        for step, user_id in zip(all_steps, users):
            hr_document_info_service.create_info_for_step(
                db, document.id, step.id, user_id, None, None, None
            )

        if len(all_steps) == 0:
            document.last_step_id = None
        else:
            document.last_step_id = all_steps[0].id

        db.add(document)
        db.flush()
        return document

    async def sign(
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

        if document_staff_function.role.name == DocumentFunctionTypeEnum.EXPERT.value:
            body.is_signed = True

        hr_document_info_service.sign(db, info, user, body.comment, body.is_signed)

        next_step = hr_document_step_service.get_next_step_from_previous_step(
                db, info.hr_document_step
            )

        if body.is_signed:
            if next_step is None:
                return self._finish_document(db, document, document.users, user_id)

            document.last_step_id = next_step.id

            in_progress_status: HrDocumentStatus = hr_document_status_service.get_by_name(db,
                                                                                          HrDocumentStatusEnum.IN_PROGRESS.value)

            document.status_id = in_progress_status.id

        else:
            if next_step is None:
                document.status_id = hr_document_status_service.get_by_name(db, HrDocumentStatusEnum.CANCELED.value).id
                db.add(document)
                db.flush()
                return document

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

    async def generate(self, db: Session, id: str, language: LanguageEnum):
        document = self.get_by_id(db, id)
        document_template = hr_document_template_service.get_by_id(
            db, document.hr_document_template_id
        )

        path = document_template.path if language == LanguageEnum.ru else document_template.pathKZ

        if path is None:
            raise BadRequestException(detail=f'Приказа нет на русском языке!')

        temp_file_path = await download_file_to_tempfile(path)

        template = jinja_env.get_template(temp_file_path.replace('/tmp/', ''))

        context = {}

        for i in list(document.properties):
            if isinstance(document.properties[i], dict):
                context[i] = document.properties[i]["name"] if language == LanguageEnum.ru else document.properties[i]["nameKZ"]
            else:
                context[i] = document.properties[i]
        if document.reg_number is not None:
            context["reg_number"] = document.reg_number
        if document.signed_at is not None:
            context["signed_at"] = document.signed_at.strftime("%Y-%m-%d")

        ans = template.render(context)
        
        opts = {
            'encoding': 'UTF-8',
            'enable-local-file-access': True
        }

        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            file_name = temp_file.name + ".pdf"
            pdfkit.from_string(ans, file_name, options=opts, configuration=pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path))

        return FileResponse(
            path=file_name,
            filename=document_template.name + ".pdf",
        )

    def get_all_by_option(
        self,
        db: Session,
        option: str,
        data_taken: str,
        id: uuid.UUID,
        type: str,
        skip: int,
        limit: int
    ):
        service = options.get(option)
        if service is None:
            raise InvalidOperationException(
                f"Работа с {option} еще не поддерживается! Обратитесь к администратору для получения информации!"
            )
        if data_taken is not None and data_taken == "matreshka":
            if id is None:
                return [responses.get(option).from_orm(i) for i in service.get_parents(db, skip, limit)]
            else:
                return [responses.get(option).from_orm(i) for i in service.get_by_id(db, id).children]
        return service.get_by_option(db, type, id, skip, limit)

    def _validate_document(self, db: Session, body: HrDocumentInit, role: str, step: HrDocumentStep):

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

    def _validate_document_for_steps(self, step: HrDocumentStep, all_steps: list, users: list):

        all_steps.remove(step)

        if len(users) != len(all_steps):
            raise BadRequestException(
                detail="Количество пользователей не соответствует количеству шагов!"
            )

    async def _finish_document(self, db: Session, document: HrDocument, users: List[User], current_user_id: uuid.UUID):
        completed_status = hr_document_status_service.get_by_name(db, HrDocumentStatusEnum.COMPLETED.value)
        document.status_id = completed_status.id

        props = document.document_template.properties

        template: HrDocumentTemplate = document.document_template

        properties: dict = document.properties

        for user in users:
            for i in template.actions['args']:
                action_name = list(i)[0]
                action = i[action_name]

                if handlers.get(action_name) is None:
                    raise InvalidOperationException(
                        f"Action {action_name} is not supported!"
                    )

                handlers[action_name].handle_action(db, user, action, props, properties, document)

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
        
        # message = f"{template.name} №{document.reg_number} успешно подписан!"
        # notifiers = hr_document_step_service.get_all_notifiers_by_template_id(db, template.id)

        # notified_users = {}

        # for notifier in notifiers:
        #     staff_units: list[StaffUnit] = notifier.staff_function.staff_units
        #     for i in staff_units:
        #         for j in i.actual_users:
        #             if notified_users.get(j.id) is not None:
        #                 continue
        #             db.add(notification_service.create(db, NotificationCreate(
        #                 message=message,
        #                 sender_id=current_user_id,
        #                 receiver_id=j.id
        #             )))

        #             await notification_manager.broadcast(message, j.id)
        #             notified_users[j.id] = True

        return document

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
                if isinstance(attr, Base):
                    new_val[value["field_name"]] = self._get_service(
                        value["field_name"]
                    ).get(db, value["value"])
                elif isinstance(attr, list):
                    print(value["value"])
                    new_val[value["field_name"]] = self._get_service(
                        value["field_name"]
                    ).get_object(db, value["value"])
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
                        new_val[value["field_name"]] = responses.get(
                            value["field_name"]
                        ).from_orm(self._get_service(value["field_name"]).get(db, val))
                    else:
                        new_val[value["field_name"]] = val
                else:
                    if val["value"] == None:
                        raise BadRequestException(f"Обьект {key} должен иметь value!")
                    obj = self._get_service(value["field_name"]).get_object(db, val["value"])
                    new_val[value["field_name"]] = responses.get(
                        value["field_name"]
                    ).from_orm(obj)

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
