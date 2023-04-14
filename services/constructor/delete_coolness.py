from sqlalchemy.orm import Session

from models import User
from .base import BaseHandler
from services import coolness_service
from exceptions import ForbiddenException


class DeleteCoolnessHandler(BaseHandler):
    __handler__ = "delete_coolness"

    def handle_action(
        self, db: Session, user: User, action: dict, template_props: dict, props: dict
    ):
        tagname = action["coolness"]["tagname"]
        if not coolness_service.exists_relation(db, user.id, props[tagname]["value"]):
            raise ForbiddenException(
                f"Coolness is not assigned to this user: {user.first_name}, {user.last_name}"
            )
        res = coolness_service.stop_relation(db, user.id, props[tagname]["value"])


handler = DeleteCoolnessHandler()
