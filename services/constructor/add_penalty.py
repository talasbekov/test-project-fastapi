from sqlalchemy.orm import Session

from models import User
from .base import BaseHandler
from services import penalty_service, history_service

from utils import convert_str_to_datetime


class AddPenaltyHandler(BaseHandler):
    __handler__ = "add_penalty"

    def handle_action(
        self, db: Session, user: User, action: dict, template_props: dict, props: dict
    ):
        tagname = action["penalty"]["tagname"]

        res = penalty_service.create_relation(db, user.id, props[tagname]["value"])
        res.name = action["reason"]["tagname"]
        user.penalties.append(res)
        history_service.create_history(db, user.id, res)

        db.add(user)
        db.flush()

        return user


handler = AddPenaltyHandler()
