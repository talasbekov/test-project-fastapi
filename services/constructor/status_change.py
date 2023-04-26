import datetime

from sqlalchemy.orm import Session

from core import configs
from models import User, HrDocument, StaffDivisionEnum, StaffUnit
from .base import BaseHandler
from services import status_service, history_service, staff_unit_service, staff_division_service
from exceptions import ForbiddenException
from utils import convert_str_to_datetime

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
        status = action["status"]["tagname"]

        self.handle_validation(db, user, action, template_props, props, document)

        if props[status]["name"] in archive_status:
            staff_unit = staff_unit_service.existing_or_create(db, props[status]["name"])
            staff_unit.users.append(user)
            staff_unit.actual_users.append(user)
            user.is_active = False
            db.add(staff_unit)

        res = status_service.create_relation(db, user.id, props[status]["value"])
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
        status = action["status"]["tagname"]

        if status_service.exists_relation(db, user.id, props[status]["value"]):
            raise ForbiddenException(
                f"This status is already assigned to this user: {user.first_name}, {user.last_name}"
            )

handler = StatusChangeHandler()
