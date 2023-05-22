from typing import Any

from sqlalchemy.orm import Session, Query

from core import configs
from models import User, HrDocument, Badge
from .base import BaseHandler
from services import badge_service
from exceptions import ForbiddenException


class DeleteBlackBeretHandler(BaseHandler):
    __handler__ = "delete_black_beret"

    def handle_action(
        self,
        db: Session,
        user: User,
        action: dict,
        template_props: dict,
        props: dict,
        document: HrDocument,
    ):
        black_beret = badge_service.get_black_beret_by_user_id(db, user.id)
        self.handle_validation(db, user, action, template_props, props, document)
        res = badge_service.stop_relation(db, user.id, black_beret.id)
        res.cancel_document_link = configs.GENERATE_IP + str(document.id)

        db.add(res)
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
        black_beret = badge_service.get_black_beret_by_user_id(db, user.id)
        if black_beret is None:
            raise ForbiddenException(
                f"Black Beret is not assigned to this user: {user.first_name}, {user.last_name}"
            )

    def handle_filter(self, db: Session, user_query: Query[Any]):
        badge_type = badge_service.get_black_beret(db)
        return user_query.filter(User.badges.any(Badge.type_id == badge_type.id))


handler = DeleteBlackBeretHandler()
