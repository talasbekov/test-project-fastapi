from sqlalchemy.orm import Session

from models import User
from .base import BaseHandler
from services import penalty_service
from exceptions import ForbiddenException


class DeletePenaltyHandler(BaseHandler):
    __handler__ = "delete_penalty"

    def handle_action(
        self, db: Session, user: User, action: dict, template_props: dict, props: dict
    ):
        tagname = action["penalty"]["tagname"]
        if not penalty_service.exists_relation(db, user.id, props[tagname]["value"]):
            raise ForbiddenException(
                f"Penalty is not assigned to this user: {user.first_name}, {user.last_name}"
            )
        res = penalty_service.stop_relation(db, user.id, props[tagname]["value"])


handler = DeletePenaltyHandler()
