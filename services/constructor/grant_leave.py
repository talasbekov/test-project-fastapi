import logging

from sqlalchemy.orm import Session

from core import configs
from models import User, HrDocument, StatusEnum
from services import status_service, history_service
from exceptions import ForbiddenException, BadRequestException
from utils import convert_str_to_datetime
from .base import BaseHandler


class GrantLeaveHandler(BaseHandler):
    __handler__ = "grant_leave"

    def handle_action(
            self,
            db: Session,
            user: User,
            action: dict,
            template_props: dict,
            props: dict,
            document: HrDocument,
    ):
        self.handle_validation(
            db, user, action, template_props, props, document)
        status_id, date_from, date_to = self.get_args(action, props)

        res = status_service.create_relation(db, user.id, status_id)
        history = history_service.create_timeline_history(
            db, user.id, res, date_from, date_to)

        history.document_link = configs.GENERATE_IP + str(document.id)
        history.document_number = document.reg_number
        document.old_history_id = history.id
        history.document_number = document.reg_number
        status = status_service.get_object(db, status_id, 'write')
        history.status_name = status.name

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
        status_id, date_from, date_to = self.get_args(action, props)
        if status_service.get_object(db, status_id, 'write') is None:
            raise ForbiddenException(
                detail=f'Invalid status_id for action: {self.__handler__}')
        if date_to < date_from:
            raise ForbiddenException(
                detail=f'Invalid dates for action: {self.__handler__}')

    def get_args(
            self,
            action: dict,
            props: dict,
    ):
        try:
            status_id = props[action['status']['tagname']]['value']
            date_from = convert_str_to_datetime(
                props[action['date_from']['tagname']]['name'])
            date_to = convert_str_to_datetime(
                props[action['date_to']['tagname']]['name'])
        except Exception as e:
            raise BadRequestException(
                detail=f'Invalid props for action: {self.__handler__}')
        return status_id, date_from, date_to

    def handle_response(self, db: Session,
                        user: User,
                        action: dict,
                        properties: dict,
                        ):
        status_id, date_from, date_to = self.get_args(action, properties)
        status = status_service.get_object(db, status_id, 'write')
        return [status, date_from, date_to]


handler = GrantLeaveHandler()
