from sqlalchemy.orm import Session

from core import configs
from models import User, HrDocument, History
from .base import BaseHandler
from services import status_service, history_service
from exceptions import ForbiddenException


class GrantLeaveHandler(BaseHandler):
    __handler__ = "grant_leave"

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
            badge = action["badge"]["tagname"]
            date_from = action["date_from"]["tagname"]
            date_to = action["date_to"]["tagname"]
        except:
            raise ForbiddenException(
                f"Badge is not defined for this action: {self.__handler__}"
            )

        res = badge_service.create_relation(db, user.id, props[badge]["value"])
        history = history_service.create_timeline_history(
            db, user.id, res, props[date_from]["value"], props[date_to]["value"]
        )

        history.document_link = configs.GENERATE_IP + str(document.id)
        document.old_history_id = history.id

        db.add(user)
        db.add(res)
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
        pass

grant_leave_handler = GrantLeaveHandler()
