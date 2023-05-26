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
        try:
            badge_id = props[action["badge"]["tagname"]]["value"]
        except:
            raise ForbiddenException(
                f"Badge is not defined for this action: {self.__handler__}"
            )
        print(user.id)
        res = badge_service.stop_relation(db, user.id, badge_id)
        self.handle_validation(db, user, action, template_props, props, document)
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
        tagname = action["badge"]["tagname"]
        badge = badge_service.get_by_id(db, props[tagname]["value"])
        if not badge_service.exists_relation(db, user.id, badge.type_id):
            raise ForbiddenException(
                f"Badge is not assigned to this user: {user.first_name}, {user.last_name}"
            )

    def handle_filter(self, db: Session, user_query: Query[Any]):
        return user_query.join(Badge).filter(User.badges.any(User.id == Badge.user_id)).join(BadgeHistory, Badge.id == BadgeHistory.badge_id).filter(BadgeHistory.date_to == None)


handler = DeleteBadgeHandler()
