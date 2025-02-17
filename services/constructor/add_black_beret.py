from typing import Any

from sqlalchemy.orm import Session, Query

from core import configs
from models import User, HrDocument, Badge
from exceptions import ForbiddenException, BadRequestException
from services import badge_service, history_service
from .base import BaseHandler


class AddBlackBeretHandler(BaseHandler):
    __handler__ = "add_black_beret"

    def handle_action(
        self,
        db: Session,
        user: User,
        action: dict,
        template_props: dict,
        props: dict,
        document: HrDocument,
    ):
        badge = self.get_args(db)
        self.handle_validation(
            db, user, action, template_props, props, document)
        res = badge_service.create_relation(db, user.id, badge.id)
        history = history_service.create_history(db, user.id, res)
        document.old_history_id = history.id
        history.document_link = configs.GENERATE_IP + str(document.id)
        db.add(user)
        db.add(document)
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
        if history_service.has_penalty_history(db, user.id):
            raise BadRequestException(
                f"Инициирование приказа возможно после снятия взыскания!")
        if badge_service.get_black_beret_by_user_id(db, user.id) is not None:
            raise ForbiddenException(
                ("Badge is already assigned to this user:"
                 f" {user.first_name} {user.last_name}")
            )

    def handle_filter(self, db: Session, user_query: Query[Any]):
        badge = self.get_args(db)
        users = user_query.filter(User.badges.any(
            Badge.type_id != badge.id))
        
        return users

    def get_args(self, db: Session):
        badge_type = badge_service.get_black_beret(db)
        if badge_type:
            return badge_type
        else:
            raise BadRequestException("Black beret badge not found")

    def handle_response(self, db: Session,
                        user: User,
                        action: dict,
                        properties: dict,
                        ):
        obj = badge_service.get_black_beret(db)
        return obj


handler = AddBlackBeretHandler()
