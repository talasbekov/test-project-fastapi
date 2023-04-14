from sqlalchemy.orm import Session

from core import configs
from models import User, HrDocument
from .base import BaseHandler
from services import secondment_service, history_service
from utils import convert_str_to_datetime


class AddSecondmentHandler(BaseHandler):
    __handler__ = "add_secondment"

    def handle_action(
        self,
        db: Session,
        user: User,
        action: dict,
        template_props: dict,
        props: dict,
        document: HrDocument,
    ):
        tagname = action["secondment"]["tagname"]

        date_from = convert_str_to_datetime(action["date_from"]["tagname"])
        date_to = convert_str_to_datetime(action["date_to"]["tagname"])

        res = secondment_service.create_relation(db, user.id, props[tagname]["value"])
        history = history_service.create_timeline_history(
            db, user.id, res, date_from, date_to
        )

        history.document_link = configs.GENERATE_IP + document.id
        document.old_history_id = history.id

        db.add(user)
        db.add(history)
        db.add(document)
        db.flush()

        return user


handler = AddSecondmentHandler()
