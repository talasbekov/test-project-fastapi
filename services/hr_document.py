import pdfkit
import random
import tempfile
import uuid
from datetime import datetime, timedelta
from typing import List

from fastapi.encoders import jsonable_encoder
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy import func, and_

from core import Base, jinja_env, download_file_to_tempfile, wkhtmltopdf_path
from exceptions import (
    BadRequestException,
    ForbiddenException,
    InvalidOperationException,
    NotFoundException,
    SgoErpException,
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
    ArchiveStaffUnit,
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
    ArchiveStaffUnitRead,
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
    staff_list_service,
    archive_staff_unit_service,
    status_leave_service,
    state_body_service,
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
    'archive_staff_unit': archive_staff_unit_service,
    'status_leave': status_leave_service,
    'state_body': state_body_service,
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
    'archive_staff_unit': ArchiveStaffUnitRead,
}

from .constructor import handlers


class HrDocumentService(ServiceBase[HrDocument, HrDocumentCreate, HrDocumentUpdate]):
    def get_by_id(self, db: Session, id: str) -> HrDocument:
        document = super().get(db, id)
        if document is None:
            raise NotFoundException(detail="Document is not found!")
        return document

    def get_initialized_documents(self, db: Session, user_id: uuid.UUID, parent_id: uuid.UUID, filter: str, skip: int,
                                  limit: int):
        user = user_service.get_by_id(db, user_id)
        documents = (
            db.query(self.model)
            .join(self.model.hr_document_infos)
            .join(HrDocumentStep)
            .join(DocumentStaffFunction)
            .filter(
                HrDocumentInfo.assigned_to_id == user_id,
                DocumentStaffFunction.priority == 1,
                self.model.parent_id == parent_id,
            )
        )

        if filter != '':
            documents = self._add_filter_to_query(documents, filter)

        documents = (
            documents
            .order_by(self.model.initialized_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        return self._return_correctly(db, documents, user)

    def get_not_signed_documents(
            self, db: Session, user_id: str, parent_id: uuid.UUID, filter: str, skip: int, limit: int
    ):
        user = user_service.get_by_id(db, user_id)

        staff_unit_service.get_by_id(db, user.actual_staff_unit_id)

        draft_status = hr_document_status_service.get_by_name(db, HrDocumentStatusEnum.DRAFT.value)
        revision_status = hr_document_status_service.get_by_name(db, HrDocumentStatusEnum.ON_REVISION.value)
        documents = (
            db.query(self.model)
            .filter(self.model.status_id != draft_status.id,
                    self.model.status_id != revision_status.id,
                    self.model.parent_id == parent_id)
            .join(HrDocumentStep)
            .join(HrDocumentInfo, and_(HrDocumentInfo.hr_document_step_id == HrDocumentStep.id,
                                       HrDocumentInfo.assigned_to_id == user_id, HrDocumentInfo.signed_by_id == None))
        )

        if filter != '':
            documents = self._add_filter_to_query(documents, filter)

        documents = (
            documents
            .order_by(self.model.initialized_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        return self._return_correctly(db, documents, user)

    def get_signed_documents(
            self, db: Session, user_id: str, parent_id: uuid.UUID, filter: str, skip: int, limit: int
    ):
        user = user_service.get_by_id(db, user_id)
        documents = (
            db.query(self.model)
            .join(self.model.hr_document_infos)
            .filter(
                HrDocumentInfo.signed_by_id == user_id,
                self.model.parent_id == parent_id,
            )
        )

        if filter != '':
            documents = self._add_filter_to_query(documents, filter)

        documents = (
            documents
            .order_by(self.model.initialized_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        return self._return_correctly(db, documents, user)

    def get_all_documents(
            self, db: Session, user_id: str, filter: str, skip: int, limit: int
    ):
        user = user_service.get_by_id(db, user_id)
        documents = (
            db.query(self.model)
            .join(self.model.hr_document_infos)
            .join(self.model.users)
            .filter(
                User.id == user_id,
            )
        )

        if filter != '':
            documents = self._add_filter_to_query(documents, filter)

        documents = (
            documents
            .order_by(self.model.created_at.asc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        return self._return_correctly(db, documents, user)

    def get_draft_documents(self, db: Session, user_id: str, parent_id: uuid.UUID, filter: str, skip: int = 0,
                            limit: int = 100):
        user = user_service.get_by_id(db, user_id)
        status = hr_document_status_service.get_by_name(db, HrDocumentStatusEnum.DRAFT.value)

        documents = (
            db.query(self.model)
            .filter(
                self.model.status_id == status.id,
                self.model.initialized_by_id == user_id,
                self.model.parent_id == parent_id,
            ))

        if filter != '':
            documents = self._add_filter_to_query(documents, filter)

        documents = (
            documents
            .order_by(self.model.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )


        return self._return_correctly(db, documents, user)

    def save_to_draft(self, db: Session, user_id: str, body: DraftHrDocumentCreate, role: str):
        template = hr_document_template_service.get_by_id(
            db, body.hr_document_template_id
        )

        step: HrDocumentStep = hr_document_step_service.get_initial_step_for_template(
            db, template.id
        )

        self._validate_document(db, body=body, role=role, step=step, users=body.user_ids)

        status = hr_document_status_service.get_by_name(db, HrDocumentStatusEnum.DRAFT.value)

        document: HrDocument = super().create(
            db,
            HrDocumentCreate(
                hr_document_template_id=body.hr_document_template_id,
                status_id=status.id,
                due_date=body.due_date,
                properties=body.properties,
                parent_id=None,
                initial_comment=body.initial_comment,
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

    def initialize_draft_document(self, db: Session, body: DraftHrDocumentCreate, document_id: str, user_id: str,
                                  role: str):
        document = hr_document_service.get_by_id(db, document_id)

        template = hr_document_template_service.get_by_id(
            db, document.hr_document_template_id
        )

        step: HrDocumentStep = hr_document_step_service.get_initial_step_for_template(
            db, template.id
        )

        all_steps = hr_document_step_service.get_all_by_document_template_id(
            db, template.id
        )

        current_user = user_service.get_by_id(db, user_id)

        step_from_template = hr_document_template_service.get_steps_by_document_template_id(db,
                                                                                            document.hr_document_template_id,
                                                                                            current_user.id)

        users = [v for _, v in step_from_template.items()]
        subject_users_ids: List[uuid.UUID] = []

        for user in body.user_ids:
            subject_users_ids.append(user)

        hr_document_init = HrDocumentInit(
            properties=body.properties,
            due_date=body.due_date,
            hr_document_template_id=document.hr_document_template_id,
            user_ids=body.user_ids,
            document_step_users_ids=step_from_template,
            initial_comment=body.initial_comment,
            initialized_at=datetime.now(),
        )

        self._validate_document(db, hr_document_init, role=role, step=step, users=subject_users_ids)
        self._validate_document_for_steps(step=step, all_steps=all_steps, users=users)

        self._create_hr_document_info_for_initiator(db, document, current_user, step)
        self._create_hr_document_info_for_all_steps(db, document, users, all_steps)

        status = hr_document_status_service.get_by_name(db, HrDocumentStatusEnum.IN_PROGRESS.value)

        document.last_step_id = all_steps[0].id
        document.status_id = status.id

        db.add(document)
        db.flush()

        return document

    async def initialize(self, db: Session, body: HrDocumentInit, user_id: str, role: str, parent_id: uuid.UUID = None):
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

        self._validate_document(db, body=body, role=role, step=step, users=body.user_ids)
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
                parent_id=parent_id,
                initial_commit=body.initial_comment,
                initialized_at=datetime.now(),
            ),
        )

        document_info_initiator = self._create_hr_document_info_for_initiator(db, document, current_user, step)

        if body.user_ids is not None:
            users_document = [
                user_service.get_by_id(db, user_id) for user_id in body.user_ids
            ]

            props = document.document_template.properties

            template = document.document_template

            properties: dict = document.properties

            for user in users_document:
                for i in template.actions['args']:
                    action_name = list(i)[0]
                    action = i[action_name]

                    if handlers.get(action_name) is None:
                        raise InvalidOperationException(
                            f"Action {action_name} is not supported!"
                        )

                    handlers[action_name].handle_validation(db, user, action, props, properties, document)

            document.users = users_document

            if len(all_steps) == 0:
                await self._finish_document(db, document, document.users)

        self._create_hr_document_info_for_all_steps(db, document, users, all_steps)

        if len(all_steps) == 0:
            document.last_step_id = None
        else:
            document.last_step_id = all_steps[0].id

        if body.parent_id is not None:
            parent = self.get_by_id(db, body.parent_id)

            document.parent_id = parent.id

            hr_document_info_service.sign(
                db, document_info_initiator, current_user, None, True
            )

        db.add(document)
        db.flush()
        return document

    async def sign(
            self,
            db: Session,
            document_id: str,
            body: HrDocumentSign,
            user_id: str,
    ):
        document = self.get_by_id(db, document_id)
        self._validate_document_for_completed(db, document)

        current_user = user_service.get_by_id(db, user_id)
        info = hr_document_info_service.get_by_document_id_and_step_id(db, document_id, document.last_step_id)
        self._validate_document_for_user_step(info, current_user)

        step: HrDocumentStep = hr_document_step_service.get_initial_step_for_template(db, document.hr_document_template_id)
        document_staff_function = document_staff_function_service.get_by_id(db, step.staff_function_id)

        if document_staff_function.role.name == DocumentFunctionTypeEnum.EXPERT.value:
            body.is_signed = True

        hr_document_info_service.sign(db, info, current_user, body.comment, body.is_signed)

        next_step = self._set_next_step(db, document_id, info)

        if self._is_superdoc(db, document):
            return await self._sign_super_document(db, document, next_step, body.is_signed, body.comment, info, current_user)

        if body.is_signed:
            if next_step is None:
                return await self._finish_document(db, document, document.users)

            document.last_step_id = next_step.id
            document.status_id = hr_document_status_service.get_by_name(db, HrDocumentStatusEnum.IN_PROGRESS.value).id
        else:
            if next_step is None:
                return self._cancel_document(db, document)

            steps = hr_document_step_service.get_all_by_document_template_id_without_notifiers(db, document.hr_document_template_id)
            self._create_info_for_document_steps(db, document, steps)

            document.last_step = steps[0]
            document.status_id = hr_document_status_service.get_by_name(db, HrDocumentStatusEnum.ON_REVISION.value).id

        db.add(document)
        db.flush()

        return document

    async def generate_html(self, db: Session, id: str, language: LanguageEnum):
        ans, name = await self._get_html(db, id, language)

        # Write ans to tempfile and return it
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            file_name = temp_file.name
            temp_file.write(ans.encode("utf-8"))
            return FileResponse(
                path=file_name,
                filename=name + ".html",
            )

    async def generate(self, db: Session, id: str, language: LanguageEnum):
        ans, name = await self._get_html(db, id, language)

        opts = {
            'encoding': 'UTF-8',
            'enable-local-file-access': True
        }

        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            file_name = temp_file.name + ".pdf"
            pdfkit.from_string(ans, file_name, options=opts,
                               configuration=pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path))

        return FileResponse(
            path=file_name,
            filename=name + ".pdf",
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
        return service.get_by_option(db, type, id, skip, limit)

    def _create_staff_unit_document_body(self, db: Session, user_id: uuid.UUID, staff_unit: ArchiveStaffUnit,
                                         template_id: uuid.UUID, parent_id: uuid.UUID):
        steps = hr_document_template_service.get_steps_by_document_template_id(db, template_id)
        body = HrDocumentInit(
            hr_document_template_id=template_id,
            user_ids=[user_id],
            document_step_users_ids=steps,
            parent_id=parent_id,
            due_date=datetime.now() + timedelta(days=7),
            properties={
                'staff_unit': {
                    'name': staff_unit.position.name,
                    'nameKZ': staff_unit.position.nameKZ,
                    'value': staff_unit.id,
                    'field_name': "archive_staff_unit"
                }
            }
        )
        return body

    def _validate_document(self, db: Session, body: HrDocumentInit, role: str, step: HrDocumentStep,
                           users: List[uuid.UUID]):

        staff_unit: StaffUnit = staff_unit_service.get_by_id(db, role)

        staff_units = staff_unit_service.get_all(db, users)

        if step.is_direct_supervisor is not None:
            if staff_unit.staff_division.leader_id != staff_unit.id:
                raise ForbiddenException(
                    detail='Вы не можете инициализировать этот документ!'
                )
            if step.is_direct_supervisor:
                for i in staff_units:
                    if i.staff_division_id != staff_unit.staff_division_id:
                        raise ForbiddenException(
                            detail='Вы не можете инициализировать этот документ!'
                        )
        elif not staff_unit_service.has_staff_function(db, staff_unit.id, step.staff_function_id):
            raise ForbiddenException(
                detail=f"Вы не можете инициализировать этот документ из-за отсутствия прав!"
            )

        forbidden_users = self._exists_user_document_in_progress(db, body.hr_document_template_id, users)

        if forbidden_users:
            user_info_list = list(
                map(lambda user: f"{user.first_name} {user.last_name} {user.father_name}", forbidden_users))
            raise ForbiddenException(
                detail=f"Вы не можете инициализировать этот документ, для пользователей:{user_info_list} так как они уже имеют аналогичный документ в процессе"
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

    def _exists_user_document_in_progress(self, db: Session, hr_document_template_id: uuid.UUID,
                                          user_ids: List[uuid.UUID]):

        if user_ids is None:
            return None

        forbidden_statuses = hr_document_status_service.get_by_names(db, ["Завершен", "Отменен"])

        return (
            db.query(User)
            .distinct(User.id)
            .join(HrDocument.users)
            .join(HrDocumentInfo, HrDocument.id == HrDocumentInfo.hr_document_id)
            .filter(HrDocument.hr_document_template_id == hr_document_template_id,
                    User.id.in_(user_ids),
                    HrDocumentInfo.signed_by_id.is_(None),
                    and_(*[HrDocument.status_id != status.id for status in forbidden_statuses])
                    )
            .all()
        )

    async def _finish_document(self, db: Session, document: HrDocument, users: List[User]):
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
                "11"
                + "-"
                + str(random.randint(1, 10000))
                + "ДСП/ЛС-ЭС"
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

    async def initialize_super_document(self, db: Session, staff_list_id: uuid.UUID, user_id: str, role: str):
        template = hr_document_template_service.get_staff_list(db)
        child_template = hr_document_template_service.get_staff_unit(db)
        body: HrDocumentInit = HrDocumentInit(
            hr_document_template_id=template.id,
            user_ids=[],
            parent_id=None,
            due_date=datetime.now() + timedelta(days=7),
            document_step_users_ids=hr_document_template_service.get_steps_by_document_template_id(db, template.id,
                                                                                                   user_id=user_id),
            properties={
                'staff_list': {
                    'name': 'staff_list',
                    'nameKZ': "Штатный список",
                    'value': str(staff_list_id)
                },
            },
        )
        document = await self.initialize(db, body, user_id, role)
        staff_list = staff_list_service.get_by_id(db, staff_list_id)
        staff_list.is_signed = True
        for archive_staff_division in staff_list.archive_staff_divisions:
            for archive_staff_unit in archive_staff_division.staff_units:
                if not staff_unit_service.exists_relation(db, archive_staff_unit.user_id, archive_staff_unit.origin_id):
                    if archive_staff_unit.user_id is not None:
                        child_body = self._create_staff_unit_document_body(db, archive_staff_unit.user_id,
                                                                           archive_staff_unit, child_template.id,
                                                                           document.id)
                        await self.initialize(db, child_body, user_id, role, parent_id=document.id)
        return document

    async def _sign_super_document(self,
                                   db: Session,
                                   super_document: HrDocument,
                                   super_document_next_step: HrDocumentStep,
                                   is_signed: bool,
                                   comment: str,
                                   super_document_info: HrDocumentInfo,
                                   user: User):
        child_documents = db.query(self.model).filter(
            self.model.parent_id == super_document.id
        ).all()

        completed_status = hr_document_status_service.get_by_name(db, HrDocumentStatusEnum.COMPLETED.value)

        if is_signed:
            if super_document_next_step is None:
                return await self._finish_super_document(db, super_document)

            in_progress_status = hr_document_status_service.get_by_name(db, HrDocumentStatusEnum.IN_PROGRESS.value)

            super_document.status_id = in_progress_status.id
            super_document.last_step_id = super_document_next_step.id
        else:
            if super_document_next_step is None:
                canceled_status = hr_document_status_service.get_by_name(db, HrDocumentStatusEnum.CANCELED.value)

                super_document.status_id = canceled_status.id
                super_document.last_step_id = None
            else:
                steps = hr_document_step_service.get_all_by_document_template_id_without_notifiers(
                    db, super_document.hr_document_template_id
                )

                self._create_info_for_document_steps(db, super_document, steps)

                super_document.last_step = steps[0]

                on_revision_status = hr_document_status_service.get_by_name(db, HrDocumentStatusEnum.ON_REVISION.value)

                super_document.status_id = on_revision_status.id


        for child_document in child_documents:
            if child_document.last_step is None and child_document.status_id is completed_status.id:
                raise InvalidOperationException(detail=f'Document with id {child_document.id} is already signed!')

            child_document_info = hr_document_info_service.get_by_document_id_and_step_id(
                db, child_document.id, child_document.last_step_id
            )

            hr_document_info_service.sign(db, child_document_info, user, comment, is_signed)

            if is_signed:
                next_step = hr_document_step_service.get_next_step_from_previous_step(
                    db, child_document_info.hr_document_step
                )
                child_document.last_step_id = next_step.id
                child_document.status_id = in_progress_status.id
            else:
                if super_document_next_step is None:
                    child_document.status_id = canceled_status.id
                    child_document.last_step = None
                else:
                    child_steps = hr_document_step_service.get_all_by_document_template_id_without_notifiers(
                        db, child_document.hr_document_template_id
                    )
                    self._create_info_for_document_steps(db, child_document, child_steps)

                    child_document.last_step = child_steps[0]

                    child_document.status_id = on_revision_status.id

        db.add_all(child_documents)
        db.add(super_document)
        db.flush()
        return super_document

    async def _finish_super_document(self, db: Session, super_document: HrDocument):
        completed_status = hr_document_status_service.get_by_name(db, HrDocumentStatusEnum.COMPLETED.value)


        documents = db.query(self.model).filter(
            self.model.parent_id == super_document.id
        ).all()

        super_template: HrDocumentTemplate = super_document.document_template

        for i in super_template.actions['args']:
            action_name = list(i)[0]
            action = i[action_name]

            if handlers.get(action_name) is None:
                raise InvalidOperationException(
                    f"Action {action_name} is not supported!"
                )
            if super_document.users is not None and len(super_document.users) > 0:
                for user in super_document.users:
                    handlers[action_name].handle_action(db, user, action, super_template.properties,
                                                        super_document.properties, super_document)
            else:
                handlers[action_name].handle_action(db, None, action, super_template.properties,
                                                    super_document.properties, super_document)

        for document in documents:
            document.status_id = completed_status.id

            props = document.document_template.properties

            template: HrDocumentTemplate = document.document_template

            properties: dict = document.properties

            for user in document.users:
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

            document.status_id = completed_status.id
            document.last_step_id = None

        super_document.signed_at = datetime.now()
        super_document.reg_number = (
                str(random.randint(1, 10000))
                + "-"
                + str(random.randint(1, 10000))
                + "қбп/жқ"
        )

        super_document.status_id = completed_status.id
        super_document.last_step_id = None

        db.add_all(documents)
        db.add(super_document)
        db.flush()

        return super_document

    def _get_service(self, key):
        service = options.get(key)
        if service is None:
            raise InvalidOperationException(
                f"New state is encountered! Cannot change {key}!"
            )
        return service

    # TODO
    def _to_response(self, db: Session, document: HrDocument) -> HrDocumentRead:
        response = HrDocumentRead.from_orm(document)
        if document.last_step_id is not None:
            response.can_cancel = document.last_step.staff_function.role.can_cancel

        new_val = []

        properties = document.properties
        actions = document.document_template.actions['args']

        for action in actions:
            for action_name in list(action.keys()):
                new_val.append({f'{action_name}': handlers[action_name].handle_response(db, action[action_name],
                                                                                        properties)})

        response.new_value = new_val

        return response


    def _to_response_super_doc(self, db: Session, document: HrDocument):
        response = HrDocumentRead.from_orm(document)
        if document.last_step_id is not None:
            response.can_cancel = document.last_step.staff_function.role.can_cancel


        count_child_documents = db.query(self.model).filter(
            self.model.parent_id == document.id
        ).count()


        response.new_value = {"count": count_child_documents}


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
                if len(i.users) > 0:
                    subject = i.users[0]
                    if self._check_for_department(db, user, subject):
                        l.append(self._to_response(db, i))
                else:
                    l.append(self._to_response_super_doc(db, i))

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
            self._check_personnel_jurisdiction(db, staff_unit=staff_unit, staff_division=staff_division,
                                               subject_users=subject_users)

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

    def _add_filter_to_query(self, document_query, filter):
        key_words = filter.lower().split()
        documents = (
            document_query
            .join(self.model.users)
            .join(self.model.document_template)
            .filter(and_(func.concat(func.lower(User.first_name), ' ',
                                     func.lower(User.last_name), ' ',
                                     func.lower(User.father_name), ' ',
                                     func.lower(HrDocumentTemplate.name), ' ',
                                     func.lower(HrDocumentTemplate.nameKZ)
                                     ).contains(name) for name in key_words)
                    )
        )
        return documents

    def update_document(
            self,
            db: Session,
            hr_document: HrDocument,
            hr_document_update: HrDocumentUpdate
    ) -> HrDocument:
        document_data = jsonable_encoder(hr_document)
        if isinstance(hr_document_update, dict):
            update_data = hr_document_update
        else:
            update_data = hr_document_update.dict(exclude_unset=True)
        for field in document_data:
            if field in update_data:
                setattr(hr_document, field, update_data[field])
        if update_data['user_ids'] and update_data['user_ids'] != []:
            users_document = [
                user_service.get_by_id(db, user_id) for user_id in update_data['user_ids']
            ]
            hr_document.users = users_document
        hr_document.updated_at = datetime.now()
        db.add(hr_document)
        db.flush()
        return hr_document

    def get_signee(self, db: Session, id: uuid.UUID) -> User:
        document = self.get_by_id(db, id)
        if document.status.name != HrDocumentStatusEnum.COMPLETED.value:
            raise ForbiddenException('Документ не завершен')
        steps = hr_document_step_service.get_all_by_document_template_id(db, document.hr_document_template_id)
        if len(steps) < 3:
            raise ForbiddenException('Документ не завершен')
        last_step = steps[len(steps) - 1]
        info = hr_document_info_service.get_by_document_id_and_step_id(db, id, last_step.id)
        return info.signed_by

    def _create_hr_document_info_for_all_steps(self, db: Session, document: HrDocument, users: List[User], all_steps: List[HrDocumentStep]):
        for step, user_id in zip(all_steps, users):
            if step.is_direct_supervisor is not None:
                if not isinstance(user_id, dict):
                    raise InvalidOperationException(
                        f"User id must be dict for step {step.id}"
                    )
                for i in sorted(user_id.keys()):
                    hr_document_info_service.create_info_for_step(
                        db, document.id, step.id, user_id[i], None, None, None
                    )
                continue
            hr_document_info_service.create_info_for_step(
                db, document.id, step.id, user_id, None, None, None
            )

    def _create_hr_document_info_for_initiator(self, db: Session, document: HrDocument, current_user: User, step: HrDocumentStep):
        document_info_initiator = hr_document_info_service.create_info_for_step(
            db, document.id, step.id, current_user.id, True, None,
            datetime.now()
        )

        hr_document_info_service.sign(
            db, document_info_initiator, current_user, document.initial_comment, True
        )


        return document_info_initiator

    def _is_superdoc(self, db: Session, document):
        superdoc = False

        if document.parent_id is None:
            template = hr_document_template_service.get_by_id(db, document.hr_document_template_id)
            for i in template.actions['args']:
                actions = list(i)
                if "superdoc" in actions:
                    superdoc = True
        return superdoc

    def _validate_document_for_completed(self, db, document):
        completed_status: HrDocumentStatus = hr_document_status_service.get_by_name(db, HrDocumentStatusEnum.COMPLETED.value)

        if document.last_step is None\
           and document.status_id is completed_status.id:
            raise InvalidOperationException(detail=f'Document is already signed!')

    def _validate_document_for_user_step(self, info, current_user):
        if info.assigned_to_id != current_user.id:
            raise ForbiddenException(
                detail=f"User {current_user.first_name} is not assigned to this step!"
            )

    def _cancel_document(self, db: Session, document: HrDocument):
        document.status_id = hr_document_status_service.get_by_name(db, HrDocumentStatusEnum.CANCELED.value).id
        document.last_step = None
        db.add(document)
        db.flush()
        return document

    def _set_next_step(self, db: Session, document_id: str, info: HrDocumentInfo):
        try:
            next_step = hr_document_info_service.get_by_document_id_and_step_id(db, document_id, info.hr_document_step.id).hr_document_step
        except SgoErpException:
            next_step = hr_document_step_service.get_next_step_from_previous_step(
                db, info.hr_document_step
            )
        return next_step

    def _create_info_for_document_steps(self, db: Session, document: HrDocument, steps):
        for step in steps:
            had_step = False
            count = 1
            while True:
                try:
                    signed_info = hr_document_info_service.get_signed_by_document_id_and_step_id(
                        db, document.id, step.id, count)
                    had_step = True
                    hr_document_info_service.create_info_for_step(
                        db, document.id, step.id,
                        signed_info.assigned_to_id, None, None, None,
                        signed_info.order
                    )

                    count += 1
                except SgoErpException:
                    break
            if not had_step:
                break

    async def _get_html(self, db: Session, id: uuid.UUID, language: LanguageEnum):
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

        last_step = hr_document_step_service.get_last_step_document_template_id(db, document.hr_document_template_id)

        last_info = hr_document_info_service.find_by_document_id_and_step_id(db, document.id, last_step.id)

        if last_info is not None and last_info.signed_at is not None:
            context['approving_rank'] = last_info.signed_by.rank.name
            context['approving_name'] = f"{last_info.signed_by.name} {last_info.signed_by.last_name} {last_info.signed_by.father_name}"

        return template.render(context), document_template.name


hr_document_service = HrDocumentService(HrDocument)
