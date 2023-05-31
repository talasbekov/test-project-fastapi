import uuid

from sqlalchemy.orm import Session

from core import configs
from exceptions import ForbiddenException
from models import User, HrDocument, ArchiveStaffUnit
from .base import BaseHandler
from exceptions import ForbiddenException
from .. import staff_unit_service, history_service, archive_staff_unit_service


class ApplyArchivePosition(BaseHandler):
    __handler__ = "apply_archive_position"

    def handle_action(self,
                      db: Session,
                      user: User,
                      action: dict,
                      template_props: dict,
                      props: dict,
                      document: HrDocument):

        position_id = self.get_args(action, props)
        staff_unit_id = archive_staff_unit_service.get_by_id(db, position_id).origin_id
        self.handle_validation(db, user, action, props)

        old_history = staff_unit_service.get_last_history(db, user.id)
        if old_history is not None:
            document.old_history_id = old_history.id
        res = staff_unit_service.create_relation(db, user, staff_unit_id)
        history = history_service.create_history(db, user.id, res)

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
        props: dict,
    ):
        position_id = self.get_args(action, props)
        if staff_unit_service.exists_relation(db, user.id, position_id):
            raise ForbiddenException(
                f"This position is already assigned to this user: {user.first_name}, {user.last_name}"
            )

    def get_args(self, action, properties):
        try:
            position_id = properties[action["staff_unit"]["tagname"]]["value"]
        except KeyError:
            raise ForbiddenException(f"Position is not defined for this action: {self.__handler__}")
        return position_id


handler = ApplyArchivePosition()
