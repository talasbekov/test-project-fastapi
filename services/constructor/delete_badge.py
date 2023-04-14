from sqlalchemy.orm import Session

from models import User
from .base import BaseHandler
from services import badge_service, history_service
from exceptions import ForbiddenException


class DeleteBadgeHandler(BaseHandler):
    __handler__ = "delete_badge"

    def handle_action(
        self, db: Session, user: User, action: dict, template_props: dict, props: dict
    ):
        tagname = action["badge"]["tagname"]
        if not badge_service.exists_relation(db, user.id, props[tagname]["value"]):
            raise ForbiddenException(
                f"Badge is not assigned to this user: {user.first_name}, {user.last_name}"
            )
        res = badge_service.stop_relation(db, user.id, props[tagname]["value"])


handler = DeleteBadgeHandler()
