from sqlalchemy.orm import Session

from core import configs
from models import User, CoolnessHistory, HrDocument
from .base import BaseHandler
from services import coolness_service, history_service
from exceptions import ForbiddenException, NotSupportedException


def get_last_by_user_id(db: Session, user_id: str):
    res = (
        db.query(CoolnessHistory)
        .filter(CoolnessHistory.user_id == user_id, CoolnessHistory.date_to == None)
        .order_by(CoolnessHistory.date_to.desc())
        .first()
    )
    return res


class DecreaseCoolnessHandler(BaseHandler):
    __handler__ = "decrease_coolness"

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
        coolness = coolness_service.get_by_id(db, props[tagname]["value"])

        self.handle_validation(db, user, action, template_props, props, document)
        user.coolnesses.append(coolness)
        history = history_service.create_history(db, user.id, coolness)

        history.document_link = configs.GENERATE_IP + str(document.id)
        document.old_history_id = history.id

        db.add(user)
        db.add(history)
        db.add(document)
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
        coolness = coolness_service.get_by_id(db, props[tagname]["value"])
        coolness_type = coolness_service.get_object(db, coolness.type_id)

        history_last_coolness = get_last_by_user_id(db, user.id)
        user_coolness = coolness_service.get_by_id(
            db, history_last_coolness.coolness_id
        )
        user_coolness_type = coolness_service.get_object(db, user_coolness.type_id)

        if (
            user_coolness_type.order <= coolness_type.order
            or user_coolness_type.order - coolness_type.order != 1
        ):
            raise ForbiddenException(
                detail=f"You can not decrease coolness to {coolness.name}"
            )


handler = DecreaseCoolnessHandler()
