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
        self.handle_validation(
            db, user, action, template_props, props, document)
        black_beret = self.get_args(db, user)
        res = badge_service.stop_relation(db, user.id, black_beret.id)
        res.cancel_document_link = configs.GENERATE_IP + str(document.id)
        res.document_number = document.reg_number

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
        black_beret = self.get_args(db, user)
        if black_beret is None:
            raise ForbiddenException(
                ("Black Beret is not assigned to this user:"
                 f" {user.first_name}, {user.last_name}")
            )

    def handle_filter(self, db: Session, user_query: Query[Any]):
        badge_type = badge_service.get_black_beret(db)
        return user_query.filter(User.badges.any(
            Badge.type_id == badge_type.id))

    def get_args(self, db: Session, user: User):
        black_beret = badge_service.get_black_beret_by_user_id(db, user.id)
        return black_beret

    def handle_response(self, db: Session,
                        user: User,
                        action: dict,
                        properties: dict,
                        ):
        obj = badge_service.get_black_beret(db)
        return obj


handler = DeleteBlackBeretHandler()
