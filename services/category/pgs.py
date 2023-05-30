import uuid

from sqlalchemy.orm import Session

from models import User
from .base import BaseCategory


class PgsCategory(BaseCategory):
    __handler__ = 2

    def handle(self, db: Session) -> list[uuid.UUID]:
        return [db.query(User).first().id]


handler = PgsCategory()
