from typing import Any

from sqlalchemy.orm import Session, Query

from core import configs
from models import User, HrDocument, Badge, BadgeHistory
from .base import BaseHandler
from services import badge_service, history_service
from exceptions import ForbiddenException


class DeleteBadgeHandler(BaseHandler):
    __handler__ = "delete_badge"

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
        res = badge_service.stop_relation(db, user.id, badge_id)
        document.old_history_id = res.id
        res.cancel_document_link = configs.GENERATE_IP + str(document.id)
        db.add(document)
        db.add(res)
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
        badge_id = self.get_args(action, props)
        badge = badge_service.get_by_id(db, badge_id)
        if not badge_service.exists_relation(db, user.id, badge.type_id):
            raise ForbiddenException(
                f"Badge is not assigned to this user: {user.first_name}, {user.last_name}"
            )

    def handle_filter(self, db: Session, user_query: Query[Any]):
        return user_query.join(Badge).filter(User.badges.any(User.id == Badge.user_id)).join(BadgeHistory,
                                                                                             Badge.id == BadgeHistory.badge_id).filter(
            BadgeHistory.date_to is None)

    def get_args(self, action, properties):
        try:
            badge_id = properties[action["badge"]["tagname"]]["value"]
        except KeyError:
            raise ForbiddenException(
                f"Badge is not defined for this action: {self.__handler__}")
        return badge_id

    def handle_response(self, db: Session,
                        user: User,
                        action: dict,
                        properties: dict,
                        ):
        badge_id = self.get_args(action, properties)
        badge_type_id = badge_service.get_by_id(db, badge_id).type_id
        badge_type = badge_service.get_badge_by_id(db, badge_type_id)
        return badge_type


handler = DeleteBadgeHandler()
