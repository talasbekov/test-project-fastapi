import uuid

from sqlalchemy.orm import Session

from schemas import UserShortRead
from models import User
from services import staff_division_service
from .base import BaseCategory


class CuratorCategory(BaseCategory):
    __handler__ = 1

    def handle(self, db: Session, user_id: uuid.UUID) -> list[uuid.UUID]:
        user = db.query(User).filter(User.id == user_id).first()
        superviser = db.query(User).filter(
            User.id == user.supervised_by).first()
        if superviser is None:
            return []
        return [superviser.id]


handler = CuratorCategory()
