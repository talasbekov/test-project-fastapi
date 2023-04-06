from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import Badge
from schemas import BadgeCreate, BadgeUpdate
from .base import ServiceBase


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

    def get_by_user_id(self, db: Session, user_id: str):
        badge = db.query(self.model).filter(self.model.user_id == user_id).first()
        return badge
    
    def get_black_beret_by_user_id(self, db: Session, user_id: str):
        badge = db.query(self.model).filter(self.model.user_id == user_id).filter(self.model.badge_type.name == 'Черный Берет').first()
        return badge

badge_service = BadgeService(Badge)
