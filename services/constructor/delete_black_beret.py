from sqlalchemy.orm import Session

from core import configs
from models import User, HrDocument
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
        tagname = action["black_beret"]["tagname"]
        if not badge_service.get_black_beret_by_user_id(db, user.id) is None:
            raise ForbiddenException(
                f"Black Beret is not assigned to this user: {user.first_name}, {user.last_name}"
            )
        res = badge_service.stop_relation(db, user.id, props[tagname]["value"])
        res.cancel_document_link = configs.GENERATE_IP + document.id

        db.add(res)
        db.add(document)
        db.flush()


handler = DeleteBlackBeretHandler()
