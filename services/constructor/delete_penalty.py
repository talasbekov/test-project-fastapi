from typing import Any

from sqlalchemy.orm import Session, Query

from core import configs
from models import User, HrDocument, Penalty, PenaltyHistory
from .base import BaseHandler
from services import penalty_service, penalty_type_service
from exceptions import BadRequestException


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
        self.handle_validation(
            db, user, action, template_props, props, document)
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
        penalty_type_id = self.get_args(action, props)
        penalty = penalty_service.get_by_type_and_user(db, str(penalty_type_id), user.id)
        penalty_service.get_by_id(db, str(penalty.id))

    def handle_filter(self, db: Session, user_query: Query[Any]):
        return user_query.filter(
            User.penalties.any(User.id == Penalty.user_id))

    def get_args(self, action, properties):
        try:
            penalty_id = properties[action["penalty"]["tagname"]]["value"]
        except KeyError:
            raise BadRequestException(
                f"Penalty is not defined for this action: {self.__handler__}")
        return penalty_id

    def handle_response(self, db: Session,
                        user: User,
                        action: dict,
                        properties: dict,
                        ):
        penalty_id = self.get_args(action, properties)
        penalty_type_id = penalty_service.get_by_id(
            db=db, id=str(penalty_id)).type_id
        obj = penalty_type_service.get_by_id(db, penalty_type_id)
        penalty_type = {'name': obj.name, 'nameKZ': obj.nameKZ}
        history = (db.query(PenaltyHistory)
                   .filter(PenaltyHistory.user_id == user.id,
                           PenaltyHistory.penalty_id == penalty_id).first())
        return {"penalty_type": penalty_type,
                "document_number": history.document_number,
                "document_link": history.document_link}


handler = DeletePenaltyHandler()
