import uuid
from datetime import datetime

from sqlalchemy import and_
from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import Badge, BadgeType, User, BadgeHistory
from schemas import BadgeCreate, BadgeUpdate, BadgeRead, BadgeTypeRead
from .base import ServiceBase


class BadgeService(ServiceBase[Badge, BadgeCreate, BadgeUpdate]):
    def get_by_id(self, db: Session, id: str):
        badge = super().get(db, id)
        if badge is None:
            raise NotFoundException(
                detail=f"Badge with id: {id} is not found!")
        return badge

    def get_badge_by_type(self, db: Session, type_id: str):
        badge = db.query(Badge).filter(Badge.type_id == type_id).first()
        if badge is None:
            raise NotFoundException(
                detail=f"Badge with id: {type_id} is not found!")
        return badge

    def add_badge(self, db: Session, body: BadgeCreate):
        badge = Badge(name=body.name, url=body.url)
        db.add(badge)
        db.flush()
        return badge

    def get_by_user_id(self, db: Session, user_id: str):
        badge = db.query(
            self.model).filter(
            self.model.user_id == user_id).first()
        return badge

    def get_black_beret_by_user_id(self, db: Session, user_id: str):
        badge_type = (
            db.query(BadgeType).filter(
                BadgeType.name == "Черный Берет").first()
        )
        badge_history = db.query(BadgeHistory).filter(BadgeHistory.user_id == user_id).all()
          # Refresh the session to get the most up-to-date data
        db.refresh(badge_type)
        badge = (
            db.query(Badge)
            .filter(Badge.user_id == user_id)
            .filter(Badge.type_id == badge_type.id)
            .first()
        )
        db.refresh(badge)
        badge = (
            db.query(Badge)
            .filter(Badge.user_id == user_id)
            .filter(Badge.type_id == badge_type.id)
            .order_by(self.model.created_at.desc()) # Аскар чекни это правильно или нет
            .first() 
        )
        print("Beret:", badge.created_at)
        print("Beret:", badge.id)
        return badge

    def get_black_beret_by_user_id_and_date(self, db: Session, user_id: str, date_till):
        badge_type = (
            db.query(BadgeType).filter(
                BadgeType.name == "Черный Берет").first()
        )
        badge = (
            db.query(self.model)
            .filter(self.model.user_id == user_id)
            .filter(self.model.type_id == badge_type.id)
            .filter(self.model.created_at <= date_till)
            .first()
        )
        return badge

    def create_relation(self, db: Session, user_id: str,
                        badge_type_id: str):
        if db.query(BadgeType).filter(
                BadgeType.id == badge_type_id).first() is None:
            raise NotFoundException(
                detail=f"Badge type with id: {badge_type_id} is not found!"
            )
        badge = Badge(user_id=user_id, type_id=badge_type_id)
        db.add(badge)
        db.flush()

        return badge

    def exists_relation(self, db: Session, user_id: str,
                        badge_type_id: str):
        return (
            db.query(Badge)
            .filter(Badge.user_id == user_id)
            .filter(Badge.type_id == badge_type_id)
            .join(BadgeHistory,
                  and_(Badge.id == BadgeHistory.badge_id,
                       BadgeHistory.date_to == None))
            .first()
        ) is not None

    def stop_relation(self, db: Session, user_id: str, badge_id: str):
        res = (
            db.query(BadgeHistory)
            .filter(BadgeHistory.badge_id == badge_id,
                    BadgeHistory.user_id == user_id,
                    BadgeHistory.date_to == None)
            .first()
        )
        if res is None:
            raise NotFoundException(
                detail=f"Badge with id: {badge_id} is not found!")
        res.date_to = datetime.now()
        db.add(res)
        db.flush()
        db.refresh(res)
        return res

    def get_multiple(self, db: Session, skip: int, limit: int):
        return db.query(BadgeType).offset(skip).limit(limit).all()

    def get_badge_by_id(self, db: Session, id: str):
        badge = db.query(BadgeType).filter(BadgeType.id == id).first()
        if badge is None:
            raise NotFoundException(
                detail=f"Badge with id: {id} is not found!")
        return badge
    
    def get_by_badge_id(self, db: Session, id: str):
        badge = db.query(Badge).filter(Badge.id == id).first()
        if badge is None:
            raise NotFoundException(
                detail=f"Badge with id: {id} is not found!")
        return badge

    def create_badge(self, db: Session, body: BadgeCreate):
        badge = db.query(Badge).filter(Badge.user_id == body.user_id).first()
        badge_type = db.query(BadgeType).filter(
            BadgeType.id == body.type_id).first()
        if badge_type is None:
            raise NotFoundException(
                detail=f"Badge type with id: {body.type_id} is not found!"
            )
        badge = Badge(user_id=body.user_id, type_id=badge_type.id)
        db.add(badge)
        db.flush()
        return badge

    def update_badge(self, db: Session, id: str, body: BadgeUpdate):
        badge = self.get_badge_by_id(db, id)
        badge.name = body.name
        badge.url = body.url
        db.add(badge)
        db.flush()
        return badge

    def delete_badge(self, db: Session, id: str):
        badge = db.query(BadgeType).filter(BadgeType.id == id).first()
        if badge is None:
            raise NotFoundException(
                detail=f"Badge with id: {id} is not found!")
        db.delete(badge)
        db.flush()

    def get_by_option(
        self, db: Session, type: str, id: str, skip: int, limit: int
    ):
        user = db.query(User).filter(User.id == id).first()
        if user is None:
            raise NotFoundException(detail=f"User with id: {id} is not found!")
        if type == "write":
            active_badges = [i.id for i in (
                db.query(BadgeType)
                .join(Badge, and_(Badge.type_id == BadgeType.id,
                                  Badge.user_id == id))
                .join(BadgeHistory,
                      and_(Badge.id == BadgeHistory.badge_id,
                           BadgeHistory.date_to == None))
                .all()
            )]
            return [
                BadgeTypeRead.from_orm(badge).dict()
                for badge in db.query(BadgeType)
                .filter(BadgeType.id.notin_(active_badges))
                .filter(
                    BadgeType.name != "Черный Берет")
                .offset(skip)
                .limit(limit)
                .all()
            ]
        else:
            return [BadgeRead.from_orm(badge).dict() for badge in (
                db.query(Badge)
                .join(BadgeHistory,
                      Badge.id == BadgeHistory.badge_id)
                .filter(Badge.user_id == id)
                .filter(BadgeHistory.date_to == None)
                .all()
            )]

    def get_object(self, db: Session, id: str, type: str):
        if type == 'write':
            res = db.query(BadgeType).filter(BadgeType.id == id).first()
        else:
            res = db.query(Badge).filter(Badge.id == id).first().type
        return res

    def get_black_beret(self, db: Session):
        badge_type = (
            db.query(BadgeType).filter(
                BadgeType.name == "Черный Берет").first()
        )
        return badge_type


badge_service = BadgeService(Badge)
