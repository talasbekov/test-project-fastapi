from sqlalchemy.orm import Session

from core import configs
from models import User, HrDocument
from .base import BaseHandler
from services import status_service, history_service
from exceptions import BadRequestException
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
        status_id, date_from, date_to = self.get_args(db, action, props)

        self.handle_validation(
            db, user, action, template_props, props, document)

        res = status_service.create_relation(db, user.id, status_id)
        history = history_service.create_timeline_history(
            db, user.id, res,
            convert_str_to_datetime(
                props[action['date_from']['tagname']]['name']),
            convert_str_to_datetime(
                props[action['date_to']['tagname']]['name'])
        )

        history.document_link = configs.GENERATE_IP + str(document.id)
        document.old_history_id = history.id

        db.add(user)
        db.add(res)
        db.add(history)
        db.flush()

        return user

    def handle_validation(
        self,
        db: Session,
        user: User,
        action: dict,
        template_props: dict,
        props: dict,
        document: HrDocument,
    ):
        status_id, _, _ = self.get_args(db, action, props)

        status_service.get_by_id(db, status_id)

    def get_args(
            self,
            db: Session,
            action: dict,
            props: dict,
    ):
        try:
            status_id = props[action["status"]["tagname"]]["value"]
            date_from = convert_str_to_datetime(
                props[action['date_from']['tagname']]['name'])
            date_to = convert_str_to_datetime(
                props[action['date_to']['tagname']]['name'])
        except Exception:
            raise BadRequestException(
                f"Status is not defined for this action: {self.__handler__}"
            )
        return status_id, date_from, date_to

    def handle_response(self, db: Session,
                        user: User,
                        action: dict,
                        properties: dict,
                        ):
        status_id, date_from, date_to = self.get_args(db, action, properties)
        status = status_service.get_object(db, status_id, 'write')
        return {status, date_from, date_to}


handler = TemporaryStatusChangeHandler()
