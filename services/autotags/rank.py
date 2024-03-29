from uuid import UUID

from sqlalchemy.orm import Session

from .base import BaseAutoTagHandler
from schemas import AutoTagRead
from services import user_service


class RankAutoTagHandler(BaseAutoTagHandler):
    __handler__ = "rank"

    def handle(self, db: Session, user_id: UUID):
        user = user_service.get_by_id(db, user_id)
        return AutoTagRead(name=user.rank.name, nameKZ=user.rank.nameKZ)


handler = RankAutoTagHandler()
