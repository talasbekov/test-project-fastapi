from typing import Any

from sqlalchemy.orm import Session, Query

from core import configs
from models import User, HrDocument, Badge
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
        tagname = action["badge"]["tagname"]
        res = badge_service.stop_relation(db, user.id, props[tagname]["value"])
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
        if not badge_service.exists_relation(db, user.id, props[tagname]["value"]):
            raise ForbiddenException(
                f"Badge is not assigned to this user: {user.first_name}, {user.last_name}"
            )

    def handle_filter(self, db: Session, user_query: Query[Any]):
        return user_query.filter(User.badges.any(User.id == Badge.user_id))


handler = DeleteBadgeHandler()
