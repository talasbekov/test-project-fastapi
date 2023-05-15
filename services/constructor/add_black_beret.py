from sqlalchemy.orm import Session

from core import configs
from models import User, HrDocument, Badge
from exceptions import ForbiddenException
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
        badge_type = badge_service.get_black_beret(db)
        self.handle_validation(db, user, action, template_props, props, document)
        res = badge_service.create_relation(db, user.id, badge_type.id)
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
        badge_type = badge_service.get_black_beret(db)
        if badge_service.exists_relation(db, user.id, badge_type.id):
            raise ForbiddenException(
                f"Badge is already assigned to this user: {user.first_name} {user.last_name}"
            )

    def handle_filter(self, db: Session, user_queue):
        badge_type = badge_service.get_black_beret(db)
        print(badge_type.id)
        return user_queue.join(Badge).filter(Badge.type_id != badge_type.id)


handler = AddBlackBeretHandler()
