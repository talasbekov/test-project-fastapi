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
        try:
            position = action["staff_unit"]["tagname"]
        except:
            raise ForbiddenException(
                f"Staff unit is not defined for this action: {self.__handler__}"
            )
        staff_unit_id = archive_staff_unit_service.get_by_id(db, props[position]["value"]).origin_id
        self._handle_validation(db, user, staff_unit_id)

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
        template_props: dict,
        props: dict,
        document: HrDocument,
    ):
        if staff_unit_service.exists_relation(db, user.id, props[action["staff_unit"]["tagname"]]['value']):
            raise ForbiddenException(
                f"This position is already assigned to this user: {user.first_name}, {user.last_name}"
            )

    def _handle_validation(self, db: Session, user: User, staff_unit_id: uuid.UUID):
        if staff_unit_service.exists_relation(db, user.id, staff_unit_id):
            raise ForbiddenException(
                f"This position is already assigned to this user: {user.first_name}, {user.last_name}"
            )


handler = ApplyArchivePosition()
