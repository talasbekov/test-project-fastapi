from sqlalchemy.orm import Session

from models import User
from .base import BaseHandler
from services import status_service, history_service
from exceptions import ForbiddenException
from utils import convert_str_to_datetime


class StatusChangeHandler(BaseHandler):
    __handler__ = "status_change"

    def handle_action(
        self, db: Session, user: User, action: dict, template_props: dict, props: dict
    ):
        status = action["status"]["tagname"]

        if status_service.exists_relation(db, user.id, props[status]["value"]):
            raise ForbiddenException(
                f"This status is already assigned to this user: {user.first_name}, {user.last_name}"
            )

        res = status_service.create_relation(db, user.id, props[status]["value"])
        history_service.create_history(db, user.id, res)

        db.add(user)
        db.flush()

        return user


handler = StatusChangeHandler()
