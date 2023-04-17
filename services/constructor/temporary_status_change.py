from sqlalchemy.orm import Session

from core import configs
from models import User, HrDocument
from .base import BaseHandler
from services import status_service, history_service
from exceptions import ForbiddenException
from utils import convert_str_to_datetime


class TemporaryStatusChangeHandler(BaseHandler):
    __handler__ = "temporary_status_change"

    def handle_action(
        self,
        db: Session,
        user: User,
        action: dict,
        template_props: dict,
        props: dict,
        document: HrDocument,
    ):
        status = action["status"]["tagname"]
        date_from = convert_str_to_datetime(action["date_from"]["tagname"])
        date_to = convert_str_to_datetime(action["date_to"]["tagname"])

        res = status_service.create_relation(db, user.id, props[status]["value"])
        history = history_service.create_timeline_history(
            db, user.id, res, date_from, date_to
        )

        history.document_link = configs.GENERATE_IP + str(document.id)
        document.old_history_id = history.id

        db.add(user)
        db.add(res)
        db.add(history)
        db.flush()

        return user


handler = TemporaryStatusChangeHandler()
