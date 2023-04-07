import uuid

from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import Badge, BadgeType
from schemas import BadgeCreate, BadgeUpdate, BadgeRead
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
        badge_type = db.query(BadgeType).filter(BadgeType.name == "Черный Берет").first()
        badge = db.query(self.model).filter(self.model.user_id == user_id).filter(self.model.type_id == badge_type.id).first()
        return badge
    
    def create_relation(self, db: Session, user_id: str, badge_type_id: uuid.UUID):
        if db.query(BadgeType).filter(BadgeType.id == badge_type_id).first() is None:
            raise NotFoundException(detail=f"Badge type with id: {badge_type_id} is not found!")
        badge = Badge(
            user_id=user_id,
            type_id=badge_type_id
        )
        db.add(badge)
        db.flush()

        return badge
    
    def get_by_option(self, db: Session, skip: int, limit: int):
        return [BadgeRead.from_orm(badge) for badge in super().get_multi(db, skip, limit)]


badge_service = BadgeService(Badge)
