import pdfkit
import qrcode
import hashlib
import random
import tempfile
import json
import requests
import io
import base64
from core import configs
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import pytz

from typing import List, Union, Dict, Any, Optional

from fastapi.encoders import jsonable_encoder
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from sqlalchemy import func, and_

from core import jinja_env, download_file_to_tempfile, wkhtmltopdf_path
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
    HrDocumentUsers,
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
    HrDocumentCreate,
    HrDocumentInit,
    HrDocumentRead,
    HrDocumentSign,
    HrDocumentUpdate,
    RankRead,
    StaffDivisionOptionRead,
    StaffUnitRead,
    DraftHrDocumentCreate,
    BadgeTypeRead,
    StatusTypeRead,
    CoolnessTypeRead,
    PenaltyTypeRead,
    ContractTypeRead,
    ArchiveStaffUnitRead,
    HrDocumentInitEcp,
    HrDocumentSignEcp,
    QrRead,
    NotificationCreate
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
    status_service,
    secondment_service,
    coolness_service,
    penalty_service,
    contract_service,
    archive_staff_unit_service,
    status_leave_service,
    state_body_service,
    categories,
    detailed_notification_service,
    notification_service,
)

from services.history import history_service
from .base import ServiceBase
from .constructor import handlers

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


class HrDocumentService(
        ServiceBase[HrDocument, HrDocumentCreate, HrDocumentUpdate]):

    def create(self, db: Session,
               obj_in: Union[HrDocumentCreate, Dict[str, Any]]) -> HrDocument:
        obj_in_data = jsonable_encoder(obj_in)
        obj_in_data['properties'] = json.dumps(obj_in_data['properties'])
        obj_in_data['initialized_at'] = datetime.now()
        format_string = "%Y-%m-%dT%H:%M:%S.%f%z"
        due_date = obj_in_data.get('due_date', None)
        if due_date is not None:
            obj_in_data['due_date'] = datetime.strptime(obj_in_data['due_date'],
                                                        format_string)

        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.flush()
        return db_obj

    def get_by_id(self, db: Session, id: str) -> HrDocument:
        document = super().get(db, id)
        if document is None:
            raise NotFoundException(detail="Document is not found!")
        return document

    def get_by_id_for_api(self, db: Session, id: str) -> HrDocument:
        document = super().get(db, id)
        if document is None:
            raise NotFoundException(detail="Document is not found!")
        if isinstance(document.properties, str):
            document.properties = json.loads(document.properties)
        if isinstance(document.document_template.properties, str):
            document.document_template.properties = json.loads(
                document.document_template.properties)
        if isinstance(document.document_template.description, str):
            document.document_template.description = json.loads(
                document.document_template.description)
        if isinstance(document.document_template.actions, str):
            document.document_template.actions = json.loads(
                document.document_template.actions)

        return self._to_response(db, document)

    def get_initialized_documents(self,
                                  db: Session,
                                  user_id: str,
                                  parent_id: Optional[str],
                                  filter: str,
                                  skip: int,
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
        for document in documents:
            if isinstance(document.properties, str):
                document.properties = json.loads(document.properties)
            if isinstance(document.document_template.properties, str):
                document.document_template.properties = json.loads(
                    document.document_template.properties)
            if isinstance(document.document_template.description, str):
                document.document_template.description = json.loads(
                    document.document_template.description)
            if isinstance(document.document_template.actions, str):
                document.document_template.actions = json.loads(
                    document.document_template.actions)
        return self._return_correctly(db, documents, user)

    def get_not_signed_documents(
            self,
            db: Session,
            user_id: str,
            parent_id: str,
            filter: str,
            skip: int,
            limit: int
    ):
        user = user_service.get_by_id(db, user_id)

        staff_unit_service.get_by_id(db, user.staff_unit_id)

        draft_status = hr_document_status_service.get_by_name(
            db, HrDocumentStatusEnum.DRAFT.value)
        revision_status = hr_document_status_service.get_by_name(
            db, HrDocumentStatusEnum.ON_REVISION.value)
        documents = (
            db.query(self.model)
            .filter(self.model.status_id != draft_status.id,
                    self.model.status_id != revision_status.id,
                    self.model.parent_id == parent_id)
            .join(self.model.last_step)
            .join(self.model.hr_document_infos)
            .filter(
                HrDocumentInfo.hr_document_step_id == HrDocumentStep.id,
                HrDocumentInfo.assigned_to_id == user_id,
                HrDocumentInfo.is_signed == None)
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
        for document in documents:
            if isinstance(document.properties, str):
                document.properties = json.loads(document.properties)
            if isinstance(document.document_template.properties, str):
                document.document_template.properties = json.loads(
                    document.document_template.properties)
            if isinstance(document.document_template.description, str):
                document.document_template.description = json.loads(
                    document.document_template.description)
            if isinstance(document.document_template.actions, str):
                document.document_template.actions = json.loads(
                    document.document_template.actions)
        return self._return_correctly(db, documents, user)

    def get_signed_documents(
            self,
            db: Session,
            user_id: str,
            parent_id: str,
            filter: str,
            skip: int,
            limit: int
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

    def get_all_documents_of_user(
            self, db: Session, user_id: str, skip: int, limit: int
    ):
        user = user_service.get_by_id(db, user_id)
        print(user_id)
        documents = (
            db.query(self.model)
            .join(self.model.hr_document_infos)
            .filter(
                HrDocumentInfo.signed_by_id == user.id,
                HrDocumentInfo.assigned_to_id == user.id,
            )
        )

        documents = (
            documents
            .order_by(self.model.created_at.asc())
            .offset(skip)
            .limit(limit)
            .all()
        )
        return self._return_correctly(db, documents, user)

    def get_draft_documents(self,
                            db: Session,
                            user_id: str,
                            parent_id: str,
                            filter: str,
                            skip: int = 0,
                            limit: int = 100):
        user = user_service.get_by_id(db, user_id)
        status = hr_document_status_service.get_by_name(
            db, HrDocumentStatusEnum.DRAFT.value)

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

    def save_to_draft(self, db: Session, user_id: str,
                      body: DraftHrDocumentCreate, role: str):
        template = hr_document_template_service.get_by_id(
            db, body.hr_document_template_id
        )

        step: HrDocumentStep = hr_document_step_service.get_initial_step_for_template(
            db, template.id
        )

        self._validate_document(db, body=body, role=role,
                                step=step, users=body.user_ids,
                                user_id=user_id)

        status = hr_document_status_service.get_by_name(
            db, HrDocumentStatusEnum.DRAFT.value)

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

    def initialize_draft_document(self,
                                  db: Session,
                                  body: DraftHrDocumentCreate,
                                  document_id: str,
                                  user_id: str,
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

        step_from_template = (hr_document_template_service
                              .get_steps_by_document_template_id(
                                  db,
                                  document.hr_document_template_id,
                                  current_user.id))

        users = [v for _, v in step_from_template.items()]
        subject_users_ids: List[str] = []

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

        self._validate_document(db, hr_document_init,
                                role=role, step=step, users=subject_users_ids,
                                user_id=user_id)
        self._validate_document_for_steps(
            step=step, all_steps=all_steps, users=users)

        self._create_hr_document_info_for_initiator(
            db, document, current_user, step)
        self._create_hr_document_info_for_all_steps(
            db, document, users, all_steps)

        status = hr_document_status_service.get_by_name(
            db, HrDocumentStatusEnum.IN_PROGRESS.value)

        document.last_step_id = all_steps[0].id
        document.status_id = status.id

        db.add(document)
        db.flush()

        return document

    async def initialize(self,
                         db: Session,
                         body: HrDocumentInit,
                         user_id: str,
                         role: str,
                         parent_id: str = None):
        template = hr_document_template_service.get_by_id(
            db, body.hr_document_template_id
        )

        step: HrDocumentStep = hr_document_step_service.get_initial_step_for_template(
            db, template.id
        )
        all_steps: list = hr_document_step_service.get_all_by_document_template_id(
            db, template.id, False
        )
        notifier_id = body.document_step_users_ids.get('-1', None)
        users = [v for _, v in body.document_step_users_ids.items()]
        if notifier_id:
            users.remove(notifier_id)

        users_in_revision = self._exists_user_document_in_revision(
            db, body.hr_document_template_id, body.user_ids)
        revision_doc = None
        if users_in_revision:
            for user in users_in_revision:
                doc = (db.query(HrDocument)
                       .filter(HrDocument.users.contains(user),
                               HrDocument.hr_document_template_id ==
                               body.hr_document_template_id)
                       .scalar()
                       )

                revision_status = hr_document_status_service.get_by_name(db,
                                                                         'На доработке')
                if doc.status != revision_status:
                    break
                else:
                    revision_doc = doc
        else:
            self._validate_document(db, body=body, role=role,
                                    step=step, users=body.user_ids,
                                    user_id=user_id)
            self._validate_document_for_steps(
                step=step, all_steps=all_steps, users=users)

        current_user = user_service.get_by_id(db, user_id)
        status = hr_document_status_service.get_by_name(
            db, HrDocumentStatusEnum.IN_PROGRESS.value)

        template.properties = json.dumps(
            template.properties, ensure_ascii=False)
        template.description = json.dumps(template.description)
        template.actions = json.dumps(template.actions)

        document: HrDocument = self.create(
            db,
            HrDocumentCreate(
                hr_document_template_id=body.hr_document_template_id,
                status_id=status.id,
                due_date=body.due_date,
                properties=body.properties,
                parent_id=parent_id,
                initial_comment=body.initial_comment,
                initialized_at=datetime.now(),
            ),
        )

        document_info_initiator = self._create_hr_document_info_for_initiator(
            db, document, current_user, step)
        print(2)
        if body.user_ids is not None:
            users_document = [
                user_service.get_by_id(db, user_id) for user_id in body.user_ids
            ]

            props = document.document_template.properties

            template = document.document_template

            properties: dict = document.properties

            if isinstance(template.actions, str):
                document_actions = json.loads(template.actions)
            else:
                document_actions = template.actions
            if isinstance(document.properties, str):
                document_properties = json.loads(document.properties)
            if isinstance(document.document_template.properties, str):
                template_properties = json.loads(
                    document.document_template.properties)

            for user in users_document:
                if isinstance(user.staff_unit.requirements, list):
                    user.staff_unit.requirements = json.dumps(
                        user.staff_unit.requirements)
                for arg in document_actions['args']:
                    action_name = list(arg)[0]
                    action = arg[action_name]

                    if handlers.get(action_name) is None:
                        raise InvalidOperationException(
                            f"Action {action_name} is not supported!"
                        )
                    handlers[action_name].handle_validation(
                        db,
                        user,
                        action,
                        template_properties,
                        document_properties,
                        document
                    )

            document.users = users_document
            if len(all_steps) == 0:
                self._finish_document(db, document, document.users)
        self._create_hr_document_info_for_all_steps(
            db, document, users, all_steps)
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

        if revision_doc:
            super().remove(db, revision_doc.id)

        db.add(document)
        db.commit()
        print(3)
        if notifier_id:
            message = f"{template.name} \n"
            for user in users_document:
                user_name = f"{user.first_name} {user.last_name} "
                message += user_name
            notification_service.create(
                db,
                obj_in=NotificationCreate(
                    message=message,
                    sender_type="Приказ",
                    receiver_id=notifier_id
                )
            )
            message = {
                "sender_type": "Приказ",
                "message": message
            }
            await notification_service.send_message(db, message, notifier_id)

        if isinstance(document.properties, str):
            document.properties = json.loads(document.properties)
        if isinstance(document.document_template.properties, str):
            document.document_template.properties = json.loads(
                document.document_template.properties)
        if isinstance(document.document_template.description, str):
            document.document_template.description = json.loads(
                document.document_template.description)
        if isinstance(document.document_template.actions, str):
            document.document_template.actions = json.loads(
                document.document_template.actions)
        print(3)
        return document

    async def initialize_with_certificate(self,
                                          db: Session,
                                          body: HrDocumentInitEcp,
                                          user_id: str,
                                          role: str,
                                          access_token,
                                          Authorize,
                                          parent_id: str = None,
                                          ):
        document = await self.initialize(
            db,
            HrDocumentInit(
                document_step_users_ids=body.document_step_users_ids,
                user_ids=body.user_ids,
                hr_document_template_id=body.hr_document_template_id,
                due_date=body.due_date,
                parent_id=body.parent_id,
                properties=body.properties,
                initial_comment=body.initial_comment
            ),
            user_id,
            role,
            parent_id
        )

        self._create_notification_for_step(db, document, document.last_step)
        # self._create_notification_for_subject(db, document)
        user = db.query(User).filter(User.id == user_id).first()
        from services import auth_service
        access_token, refresh_token = auth_service._generate_tokens(
            Authorize, user)

        # url = configs.ECP_SERVICE_URL + 'api/hr_document_step_signer/create/template/'
        # request_body = {
        #     'hr_document_template_id': str(body.hr_document_template_id),
        #     'hr_document_id': str(document.id),
        #     'user_id': user_id,
        #     'certificate_blob': body.certificate_blob
        # }

        # headers = {"Authorization": f"Bearer {access_token}"}

        # res = requests.post(url=url, json=request_body,
        #                     headers=headers, verify=False)
        # if res.status_code == 400:
        #     raise BadRequestException(detail=res.text)

        template = document.hr_document_template_id
        step: HrDocumentStep = hr_document_step_service.get_initial_step_for_template(
            db, template
        )

        # url = configs.ECP_SERVICE_URL+'api/hr_document_step_signer/create/'
        # request_body = {
        #     'hr_document_id': str(document.id),
        #     'user_id': str(user_id),
        #     'step_id': str(step.id),
        #     'certificate_blob': body.certificate_blob
        # }

        # headers = {"Authorization": f"Bearer {access_token}"}

        # res = requests.post(url=url, json=request_body,
        #                     headers=headers, verify=False)

        # if res.status_code == 400:
        #     raise BadRequestException(detail=res.text)

        return document

    def sign_with_certificate(
            self,
            db: Session,
            document_id: str,
            body: HrDocumentSignEcp,
            user_id: str,
            access_token,
    ):
        step = self.get_by_id(db, document_id).last_step_id
        print("wtf")
        document = self.sign(
            db,
            document_id,
            HrDocumentSign(
                comment=body.comment,
                is_signed=body.is_signed
            ),
            user_id
        )
        # self._create_notification_for_subject(db, document.id)
        # url = configs.ECP_SERVICE_URL+'api/hr_document_step_signer/create/'
        # request_body = {
        #     'hr_document_template_signer_id': str(document.hr_document_template_id),
        #     'hr_document_id': str(document.id),
        #     'user_id': str(user_id),
        #     'step_id': str(step),
        #     'certificate_blob': body.certificate_blob
        # }
        # headers = {"Authorization": f"Bearer {access_token}"}

        # res = requests.post(url=url, json=request_body,
        #                     headers=headers, verify=False)

        # if res.status_code == 400:
        #     raise BadRequestException(detail=res.text)

        return document

    def sign(
            self,
            db: Session,
            document_id: str,
            body: HrDocumentSign,
            user_id: str,
    ):
        print("7")
        document = self.get_by_id(db, document_id)
        self._validate_document_for_completed(db, document)
        current_user = user_service.get_by_id(db, user_id)
        info = hr_document_info_service.get_by_document_id_and_step_id(
            db, document_id, document.last_step_id)
        self._validate_document_for_user_step(info, current_user)
        step: HrDocumentStep = hr_document_step_service.get_initial_step_for_template(
            db, document.hr_document_template_id)
        document_staff_function = document_staff_function_service.get_by_id(
            db, step.staff_function_id)
        print("77")
        if document_staff_function.role.name == DocumentFunctionTypeEnum.EXPERT.value:
            body.is_signed = True
        hr_document_info_service.sign(
            db, info, current_user, body.comment, body.is_signed)
        next_step = self._set_next_step(db, document_id, info)
        if self._is_superdoc(db, document):
            return self._sign_super_document(db,
                                             document,
                                             next_step,
                                             body.is_signed,
                                             body.comment,
                                             info,
                                             current_user)
        if body.is_signed:
            if next_step is None:
                detailed_notification_service.remove_document_notification(
                    db,
                    str(document.id),
                    str(user_id)
                )
                return self._finish_document(db, document, document.users)
            document.last_step_id = next_step.id
            query = db.execute(text(f"SELECT id \
                                      FROM HR_ERP_HR_DOCUMENT_STATUSES \
                                      WHERE name = \
                                      '{HrDocumentStatusEnum.IN_PROGRESS.value}'"))
            document.status_id = query.fetchone()[0]
        else:
            if next_step is None:
                detailed_notification_service.remove_document_notification(
                    db,
                    document.id,
                    user_id)
                return self._cancel_document(db, document)

            steps = (
                hr_document_step_service
                .get_all_by_document_template_id_without_notifiers(
                    db,
                    document.hr_document_template_id)
            )

            self._create_info_for_document_steps(db, document, steps)
            print("777")
            document.last_step = steps[0]
            document.status_id = hr_document_status_service.get_by_name(
                db, HrDocumentStatusEnum.ON_REVISION.value).id
        if isinstance(document.properties, dict):
            document.properties = json.dumps(
                document.properties, ensure_ascii=False)
        if isinstance(document.document_template.properties, dict):
            document.document_template.properties = json.dumps(
                document.document_template.properties)
        if isinstance(document.document_template.description, dict):
            document.document_template.description = json.dumps(
                document.document_template.description)
        if isinstance(document.document_template.actions, dict):
            document.document_template.actions = json.dumps(
                document.document_template.actions)
        print("blah blah")
        db.add(document)
        db.commit()

        detailed_notification_service.remove_document_notification(
            db,
            str(document.id),
            str(user_id)
        )
        print("blah blah blah")
        self._create_notification_for_step(db, document, document.last_step)
        # self._create_notification_for_subject(db, document.id)

        return document
    
    def get_subject(self, db: Session, document_id: str):
        subject = db.query(HrDocumentUsers).filter(HrDocumentUsers.document_id == document_id).first()
        return subject   
        # document = db.query(HrDocument).filter(HrDocument.id == document_id).first()
        # if document:
        #     return document.subject_id
        # return None
    

    def _create_notification_for_subject(self, db: Session, document_id: str):
        subject = self.get_subject(db, document_id)
        print("Subjeeeeeect: ", subject)
        detailed_notification = detailed_notification_service.create(
            db,
            {
                "hr_document_id": document_id,
                "receiver_id": subject.subject_id
            }
        )

    async def generate_html(self, db: Session, id: str, language: LanguageEnum):
        ans, name = await self._get_html(db, id, language)

        # Write and to tempfile and return it
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
            'page-size': 'A4',
            'dpi': 300,
            'encoding': 'UTF-8',
            'enable-local-file-access': True,
            'margin-top': '2.54cm',
            'margin-right': '1.5cm',
            'margin-bottom': '0.94cm',
            'margin-left': '2.54cm',
        }

        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            file_name = temp_file.name + ".pdf"
            pdfkit.from_string(ans, file_name, options=opts,
                               configuration=pdfkit.configuration
                               (wkhtmltopdf=wkhtmltopdf_path))

        return FileResponse(
            path=file_name,
            filename=name + ".pdf",
        )

    def get_all_by_option(
            self,
            db: Session,
            option: str,
            data_taken: str,
            id: str,
            type: str,
            skip: int,
            limit: int
    ):
        service = options.get(option)
        if service is None:
            raise InvalidOperationException(
                (f"Работа с {option} еще не поддерживается! "
                 f"Обратитесь к администратору для получения информации!")
            )
        return service.get_by_option(db, type, id, skip, limit)

    def _create_staff_unit_document_body(self,
                                         db: Session,
                                         user_id: str,
                                         staff_unit: ArchiveStaffUnit,
                                         template_id: str,
                                         parent_id: str):
        steps = hr_document_template_service.get_steps_by_document_template_id(
            db, template_id)
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

    def _validate_document(self,
                           db: Session,
                           body: HrDocumentInit,
                           role: str,
                           step: HrDocumentStep,
                           users: List[str],
                           user_id: str = None):

        staff_unit: StaffUnit = staff_unit_service.get_by_id(db, role)

        staff_units = staff_unit_service.get_all(db, users)

        if step.is_direct_supervisor is not None:
            # if staff_unit.staff_division.leader_id != staff_unit.id:
            #     raise ForbiddenException(
            #         detail='Вы не можете инициализировать этот документ!'
            #    )
            if step.is_direct_supervisor:
                for staff_unit in staff_units:
                    if staff_unit.staff_division_id != staff_unit.staff_division_id:
                        raise ForbiddenException(
                            detail='Вы не можете инициализировать этот документ!'
                        )

        elif step.category is not None:
            category = categories.get(step.category)
            if category is None:
                raise InvalidOperationException(
                    "Категория не поддерживается!"
                )
            if not category.validate(db, user_id):
                raise ForbiddenException(
                    detail='Вы не можете инициализировать этот документ!'
                )

        elif not staff_unit_service.has_staff_function(db,
                                                       staff_unit.id,
                                                       step.staff_function_id):
            raise ForbiddenException(
                detail=(
                    "Вы не можете инициализировать "
                    "этот документ из-за отсутствия прав!"
                )
            )

        forbidden_users = self._exists_user_document_in_progress(
            db, body.hr_document_template_id, users)

        if forbidden_users:
            user_info_list = list(
                map(lambda user: (f"{user.first_name}"
                                  f" {user.last_name}"
                                  f" {user.father_name}"),
                    forbidden_users)
            )
            raise ForbiddenException(
                detail=(
                    "Вы не можете инициализировать этот документ, для пользователей:"
                    f"{user_info_list} "
                    f"так как они уже имеют аналогичный документ в процессе"
                )
            )

        document_staff_function = (document_staff_function_service
                                   .get_by_id(db, step.staff_function_id))

        if not self._check_jurisdiction(
                db, staff_unit, document_staff_function, body.user_ids):
            raise ForbiddenException(
                detail="Вы не можете инициализировать этот документ из-за юрисдикции!"
            )

    def _validate_document_for_steps(
            self, step: HrDocumentStep, all_steps: list, users: list):

        all_steps.remove(step)

        if len(users) != len(all_steps):
            raise BadRequestException(
                detail="Количество пользователей не соответствует количеству шагов!"
            )

    def _exists_user_document_in_progress(
            self,
            db: Session,
            hr_document_template_id: str,
            user_ids: List[str]):

        if user_ids is None:
            return None

        forbidden_statuses = hr_document_status_service.get_by_names(
            db, ["Завершен", "Отменен"])

        return (
            db.query(User)
            .distinct(User.id)
            .join(HrDocument.users)
            .join(HrDocumentInfo, HrDocument.id == HrDocumentInfo.hr_document_id)
            .filter(HrDocument.hr_document_template_id == hr_document_template_id,
                    User.id.in_(user_ids),
                    HrDocumentInfo.signed_by_id.is_(None),
                    and_(*[HrDocument.status_id !=
                           status.id for status in forbidden_statuses])
                    )
            .all()
        )

    def _exists_user_document_in_revision(
            self,
            db: Session,
            hr_document_template_id: str,
            user_ids: List[str]):

        if user_ids is None:
            return None

        revision_status = hr_document_status_service.get_by_name(
            db, "На доработке")

        return (
            db.query(User)
            .distinct(User.id)
            .join(HrDocument.users)
            .join(HrDocumentInfo, HrDocument.id == HrDocumentInfo.hr_document_id)
            .filter(HrDocument.hr_document_template_id == hr_document_template_id,
                    User.id.in_(user_ids),
                    HrDocumentInfo.signed_by_id.is_(None),
                    HrDocument.status_id == revision_status.id)
            .all()
        )

    def _finish_document(self,
                         db: Session,
                         document: HrDocument,
                         users: List[User]):

        completed_status = hr_document_status_service.get_by_name(
            db, HrDocumentStatusEnum.COMPLETED.value)
        document.status_id = completed_status.id

        template_properties = document.document_template.properties

        template: HrDocumentTemplate = document.document_template

        document_properties: dict = document.properties

        if isinstance(document.document_template.actions, dict):
            document.document_template.actions = json.dumps(template.actions)
        if isinstance(document.document_template.properties, dict):
            document.document_template.properties = json.dumps(
                template.properties)
        if isinstance(document.document_template.description, dict):
            document.document_template.description = json.dumps(
                template.description)

        if isinstance(document.properties, str):
            document_actions = json.loads(template.actions)
        if isinstance(document.properties, str):
            document_properties = json.loads(document.properties)
        if isinstance(document.document_template.properties, str):
            template_properties = json.loads(
                document.document_template.properties)

        document.reg_number = (
            "11"
            + "-"
            + str(random.randint(1, 10000))
            + "")
        for user in users:
            for arg in document_actions['args']:
                action_name = list(arg)[0]
                action = arg[action_name]
                if handlers.get(action_name) is None:
                    raise InvalidOperationException(
                        f"Action {action_name} is not supported!"
                    )
                handlers[action_name].handle_action(
                    db,
                    user,
                    action,
                    template_properties,
                    document_properties,
                    document)

        document.signed_at = datetime.now()
        document.last_step_id = None

        if isinstance(document.document_template.actions, dict):
            document.document_template.actions = json.dumps(template.actions)
        if isinstance(document.document_template.properties, dict):
            document.document_template.properties = json.dumps(
                template.properties)
        if isinstance(document.document_template.description, dict):
            document.document_template.description = json.dumps(
                template.description)
        
        db.add(document)
        db.flush()
        self._create_notification_for_subject(db, document.id)
        return document

    def _sign_super_document(self,
                             db: Session,
                             super_document: HrDocument,
                             super_document_next_step: HrDocumentStep,
                             is_signed: bool,
                             comment: str,
                             user: User):
        child_documents = db.query(self.model).filter(
            self.model.parent_id == super_document.id
        ).all()

        completed_status = hr_document_status_service.get_by_name(
            db, HrDocumentStatusEnum.COMPLETED.value)

        if is_signed:
            if super_document_next_step is None:
                return self._finish_super_document(db, super_document)

            in_progress_status = hr_document_status_service.get_by_name(
                db, HrDocumentStatusEnum.IN_PROGRESS.value)

            super_document.status_id = in_progress_status.id
            super_document.last_step_id = super_document_next_step.id
        else:
            if super_document_next_step is None:
                canceled_status = hr_document_status_service.get_by_name(
                    db, HrDocumentStatusEnum.CANCELED.value)

                super_document.status_id = canceled_status.id
                super_document.last_step_id = None
            else:
                steps = (
                    hr_document_step_service
                    .get_all_by_document_template_id_without_notifiers(
                        db, super_document.hr_document_template_id
                    ))

                self._create_info_for_document_steps(db, super_document, steps)

                super_document.last_step = steps[0]

                on_revision_status = hr_document_status_service.get_by_name(
                    db, HrDocumentStatusEnum.ON_REVISION.value)

                super_document.status_id = on_revision_status.id

        for child_document in child_documents:
            if (child_document.last_step is None
                    and child_document.status_id is completed_status.id):
                raise InvalidOperationException(
                    detail=f'Document with id {child_document.id} is already signed!')

            child_document_info = (
                hr_document_info_service
                .get_by_document_id_and_step_id(
                    db,
                    child_document.id,
                    child_document.last_step_id
                ))

            hr_document_info_service.sign(
                db, child_document_info, user, comment, is_signed)

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
                    child_steps = (
                        hr_document_step_service
                        .get_all_by_document_template_id_without_notifiers(
                            db, child_document.hr_document_template_id
                        ))
                    self._create_info_for_document_steps(
                        db, child_document, child_steps)

                    child_document.last_step = child_steps[0]

                    child_document.status_id = on_revision_status.id

        db.add_all(child_documents)
        db.add(super_document)
        db.flush()
        return super_document

    def _finish_super_document(self, db: Session, super_document: HrDocument):
        completed_status = hr_document_status_service.get_by_name(
            db, HrDocumentStatusEnum.COMPLETED.value)

        documents = db.query(self.model).filter(
            self.model.parent_id == super_document.id
        ).all()

        super_template: HrDocumentTemplate = super_document.document_template

        for arg in super_template.actions['args']:
            action_name = list(arg)[0]
            action = arg[action_name]

            if handlers.get(action_name) is None:
                raise InvalidOperationException(
                    f"Action {action_name} is not supported!"
                )
            if super_document.users is not None and len(
                    super_document.users) > 0:
                for user in super_document.users:
                    handlers[action_name].handle_action(
                        db,
                        user,
                        action,
                        super_template.properties,
                        super_document.properties,
                        super_document)
            else:
                handlers[action_name].handle_action(
                    db,
                    None,
                    action,
                    super_template.properties,
                    super_document.properties,
                    super_document)

        for document in documents:
            document.status_id = completed_status.id

            props = document.document_template.properties

            template: HrDocumentTemplate = document.document_template

            properties: dict = document.properties

            for user in document.users:
                for arg in template.actions['args']:
                    action_name = list(arg)[0]
                    action = arg[action_name]

                    if handlers.get(action_name) is None:
                        raise InvalidOperationException(
                            f"Action {action_name} is not supported!"
                        )

                    handlers[action_name].handle_action(
                        db, user, action, props, properties, document)

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

    def generate_qrs(self, db: Session, hr_document_id: str):
        qrs = []
        query = text(
            "SELECT HR_ERP_HR_DOCUMENT_STEP_SIGNER.user_id, hr_erp_hr_document_step_signer.step_id, \
        hr_erp_hr_document_step_signer.certificate_blob, \
        hr_erp_hr_document_step_signer.created_at \
        FROM HR_ERP_HR_DOCUMENT_STEP_SIGNER \
        JOIN HR_ERP_HR_DOC_TEMPLATE_SIGNER \
        ON hr_erp_hr_document_step_signer.hr_document_template_signer_id = HR_ERP_HR_DOC_TEMPLATE_SIGNER.ID \
        WHERE HR_ERP_HR_DOC_TEMPLATE_SIGNER.hr_document_id = :hr_document_id ORDER BY hr_erp_hr_document_step_signer.created_at")
        certificates = db.execute(
            query, {"hr_document_id": str(hr_document_id)}).fetchall()

        for certificate in certificates:
            (
                user_id,
                step_id,
                certificate_blob,
                signed_at
            ) = certificate

            step = hr_document_step_service.get_by_id(db, step_id)
            user = user_service.get_by_id(db, user_id)
            hash_algorithm = hashlib.sha256()
            hash_algorithm.update(certificate_blob.encode('utf-8'))
            hashed_value = hash_algorithm.hexdigest()

            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L
            )

            qr.add_data(hashed_value)
            img = qr.make_image(fill_color="black", back_color="white")
            buffer = io.BytesIO()
            img.save(buffer, format="PNG")

            qr_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

            buffer.close()

            qrs.append(QrRead(
                step=step,
                user=user,
                qr_base64=qr_base64,
                signed_at=signed_at
            ))

        return qrs

    def _get_service(self, key):
        service = options.get(key)
        if service is None:
            raise InvalidOperationException(
                f"New state is encountered! Cannot change {key}!"
            )
        return service

    # TODO
    def _to_response(self, db: Session,
                     document: HrDocument) -> HrDocumentRead:
        response = HrDocumentRead.from_orm(document)
        if document.last_step_id is not None:
            response.can_cancel = document.last_step.staff_function.role.can_cancel

        new_val = []

        properties = document.properties
        actions = document.document_template.actions['args']
        if document.status_id == hr_document_status_service.get_by_name(
                db, HrDocumentStatusEnum.DRAFT.value).id:
            new_val.append(properties)
        else:
            for action in actions:
                for action_name in list(action.keys()):
                    new_val.append({
                        f'{action_name}': handlers[action_name].handle_response(
                            db,
                            document.users[0],
                            action[action_name],
                            properties)
                    }
                    )
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

    def _check_for_department(
            self, db: Session, user: User, subject: User) -> bool:
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
        hr_documents = []
        for document in documents:
            if document is None:
                continue
            if document.id not in s:
                if isinstance(document.properties, str):
                    document.properties = json.loads(document.properties)
                if isinstance(document.document_template.properties, str):
                    document.document_template.properties = json.loads(
                        document.document_template.properties)
                if isinstance(document.document_template.description, str):
                    document.document_template.description = json.loads(
                        document.document_template.description)
                if isinstance(document.document_template.actions, str):
                    document.document_template.actions = json.loads(
                        document.document_template.actions)
                s.add(document.id)
                if len(document.users) > 0:
                    # for user in document.users:
                    #     if user.staff_unit.user_replacing:
                    #         requirements = (user
                    #                         .staff_unit.user_replacing
                    #                         .staff_unit
                    #                         .requirements)
                    #         staff_division_description = (user
                    #                                       .staff_unit.user_replacing
                    #                                       .staff_unit
                    #                                       .staff_division
                    #                                       .description)
                    #         if isinstance(requirements, str):
                    #             (user
                    #              .staff_unit.user_replacing
                    #              .staff_unit
                    #              .requirements) = json.loads(requirements)
                    #         if isinstance(requirements, str):
                    #             (user
                    #              .staff_unit.user_replacing
                    #              .staff_unit
                    #              .staff_division
                    #              .description) = json.loads(staff_division_description)
                    hr_documents.append(self._to_response(db, document))
                else:
                    hr_documents.append(
                        self._to_response_super_doc(db, document))
        return hr_documents

    def _check_jurisdiction(
            self,
            db: Session,
            staff_unit: StaffUnit,
            document_staff_function: DocumentStaffFunction,
            subject_user_ids: List[str]
    ) -> bool:
        jurisdiction = jurisdiction_service.get_by_id(
            db, document_staff_function.jurisdiction_id)

        # Проверка на вид юрисдикции "Вся служба"
        if jurisdiction.name == JurisdictionEnum.ALL_SERVICE.value:
            return True

        staff_division = staff_division_service.get_by_id(
            db, staff_unit.staff_division_id)

        # Проверка на вид юрисдикции "Боевое подразделение"
        if jurisdiction.name == JurisdictionEnum.COMBAT_UNIT.value:
            return staff_division.is_combat_unit

        # Проверка на вид юрисдикции "Штатное подразделение"
        if jurisdiction.name == JurisdictionEnum.STAFF_UNIT.value:
            return not staff_division.is_combat_unit

        subject_users: List[User] = []

        for user_id in subject_user_ids:
            subject_users.append(user_service.get_by_id(db, user_id))

        # Проверка на вид юрисдикции "Личное дело"
        if jurisdiction.name == JurisdictionEnum.PERSONNEL.value:
            self._check_personnel_jurisdiction(db,
                                               staff_unit=staff_unit,
                                               staff_division=staff_division,
                                               subject_users=subject_users)

        # Проверка на вид юрисдикции Курируемые сотрудники
        if jurisdiction.name == JurisdictionEnum.SUPERVISED_EMPLOYEES.value:
            self._check_supervised_jurisdiction(subject_users=subject_users)

        # Проверка на вид юрисдикции Кандидаты
        if jurisdiction.name == JurisdictionEnum.CANDIDATES.value:
            self._check_candidates_jurisdiction(
                db, subject_users=subject_users)

        return False

    def _check_personnel_jurisdiction(
            self,
            db: Session,
            staff_unit: StaffUnit,
            staff_division: StaffDivision,
            subject_users: List[User]) -> bool:
        # Получаем все дочерние штатные группы пользователя, включая саму
        # группу
        staff_divisions: List[StaffDivision] = (
            staff_division_service.get_all_child_groups(
                db, staff_unit.staff_division_id
            )
        )
        staff_divisions.append(staff_division)

        # Получаем все staff unit из staff divisions
        staff_units: List[StaffUnit] = []
        for staff_division in staff_divisions:
            staff_units.extend(
                staff_unit_service.get_by_staff_division_id(db, staff_division.id))

        # Проверка субъекта на присутствие в штатной единице
        # Метод возвращает True если все из субъектов относятся к штатной единице
        # Если один из субъектов не относится к штатной единице то метод
        # выбрасывает False
        for user in subject_users:
            if user.staff_unit not in staff_units:
                return False

        return True

    def _check_supervised_jurisdiction(
            self, subject_users: List[User]) -> bool:
        for user in subject_users:
            if user.supervised_by is None:
                return False

        return True

    def _check_candidates_jurisdiction(
            self, db: Session, subject_users: List[User]):
        staff_units: List[StaffUnit] = []
        for user in subject_users:
            staff_units.append(user.staff_unit)

        candidates_staff_division = staff_division_service.get_by_name(
            db, StaffDivisionEnum.CANDIDATES.value)

        for staff_unit in staff_units:
            if not staff_unit.staff_division_id == candidates_staff_division.id:
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
                user_service.get_by_id(db, user_id)
                for user_id in update_data['user_ids']
            ]
            hr_document.users = users_document
        hr_document.updated_at = datetime.now()
        db.add(hr_document)
        db.flush()
        return hr_document

    def get_signee(self, db: Session, id: str) -> User:
        document = self.get_by_id(db, id)
        if (document.status.name
                != HrDocumentStatusEnum.COMPLETED.value):
            raise ForbiddenException('Документ не завершен')
        steps = hr_document_step_service.get_all_by_document_template_id(
            db, document.hr_document_template_id)
        if len(steps) < 3:
            raise ForbiddenException('Документ не завершен')
        last_step = steps[len(steps) - 1]
        info = hr_document_info_service.get_by_document_id_and_step_id(
            db, id, last_step.id)
        return info.signed_by

    def _create_hr_document_info_for_all_steps(
            self,
            db: Session,
            document: HrDocument,
            users: List[User],
            all_steps: List[HrDocumentStep]):
        for step, user_id in zip(all_steps, users):
            # if step.is_direct_supervisor is not None:
            #     if not isinstance(user_id, dict):
            #         print(step.id)
            #         print("anime")
            #         print(user_id)
            #         raise InvalidOperationException(
            #             f"User id must be dict for step {step.id}"
            #         )
            #     for i in sorted(user_id.keys()):
            #         hr_document_info_service.create_info_for_step(
            #             db, document.id, step.id, user_id[i], None, None, None
            #         )
            #     continue
            hr_document_info_service.create_info_for_step(
                db, document.id, step.id, user_id, None, None, None
            )

    def _create_hr_document_info_for_initiator(
            self,
            db: Session,
            document: HrDocument,
            current_user: User,
            step: HrDocumentStep):

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
            template = hr_document_template_service.get_by_id(
                db, document.hr_document_template_id)
            for arg in template.actions['args']:
                actions = list(arg)
                if "superdoc" in actions:
                    superdoc = True
        return superdoc

    def _validate_document_for_completed(self, db, document):
        completed_status: HrDocumentStatus = hr_document_status_service.get_by_name(
            db, HrDocumentStatusEnum.COMPLETED.value)

        if document.last_step is None \
                and document.status_id is completed_status.id:
            raise InvalidOperationException(
                detail='Document is already signed!')

    def _validate_document_for_user_step(self, info, current_user):
        if info.assigned_to_id != current_user.id:
            raise ForbiddenException(
                detail=f"User {current_user.first_name} is not assigned to this step!"
            )

    def _cancel_document(self, db: Session, document: HrDocument):
        template: HrDocumentTemplate = document.document_template
        if isinstance(template.actions, str):
            document_actions = json.loads(template.actions)
        if isinstance(document.properties, str):
            document_properties = json.loads(document.properties)
        if isinstance(document.document_template.properties, str):
            template_properties = json.loads(
                document.document_template.properties)
        document.status_id = hr_document_status_service.get_by_name(
            db, HrDocumentStatusEnum.CANCELED.value).id
        document.last_step = None

        if isinstance(document.document_template.actions, dict):
            document.document_template.actions = json.dumps(template.actions)
        if isinstance(document.document_template.properties, dict):
            document.document_template.properties = json.dumps(
                template.properties)
        if isinstance(document.document_template.description, dict):
            document.document_template.description = json.dumps(
                template.description)
        db.add(document)
        db.flush()
        return document

    def _set_next_step(self, db: Session, document_id: str,
                       info: HrDocumentInfo):
        try:
            next_step = hr_document_info_service.get_by_document_id_and_step_id(
                db, document_id, info.hr_document_step.id).hr_document_step
        except SgoErpException:
            next_step = hr_document_step_service.get_next_step_from_previous_step(
                db, info.hr_document_step
            )
        return next_step

    def _create_info_for_document_steps(
            self, db: Session, document: HrDocument, steps):
        for step in steps:
            had_step = False
            count = 1
            while True:
                try:
                    signed_info = (
                        hr_document_info_service
                        .get_signed_by_document_id_and_step_id(
                            db,
                            document.id,
                            step.id,
                            count
                        )
                    )
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

    async def _get_html(self, db: Session, id: str, language: LanguageEnum):
        document = self.get_by_id(db, str(id))
        if isinstance(document.properties, str):
            document.properties = json.loads(document.properties)
        if isinstance(document.document_template.properties, str):
            document.document_template.properties = json.loads(
                document.document_template.properties)
        if isinstance(document.document_template.description, str):
            document.document_template.description = json.loads(
                document.document_template.description)
        if isinstance(document.document_template.actions, str):
            document.document_template.actions = json.loads(
                document.document_template.actions)
        document_template = hr_document_template_service.get_by_id(
            db, document.hr_document_template_id
        )

        path = (document_template.path
                if language == LanguageEnum.ru
                else document_template.pathKZ)

        if path is None:
            raise BadRequestException(detail='Приказа нет на русском языке!')

        temp_file_path = await download_file_to_tempfile(path)
        try:
            template = jinja_env.get_template(
                temp_file_path.replace('/tmp/', ''))

            context = {}

            for prop in list(document.properties):
                if isinstance(document.properties[prop], dict):
                    context[prop] = (document.properties[prop]["name"]
                                     if language == LanguageEnum.ru
                                     else document.properties[prop]["nameKZ"])
                else:
                    context[prop] = document.properties[prop]
            if document.reg_number is not None:
                context["reg_number"] = document.reg_number
            if document.signed_at is not None:
                context["signed_at"] = document.signed_at.strftime("%Y-%m-%d")
        except Exception as e:
            raise BadRequestException(detail=f'Ошибка в шаблоне!{e}')
        last_step = hr_document_step_service.get_last_step_document_template_id(
            db, document.hr_document_template_id)

        last_info = hr_document_info_service.find_by_document_id_and_step_id_signed(
            db, document.id, last_step.id)

        if last_info is not None and last_info.signed_at is not None:
            context['approving_rank'] = last_info.signed_by.rank.name
            context['approving_name'] = (
                f"{last_info.signed_by.first_name} "
                f"{last_info.signed_by.last_name} {last_info.signed_by.father_name}"
            )
        return template.render(context), document_template.name

    def _create_notification_for_step(
        self,
        db: Session,
        document: HrDocument,
        step: Optional[HrDocumentStep]
    ):
        if step is None:
            pass
        info = hr_document_info_service.find_by_document_id_and_step_id(
            db,
            document.id,
            step.id
        )

        detailed_notification = detailed_notification_service.create(
            db,
            {
                "hr_document_id": document.id,
                "receiver_id": info.assigned_to_id
            }
        )
    async def generate_document_for_expiring(self, db: Session, contract_id: str, role: str, properties: dict, years: int):
        expiring_contracts = history_service.get_expiring_contracts(db)
        for contract in expiring_contracts:
            if contract.contract_id == contract_id:
                user_id = contract.user_id
          
                staff_division = user_service.get_by_id(db, user_id).staff_unit.staff_division
                leader_id = user_service.get_leader_id(db, staff_division.id)
                pgs = "dfd0a5ec-a23a-47af-8f1c-fb5e4813f570" # for testing Kozenko's id, change later!!!
                print(user_id)
                print(leader_id)
                due_date = datetime.now(pytz.timezone('Etc/GMT-6')) + relativedelta(years=years)
                new_document = HrDocumentInit(
                    hr_document_template_id="073121d7-87dd-4d72-b4d8-272acdce9d53",
                    user_ids=[user_id],
                    document_step_users_ids={100:pgs},
                    parent_id=None,
                    due_date = due_date,
                    properties=properties
                )
     
                document = await self.initialize(db, new_document, user_id, role)
           
                return document
        return None
    
    async def send_expiring_notification(self, db: Session, user_id: str, contract_id):
        sender_type = "Приказ"
        message = f'Уважаемый сотрудник, у вас истекает срок действия договора №{contract_id}'

        # check if the notification has already been created for this user
        if not notification_service.notification_exists(db, user_id, sender_type):
            notification_service.create(
                db,
                obj_in=NotificationCreate(
                    message=message,
                    sender_type=sender_type,
                    receiver_id=user_id
                )
            )
            message_to_notifier = {
                "sender_type": str(sender_type),
                "message": message
            }
            await notification_service.send_message(db, message_to_notifier, user_id)
            return "Success"
        else:
            return "Уведомление уже было отправлено!"


hr_document_service = HrDocumentService(HrDocument)
