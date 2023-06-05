from uuid import UUID

from sqlalchemy.orm import Session

from .base import BaseAutoTagHandler
from schemas import AutoTagRead
from services import user_service



class FatherNameAutoTagHandler(BaseAutoTagHandler):
    __handler__ = "father_name"

    def handle(self, db: Session, user_id: UUID):
        user = user_service.get_by_id(db, user_id)
        return AutoTagRead(name=user.father_name, nameKZ=user.father_name)


handler = FatherNameAutoTagHandler()
