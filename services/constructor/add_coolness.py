from sqlalchemy.orm import Session

from core import configs
from models import User, HrDocument
from .base import BaseHandler
from services import coolness_service, history_service
from exceptions import ForbiddenException


class AddCoolnessHandler(BaseHandler):
    __handler__ = "add_coolness"

    def handle_action(
        self,
        db: Session,
        user: User,
        action: dict,
        template_props: dict,
        props: dict,
        document: HrDocument,
    ):
        tagname = action["coolness"]["tagname"]
        if coolness_service.exists_relation(db, user.id, props[tagname]["value"]):
            raise ForbiddenException(
                f"Coolness is already assigned to this user: {user.first_name}, {user.last_name}"
            )
        res = coolness_service.create_relation(db, user.id, props[tagname]["value"])
        user.coolnesses.append(res)
        history = history_service.create_history(db, user.id, res)

        history.document_link = configs.GENERATE_IP + str(document.id)
        document.old_history_id = history.id

        db.add(user)
        db.flush()

        return user


handler = AddCoolnessHandler()
