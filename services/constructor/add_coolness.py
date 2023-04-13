from sqlalchemy.orm import Session

from models import User
from .base import BaseHandler
from services import coolness_service, history_service
from exceptions import ForbiddenException


class AddCoolnessHandler(BaseHandler):
    __handler__ = "add_coolness"

    def handle_action(
        self, db: Session, user: User, action: dict, template_props: dict, props: dict
    ):
        tagname = action["coolness"]["tagname"]
        if coolness_service.exists_relation(db, user.id, props[tagname]["value"]):
            raise ForbiddenException(
                f"Coolness is already assigned to this user: {user.first_name}, {user.last_name}"
            )
        res = coolness_service.create_relation(db, user.id, props[tagname]["value"])
        user.coolnesses.append(res)
        history_service.create_history(db, user.id, res)

        db.add(user)
        db.flush()

        return user


handler = AddCoolnessHandler()
