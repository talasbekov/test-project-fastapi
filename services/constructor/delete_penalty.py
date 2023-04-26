from sqlalchemy.orm import Session

from core import configs
from models import User, HrDocument
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
        tagname = action["penalty"]["tagname"]
        if not penalty_service.exists_relation(db, user.id, props[tagname]["value"]):
            raise ForbiddenException(
                f"Penalty is not assigned to this user: {user.first_name}, {user.last_name}"
            )
        history = penalty_service.stop_relation(db, user.id, props[tagname]["value"])

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

handler = DeletePenaltyHandler()
