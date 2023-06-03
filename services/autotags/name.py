from uuid import UUID

from sqlalchemy.orm import Session

from .base import BaseAutoTagHandler
from services import user_service


class NameAutoTagHandler(BaseAutoTagHandler):
    __handler__ = "name"

    def handle(self, db, user_id):
        user = user_service.get_by_id(db, user_id)
        return user.first_name


handler = NameAutoTagHandler()
