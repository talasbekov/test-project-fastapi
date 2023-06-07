import logging

from sqlalchemy.orm import Session

from core import configs
from models import User, HrDocument
from .base import BaseHandler
from services import secondment_service, history_service, state_body_service
from exceptions import BadRequestException
from utils import convert_str_to_datetime


class AddSecondmentToStateBody(BaseHandler):
    __handler__ = "add_secondment_to_state_body"

    def handle_action(
        self,
        db: Session,
        user: User,
        action: dict,
        template_props: dict,
        props: dict,
        document: HrDocument,
    ):
        state_body_id, date_from, date_to = self.get_args(action, props)
        self.handle_validation(db, user, action, template_props, props, document)
        state_body = state_body_service.get_by_id(db, state_body_id)
        res = secondment_service.create_relation(db, user.id, state_body)
        history = history_service.create_timeline_history(
            db, user.id, res, date_from, date_to
        )

        history.document_link = configs.GENERATE_IP + str(document.id)
        document.old_history_id = history.id

        db.add(user)
        db.add(history)
        db.add(document)
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
        pass

    def get_args(self, action, properties):
        try:
            state_body_id = properties[action["secondment"]["tagname"]]["value"]
            date_from = convert_str_to_datetime(properties[action["date_from"]["tagname"]]['name'])
            date_to = convert_str_to_datetime(properties[action["date_to"]["tagname"]]['name'])
        except KeyError as e:
            logging.exception(e)
            raise BadRequestException(f"StateBody is not defined for this action: {self.__handler__}")
        return state_body_id, date_from, date_to

    def handle_response(
        self,
        db: Session,
        user: User,
        action: dict,
        properties: dict
    ):
        state_body_id, date_from, date_to = self.get_args(action, properties)
        state_body = state_body_service.get_by_id(db, state_body_id)
        return {state_body, date_from, date_to}


handler = AddSecondmentToStateBody()
