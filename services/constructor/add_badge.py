from sqlalchemy.orm import Session

from models import User
from .base import BaseHandler
from services import badge_service, history_service
from exceptions import ForbiddenException


class AddBadgeHandler(BaseHandler):
    __handler__ = "add_badge"

    def handle_action(
        self, db: Session, user: User, action: dict, template_props: dict, props: dict
    ):
        tagname = action["badge"]["tagname"]
        if badge_service.exists_relation(db, user.id, props[tagname]["value"]):
            raise ForbiddenException(
                f"Badge is already assigned to this user: {user.first_name}, {user.last_name}"
            )
        res = badge_service.create_relation(db, user.id, props[tagname]["value"])
        user.badges.append(res)
        history_service.create_history(db, user.id, res)

        db.add(user)
        db.flush()

        return user


handler = AddBadgeHandler()
