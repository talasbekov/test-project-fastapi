from uuid import UUID

from sqlalchemy.orm import Session

from .base import BaseAutoTagHandler
from schemas import AutoTagRead
from services import user_service


class OfficerNumberAutoTagHandler(BaseAutoTagHandler):
    __handler__ = "officer_number"

    def handle(self, db: Session, user_id: UUID):
        user = user_service.get_by_id(db, user_id)
        return AutoTagRead(name=user.id_number, nameKZ=user.id_number)


handler = OfficerNumberAutoTagHandler()
