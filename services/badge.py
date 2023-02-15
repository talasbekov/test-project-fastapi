from sqlalchemy.orm import Session

from .base import ServiceBase

from models import Badge
from schemas import BadgeCreate, BadgeUpdate, BadgeRead
from exceptions.client import NotFoundException


class BadgeService(ServiceBase[Badge, BadgeCreate, BadgeUpdate]):
    
    def get_by_id(self, db: Session, id: str):
        badge = super().get(db, id)
        if badge is None:
            raise NotFoundException(detail=f"Badge with id: {id} is not found!")
        return badge

    def add_badge(self, db: Session, body: BadgeCreate):
        badge = Badge(
            name= body.name,
            url= body.url
        )
        db.add(badge)
        db.flush()
        return badge


badge_service = BadgeService(Badge)
 