from sqlalchemy.orm import Session

from models import User
from .base import BaseHandler
from services import status_service


class StopStatusHandler(BaseHandler):
    __handler__ = "stop_status"

    def handle_action(
        self, db: Session, user: User, action: dict, template_props: dict, props: dict
    ):
        status = action["status"]["tagname"]
        res = status_service.stop_relation(db, user.id, props[status]["value"])


handler = StopStatusHandler()
