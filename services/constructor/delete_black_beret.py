from sqlalchemy.orm import Session

from models import User
from .base import BaseHandler
from services import badge_service
from exceptions import ForbiddenException


class DeleteBlackBeretHandler(BaseHandler):
    __handler__ = "delete_black_beret"

    def handle_action(
        self, db: Session, user: User, action: dict, template_props: dict, props: dict
    ):
        tagname = action["black_beret"]["tagname"]
        if not badge_service.get_black_beret_by_user_id(db, user.id) is None:
            raise ForbiddenException(
                f"Black Beret is not assigned to this user: {user.first_name}, {user.last_name}"
            )
        res = badge_service.stop_relation(db, user.id, props[tagname]["value"])


handler = DeleteBlackBeretHandler()
