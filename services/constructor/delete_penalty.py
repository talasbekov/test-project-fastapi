from typing import Any

from sqlalchemy.orm import Session, Query

from core import configs
from models import User, HrDocument, Penalty
from .base import BaseHandler
from services import penalty_service
from exceptions import ForbiddenException


class DeletePenaltyHandler(BaseHandler):
    __handler__ = "delete_penalty"

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
        history = penalty_service.stop_relation(db, user.id, penalty_id)

        history.document_link = configs.GENERATE_IP + str(document.id)
        document.old_history_id = history.id

        db.add(user)
        db.add(history)
        db.add(document)
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
        pass

    def handle_filter(self, db: Session, user_query: Query[Any]):
        return user_query.filter(User.penalties.any(User.id == Penalty.user_id))

    def get_args(self, action, properties):
        try:
            penalty_id = properties[action["penalty"]["tagname"]]["value"]
        except KeyError:
            raise ForbiddenException(f"Penalty is not defined for this action: {self.__handler__}")
        return penalty_id

    def handle_response(self, db: Session,
                        action: dict,
                        properties: dict,
                        ):
        return None


handler = DeletePenaltyHandler()
