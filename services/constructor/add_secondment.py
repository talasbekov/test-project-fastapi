from sqlalchemy.orm import Session

from core import configs
from models import User, HrDocument
from .base import BaseHandler
from services import (
    secondment_service,
    history_service,
    staff_division_service,
)
from exceptions import BadRequestException
from utils import convert_str_to_datetime


class AddSecondmentHandler(BaseHandler):
    __handler__ = "add_secondment"

    def handle_action(
        self,
        db: Session,
        user: User,
        action: dict,
        template_props: dict,
        props: dict,
        document: HrDocument,
    ):
        staff_division_id, date_from, date_to = self.get_args(action, props)
        self.handle_validation(
            db, user, action, template_props, props, document)
        staff_division = staff_division_service.get_by_id(
            db, staff_division_id)
        res = secondment_service.create_relation(db, user.id, staff_division)
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
        secondment_id, _, _ = self.get_args(action, props)

        staff_division_service.get_by_id(db, secondment_id)

    def get_args(self, action, properties):
        try:
            secondment_id = properties[action["secondment"]
                                       ["tagname"]]["value"]
            date_from = convert_str_to_datetime(
                properties[action["date_from"]["tagname"]]['name'])
            date_to = convert_str_to_datetime(
                properties[action["date_to"]["tagname"]]['name'])
        except KeyError:
            raise BadRequestException(
                f"Secondment is not defined for this action: {self.__handler__}")
        return secondment_id, date_from, date_to

    def handle_response(
        self,
        db: Session,
        user: User,
        action: dict,
        properties: dict,
    ):
        secondment_id, date_from, date_to = self.get_args(action, properties)
        staff_division = staff_division_service.get_by_id(db, secondment_id)
        return {staff_division, date_from, date_to}


handler = AddSecondmentHandler()
