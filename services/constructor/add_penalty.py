from sqlalchemy.orm import Session

from core import configs
from models import User, HrDocument
from .base import BaseHandler
from services import penalty_service, history_service, penalty_type_service
from exceptions import ForbiddenException

from utils import convert_str_to_datetime


class AddPenaltyHandler(BaseHandler):
    __handler__ = "add_penalty"

    def handle_action(
        self,
        db: Session,
        user: User,
        action: dict,
        template_props: dict,
        props: dict,
        document: HrDocument,
    ):
        penalty_id = self.get_args(action, props)
        self.handle_validation(db, user, action, template_props, props, document)
        res = penalty_service.create_relation(db, user.id, penalty_id)
        res.name = action["reason"]["tagname"]
        user.penalties.append(res)
        history = history_service.create_history(db, user.id, res)

        history.document_link = configs.GENERATE_IP + str(document.id)
        document.old_history_id = history.id
        history.document_number = document.reg_number

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
            penalty_id = properties[action["penalty"]["tagname"]]["value"]
        except KeyError:
            raise ForbiddenException(f"Penalty is not defined for this action: {self.__handler__}")
        return penalty_id

    def handle_response(self, db: Session,
                        user: User,
                        action: dict,
                        properties: dict,
    ):
        args = self.get_args(action, properties)
        obj = penalty_type_service.get_by_id(db, args)
        return {'name': obj.name, 'nameKZ': obj.nameKZ}


handler = AddPenaltyHandler()
