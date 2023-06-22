from sqlalchemy.orm import Session

from core import configs
from models import User, HrDocument
from .base import BaseHandler
from services import coolness_service, history_service
from exceptions import ForbiddenException, BadRequestException


class ConfirmCoolnessHandler(BaseHandler):
    __handler__ = "confirm_coolness"

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
        res = coolness_service.get_relation(db, user.id, coolness_id)
        history = history_service.create_history(db, user.id, res)

        history.confirm_document_link = configs.GENERATE_IP + str(document.id)
        document.old_history_id = history.id

        db.add(user)
        db.add(history)
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
        coolness_id = self.get_args(action, props)

        coolness_service.get_by_id(db, coolness_id)

        if not coolness_service.exists_relation(db, user.id, coolness_id):
            raise ForbiddenException(
                ("Coolness is not assigned to this user:"
                 f" {user.first_name}, {user.last_name}")
            )

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
        coolness_id = self.get_args(action, properties)
        obj = coolness_service.get_by_id(db, coolness_id).type
        return obj


handler = ConfirmCoolnessHandler()
