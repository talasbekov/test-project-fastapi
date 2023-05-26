from typing import Any

from sqlalchemy.orm import Session, Query

from core import configs
from models import User, HrDocument, Coolness
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
        try:
            tagname = action["coolness"]["tagname"]
        except:
            raise ForbiddenException(
                f"Coolness is not defined for this action: {self.__handler__}"
            )
        self.handle_validation(db, user, action, template_props, props, document)
        res = coolness_service.stop_relation(db, user.id, props[tagname]["value"])

        res.cancel_document_link = configs.GENERATE_IP + str(document.id)
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
        coolness = coolness_service.get_by_id(db, props[tagname]["value"])
        if not coolness_service.exists_relation(db, user.id, coolness.type_id):
            raise ForbiddenException(
                f"Coolness is not assigned to this user: {user.first_name}, {user.last_name}"
            )

    def handle_filter(self, db: Session, user_query: Query[Any]):
        return user_query.filter(User.coolnesses.any(User.id == Coolness.user_id))


handler = DeleteCoolnessHandler()
