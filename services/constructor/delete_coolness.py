from typing import Any

from sqlalchemy.orm import Session, Query

from core import configs
from models import User, HrDocument, Coolness
from .base import BaseHandler
from services import coolness_service
from exceptions import ForbiddenException, BadRequestException


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
        coolness_id = self.get_args(action, props)
        self.handle_validation(
            db, user, action, template_props, props, document)
        res = coolness_service.stop_relation(db, user.id, coolness_id)

        res.cancel_document_link = configs.GENERATE_IP + str(document.id)
        document.old_history_id = res.id

    def handle_validation(
        self,
        db: Session,
        user: User,
        action: dict,
        props: dict,
    ):
        coolness_id = self.get_args(action, props)
        coolness = coolness_service.get_by_id(db, coolness_id)
        if not coolness_service.exists_relation(db, user.id, coolness.type_id):
            raise ForbiddenException(
                f"Coolness is not assigned to this user: {user.first_name}, {user.last_name}"
            )

    def handle_filter(self, db: Session, user_query: Query[Any]):
        return user_query.filter(User.coolnesses.any(User.id == Coolness.user_id))

    def get_args(self, action, properties):
        try:
            coolness_id = properties[action["coolness"]["tagname"]]["value"]
        except KeyError:
            raise BadRequestException(
                f"Coolness is not defined for this action: {self.__handler__}")
        return coolness_id

    def handle_response(self, db: Session,
                        user: User,
                        action: dict,
                        properties: dict,
                        ):
        return None


handler = DeleteCoolnessHandler()
