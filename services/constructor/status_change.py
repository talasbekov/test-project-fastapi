from sqlalchemy.orm import Session

from core import configs
from models import User, HrDocument, StaffDivisionEnum
from .base import BaseHandler
from services import status_service, history_service, staff_unit_service
from exceptions import ForbiddenException, BadRequestException

archive_status = [
    StaffDivisionEnum.DEAD,
    StaffDivisionEnum.RETIRED,
    StaffDivisionEnum.IN_RESERVE,
    StaffDivisionEnum.REMOVED_FROM_LIST,
    StaffDivisionEnum.SECONDMENT_OTHER,
    StaffDivisionEnum.PERISHED,
]


class StatusChangeHandler(BaseHandler):
    __handler__ = "status_change"

    def handle_action(
        self,
        db: Session,
        user: User,
        action: dict,
        template_props: dict,
        props: dict,
        document: HrDocument,
    ):
        status_id = self.get_args(action, props)

        self.handle_validation(
            db, user, action, template_props, props, document)

        if status_id in archive_status:
            staff_unit = staff_unit_service.existing_or_create(db, status_id)
            staff_unit.users.append(user)
            staff_unit.actual_users.append(user)
            user.is_active = False
            db.add(staff_unit)

        res = status_service.create_relation(db, user.id, status_id)
        history = history_service.create_history(db, user.id, res)

        history.document_link = configs.GENERATE_IP + str(document.id)

        db.add(user)
        db.add(res)
        db.add(history)
        db.flush()

        return user

    def handle_validation(
        self,
        db: Session,
        user: User,
        action: dict,
        template_props: dict,
        props: dict,
        document: HrDocument,
    ):
        status_id = self.get_args(action, props)

        if status_service.exists_relation(db, user.id, status_id):
            raise ForbiddenException(
                f"This status is already assigned to this user: {user.first_name}, {user.last_name}"
            )

    def get_args(
            self,
            action: dict,
            props: dict,
    ):
        try:
            status_id = props[action['status']['tagname']]['value']
        except Exception as e:
            raise BadRequestException(
                detail=f'Invalid props for action: {self.__handler__}')
        return status_id

    def handle_response(self, db: Session,
                        user: User,
                        action: dict,
                        properties: dict,
                        ):
        status_id = self.get_args(action, properties)
        status = status_service.get_object(db, status_id, 'write')
        return status


handler = StatusChangeHandler()
