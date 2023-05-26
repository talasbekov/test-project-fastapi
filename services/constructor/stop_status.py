from sqlalchemy.orm import Session

from core import configs
from models import User, HrDocument
from exceptions import ForbiddenException
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
        try:
            status = action["status"]["tagname"]
            reason = action["reason"]["tagname"]
        except:
            raise ForbiddenException(
                f"Status is not defined for this action: {self.__handler__}"
            )
        res = status_service.stop_relation(db, user.id, props[status]["value"])
        res.cancel_document_link = configs.GENERATE_IP + str(document.id)

    def handle_validation(
        self,
        db: Session,
        user: User,
        action: dict,
        template_props: dict,
        props: dict,
        document: HrDocument,
    ):
        pass

handler = StopStatusHandler()
