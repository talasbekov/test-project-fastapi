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
        status = action["staff_unit"]["tagname"]

        if staff_unit_service.exists_relation(db, user.id, props[status]["value"]):
            raise ForbiddenException(
                f"This position is already assigned to this user: {user.first_name}, {user.last_name}"
            )
        res = staff_unit_service.create_relation(db, user, props[status]["value"])
        history = history_service.create_history(db, user.id, res)

        history.document_link = configs.GENERATE_IP + str(document.id)
        document.old_history_id = history.id

        db.add(user)
        db.add(history)
        db.add(document)

        db.flush()

        return user


handler = PositionChangeHandler()
