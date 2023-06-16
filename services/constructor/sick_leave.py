from sqlalchemy.orm import Session

from core import configs
from models import User, HrDocument, StatusEnum
from services import status_service, history_service
from exceptions import BadRequestException
from utils import convert_str_to_datetime
from .base import BaseHandler


class SickLeaveHandler(BaseHandler):
    __handler__ = "sick_leave"

    def handle_action(
            self,
            db: Session,
            user: User,
            action: dict,
            template_props: dict,
            props: dict,
            document: HrDocument,
    ):
        date_from, date_to = self.get_args(action, props)
        type = status_service.get_by_name(
            db, StatusEnum.SICK_LEAVE.value)[0]

        self.handle_validation(
            db, user, action, template_props, props, document)

        res = status_service.create_relation(db, user.id, type.id)
        history = history_service.create_timeline_history(
            db, user.id, res, date_from, date_to)

        history.document_link = configs.GENERATE_IP + str(document.id)
        document.old_history_id = history.id

        db.add(user)
        db.add(res)
        db.add(history)
        db.flush()

    def handle_validation(
        self,
        db: Session,
        user: User,
        action: dict,
        template_props: dict,
        props: dict,
        document: HrDocument,
    ):
        date_from, date_to = self.get_args(action, props)
        if date_to < date_from:
            raise BadRequestException(
                detail=f'Invalid props for action: {self.__handler__}')

    def get_args(
            self,
            action: dict,
            props: dict
    ):
        try:
            date_from = convert_str_to_datetime(
                props[action['date_from']['tagname']]['name'])
            date_to = convert_str_to_datetime(
                props[action['date_to']['tagname']]['name'])
        except Exception:
            raise BadRequestException(
                detail=f'Invalid props for action: {self.__handler__}')
        return date_from, date_to

    def handle_response(self, db: Session,
                        user: User,
                        action: dict,
                        properties: dict,
                        ):
        date_range = list(self.get_args(action, properties))
        return date_range


handler = SickLeaveHandler()
