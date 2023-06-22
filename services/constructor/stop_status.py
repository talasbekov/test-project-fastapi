from sqlalchemy.orm import Session

from core import configs
from models import User, HrDocument
from exceptions import BadRequestException
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
        status_id, reason_id = self.get_args(action, props)

        self.handle_validation(
            db, user, action, template_props, props, document)

        res = status_service.stop_relation(db, user.id, status_id)
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
        status_id, _ = self.get_args(action, props)

        status_service.get_by_id(db, status_id)

    def get_args(
            self,
            action: dict,
            props: dict,
    ):
        try:
            status_id = props[action['status']['tagname']]['value']
            reason_id = props[action['reason']['tagname']]['value']
        except Exception:
            raise BadRequestException(
                f"Status is not defined for this action: {self.__handler__}"
            )
        return status_id, reason_id

    def handle_response(self,
                        db: Session,
                        user: User,
                        action: dict,
                        properties: dict,
                        ):
        return None


handler = StopStatusHandler()
