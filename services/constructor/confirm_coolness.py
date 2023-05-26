from sqlalchemy.orm import Session

from core import configs
from models import User, HrDocument, CoolnessHistory
from .base import BaseHandler
from services import coolness_service, history_service
from exceptions import ForbiddenException



class ConfirmCoolnessHandler(BaseHandler):
    __handler__ = "confirm_coolness"

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
            tagname = action["coolness"]["tagname"]
        except:
            raise ForbiddenException(
                f"Coolness is not defined for this action: {self.__handler__}"
            )
        self.handle_validation(db, user, action, template_props, props, document)
        res = coolness_service.get_relation(db, user.id, props[tagname]["value"])
        history = history_service.create_history(db, user.id, res)

        history.confirm_document_link = configs.GENERATE_IP + str(document.id)
        document.old_history_id = history.id

        db.add(user)
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
        tagname = action["coolness"]["tagname"]
        if not coolness_service.exists_relation(db, user.id, props[tagname]["value"]):
            raise ForbiddenException(
                f"Coolness is not assigned to this user: {user.first_name}, {user.last_name}"
            )

handler = ConfirmCoolnessHandler()
