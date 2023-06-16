from sqlalchemy.orm import Session

from core import configs
from models import User, CoolnessHistory, HrDocument
from .base import BaseHandler
from services import coolness_service, history_service
from exceptions import ForbiddenException, BadRequestException


def get_last_by_user_id(db: Session, user_id: str):
    res = (
        db.query(CoolnessHistory)
        .filter(CoolnessHistory.user_id == user_id, CoolnessHistory.date_to is None)
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
        coolness_id = self.get_args(action, props)

        self.handle_validation(
            db, user, action, template_props, props, document)

        coolness = coolness_service.get_by_id(db, coolness_id)
        coolness_type = coolness.type

        history = (
            db.query(CoolnessHistory)
            .filter(CoolnessHistory.user_id == user.id)
            .filter(CoolnessHistory.coolness_id == coolness.id)
            .first()
        )
        history.cancel_document_link = configs.GENERATE_IP + str(document.id)

        type = coolness_service.get_type_by_order(db, coolness_type.order - 1)

        new_coolness = coolness_service.create_relation(db, user.id, type.id)

        user.coolnesses.append(new_coolness)
        history = history_service.create_history(db, user.id, new_coolness)

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
        coolness_id = self.get_args(action, props)
        coolness = coolness_service.get_by_id(db, coolness_id)
        coolness_type = coolness.type

        if coolness_type.order == 1:
            raise ForbiddenException(
                detail=f"You can not decrease coolness to {coolness_type.name}"
            )

    def get_args(self, action, properties):
        try:
            coolness_id = properties[action["coolness"]["tagname"]]["value"]
        except KeyError:
            raise BadRequestException(
                f"Coolness is not defined for this action: {self.__handler__}")
        return coolness_id

    def handle_response(self, db: Session,
                        user: User,
                        action: dict,
                        properties: dict,
                        ):
        args = self.get_args(action, properties)
        obj = coolness_service.get_by_id(db, args).type
        return obj


handler = DecreaseCoolnessHandler()
