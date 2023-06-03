from uuid import UUID

from sqlalchemy.orm import Session

from .base import BaseAutoTagHandler
from services import user_service


class FatherNameAutoTagHandler(BaseAutoTagHandler):
    __handler__ = "father_name"

    def handle(self, db: Session, user_id: UUID):
        user = user_service.get_by_id(db, user_id)
        return user.father_name


handler = FatherNameAutoTagHandler()
