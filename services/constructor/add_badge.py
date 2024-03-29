from sqlalchemy.orm import Session

from core import configs
from models import User, HrDocument, History
from .base import BaseHandler
from services import badge_service, history_service
from exceptions import BadRequestException


class AddBadgeHandler(BaseHandler):
    __handler__ = "add_badge"

    def handle_action(
        self,
        db: Session,
        user: User,
        action: dict,
        template_props: dict,
        props: dict,
        document: HrDocument,
    ):
        badge_id = self.get_args(action, props)
        self.handle_validation(
            db, user, action, template_props, props, document)
        res = badge_service.create_relation(db, user.id, badge_id)
        user.badges.append(res)
        history: History = history_service.create_history(db, user.id, res)
        history.document_link = configs.GENERATE_IP + str(document.id)
        db.add(user)
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
        badge_id = self.get_args(action, props)

        badge_service.get_badge_by_id(db, badge_id)

        if badge_service.exists_relation(db, user.id, badge_id):
            raise BadRequestException(
                ("Badge is already assigned to this user:"
                 f" {user.first_name} {user.last_name}")
            )
        if history_service.has_penalty_history(db, user.id):
            raise BadRequestException(
                f"Инициирование приказа возможно после снятия взыскания!")

    def get_args(self, action, properties):
        try:
            badge_id = properties[action["badge"]["tagname"]]["value"]
        except KeyError:
            raise BadRequestException(
                f"Badge is not defined for this action: {self.__handler__}")
        return badge_id

    def handle_response(self, db: Session,
                        user: User,
                        action: dict,
                        properties: dict,
                        ):
        badge_id = self.get_args(action, properties)
        obj = badge_service.get_badge_by_id(db, badge_id)
        return obj


handler = AddBadgeHandler()
