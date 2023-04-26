from sqlalchemy.orm import Session

from core import configs
from models import User, HrDocument
from .base import BaseHandler
from services import staff_unit_service, history_service, user_service
from exceptions import ForbiddenException
from utils import convert_str_to_datetime


class PositionChangeHandler(BaseHandler):
    __handler__ = "position_change"

    def handle_action(
        self,
        db: Session,
        user: User,
        action: dict,
        template_props: dict,
        props: dict,
        document: HrDocument,
    ):
        position = action["staff_unit"]["tagname"]

        self.handle_validation(db, user, action, template_props, props, document)
        old_history = staff_unit_service.get_last_history(db, user.id)
        if old_history is not None:
            document.old_history_id = old_history.id

        res = staff_unit_service.create_relation(db, user, props[position]["value"])
        history = history_service.create_history(db, user.id, res)

        history.document_link = configs.GENERATE_IP + str(document.id)

        db.add(user)
        db.add(history)
        db.add(document)

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
        position = action["staff_unit"]["tagname"]

        if staff_unit_service.exists_relation(db, user.id, props[position]["value"]):
            raise ForbiddenException(
                f"This position is already assigned to this user: {user.first_name}, {user.last_name}"
            )

handler = PositionChangeHandler()
