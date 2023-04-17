from sqlalchemy.orm import Session

from core import configs
from models import User, HrDocument
from .base import BaseHandler
from services import status_service


class StopStatusHandler(BaseHandler):
    __handler__ = "stop_status"

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
        res = status_service.stop_relation(db, user.id, props[status]["value"])
        res.cancel_document_link = configs.GENERATE_IP + str(document.id)


handler = StopStatusHandler()
