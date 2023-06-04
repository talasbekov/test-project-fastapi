from sqlalchemy.orm import Session

from core import configs
from models import User, HrDocument, EmergencyServiceHistory
from .base import BaseHandler
from services import staff_unit_service, history_service, user_service
from exceptions import ForbiddenException
from utils import convert_str_to_datetime


class PositionChangeHandler(BaseHandler):
    __handler__ = "position_change"

    def handle_action(
        self,
        db: Session,
        user: User,
        action: dict,
        template_props: dict,
        props: dict,
        document: HrDocument,
    ):
        self.handle_validation(db, user, action, template_props, props, document)
        position, percent = self.get_args(action, props)
        old_history = staff_unit_service.get_last_history(db, user.id)
        if old_history is not None:
            document.old_history_id = old_history.id

        res = staff_unit_service.create_relation(db, user, position)
        history: EmergencyServiceHistory = history_service.create_history(db, user.id, res)
        history.percentage = percent
        history.document_link = configs.GENERATE_IP + str(document.id)

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
        position, percent = self.get_args(action, props)
        print(position, percent)
        try:
            if staff_unit_service.exists_relation(db, user.id, position):
                raise ForbiddenException(
                    f"This position is already assigned to this user: {user.first_name}, {user.last_name}"
                )
            if percent < 0 or percent > 100:
                raise ForbiddenException(f"Percentage must be between 0 and 100: {percent}")
        except Exception as e:
            raise ForbiddenException(f"Args are  not defined for this action: {self.__handler__}")

    def get_args(self, action, properties):
        try:
            position = properties[action["staff_unit"]["tagname"]]["value"]
            percent = int(properties[action["percent"]["tagname"]]["name"])
        except:
            raise ForbiddenException(f"Position is not defined for this action: {self.__handler__}")
        return position, percent


handler = PositionChangeHandler()
