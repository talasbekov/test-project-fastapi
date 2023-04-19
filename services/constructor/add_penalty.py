from sqlalchemy.orm import Session

from core import configs
from models import User, HrDocument
from .base import BaseHandler
from services import penalty_service, history_service

from utils import convert_str_to_datetime


class AddPenaltyHandler(BaseHandler):
    __handler__ = "add_penalty"

    def handle_action(
        self,
        db: Session,
        user: User,
        action: dict,
        template_props: dict,
        props: dict,
        document: HrDocument,
    ):
        tagname = action["penalty"]["tagname"]

        res = penalty_service.create_relation(db, user.id, props[tagname]["value"])
        res.name = action["reason"]["tagname"]
        user.penalties.append(res)
        history = history_service.create_history(db, user.id, res)

        history.document_link = configs.GENERATE_IP + str(document.id)
        document.old_history_id = history.id

        db.add(user)
        db.add(history)
        db.add(document)
        db.flush()

        return user


handler = AddPenaltyHandler()
