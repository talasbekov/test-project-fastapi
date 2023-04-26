from sqlalchemy.orm import Session

from core import configs
from models import User, HrDocument
from .base import BaseHandler
from services import coolness_service
from exceptions import ForbiddenException


class DeleteCoolnessHandler(BaseHandler):
    __handler__ = "delete_coolness"

    def handle_action(
        self,
        db: Session,
        user: User,
        action: dict,
        template_props: dict,
        props: dict,
        document: HrDocument,
    ):
        tagname = action["coolness"]["tagname"]
        self.handle_validation(db, user, action, template_props, props, document)
        res = coolness_service.stop_relation(db, user.id, props[tagname]["value"])

        res.document_link = configs.GENERATE_IP + str(document.id)
        document.old_history_id = res.id

    def handle_validation(
        self,
        db: Session,
        user: User,
        action: dict,
        template_props: dict,
        props: dict,
        document: HrDocument,
    ):
        tagname = action["coolness"]["tagname"]
        if not coolness_service.exists_relation(db, user.id, props[tagname]["value"]):
            raise ForbiddenException(
                f"Coolness is not assigned to this user: {user.first_name}, {user.last_name}"
            )


handler = DeleteCoolnessHandler()
