from sqlalchemy.orm import Session

from models import User
from exceptions import ForbiddenException
from services import badge_service, history_service
from .base import BaseHandler


class AddBlackBeretHandler(BaseHandler):
    __handler__ = "add_black_beret"

    def handle_action(
        self, db: Session, user: User, action: dict, template_props: dict, props: dict
    ):
        badge_type = badge_service.get_black_beret(db)
        if badge_service.exists_relation(db, user.id, badge_type.id):
            raise ForbiddenException(
                f"Badge is already assigned to this user: {user.first_name}, {user.last_name}"
            )
        res = badge_service.create_relation(db, user.id, badge_type.id)
        history_service.create_history(db, user.id, res)

        db.add(user)
        db.flush()
        return user


handler = AddBlackBeretHandler()
