from sqlalchemy.orm import Session

from core import configs
from models import User, HrDocument
from .base import BaseHandler
from services import secondment_service, history_service
from exceptions import ForbiddenException
from utils import convert_str_to_datetime


class AddSecondmentToStateBody(BaseHandler):

    def handle_action(
        self,
        db: Session,
        user: User,
        action: dict,
        template_props: dict,
        props: dict,
        document: HrDocument,
    ):
        pass

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
            secondment_id = properties[action["secondment"]["tagname"]]["value"]
            date_from = convert_str_to_datetime(properties[action["date_from"]["tagname"]]['name'])
            date_to = convert_str_to_datetime(properties[action["date_to"]["tagname"]]['name'])
        except KeyError:
            raise ForbiddenException(f"Secondment is not defined for this action: {self.__handler__}")
        return secondment_id, date_from, date_to

    def handle_response(
        self,
        db: Session,
        action: dict,
        properties: dict
    ):
        pass


handler = AddSecondmentToStateBody()
