from sqlalchemy.orm import Session

from core import configs
from models import User, HrDocument, StatusEnum
from services import status_service, history_service
from exceptions import ForbiddenException
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
        date_from, date_to = self.get_args(props, action)
        type = status_service.get_by_name(db, StatusEnum.SICK_LEAVE.value)

        res = status_service.create_relation(db, user.id, type.id)
        history = history_service.create_timeline_history(db, user.id, res, date_from, date_to)

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
        date_from, date_to = self.get_args(props, action)
        if date_to < date_from:
            raise ForbiddenException(detail=f'Invalid props for action: {self.__handler__}')

    def get_args(
        self,
        props: dict,
        action: dict
    ):
        try:
            date_from = convert_str_to_datetime(props[action['date_from']['tagname']]['name'])
            date_to = convert_str_to_datetime(props[action['date_to']['tagname']]['name'])
        except:
            raise ForbiddenException(detail=f'Invalid props for action: {self.__handler__}')
        return (date_from, date_to)


handler = SickLeaveHandler()
