import uuid
from datetime import datetime

from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import Coolness, CoolnessType, User, CoolnessHistory
from schemas import CoolnessCreate, CoolnessRead, CoolnessUpdate, CoolnessTypeRead
from .base import ServiceBase


class CoolnessService(ServiceBase[Coolness, CoolnessCreate, CoolnessUpdate]):
    def get_by_id(self, db: Session, id: str):
        rank = super().get(db, id)
        if rank is None:
            raise NotFoundException(
                detail=f"Coolness with id: {id} is not found!")
        return rank

    def get_by_user_id(self, db: Session, user_id: str):
        coolness = db.query(
            self.model).filter(
            self.model.user_id == user_id).first()
        return coolness

    def create_relation(self, db: Session, user_id: str, type_id: str):
        coolness = super().create(db, CoolnessCreate(user_id=user_id, type_id=type_id))
        return coolness

    def get_by_option(
        self, db: Session, type: str, id: str, skip: int, limit: int
    ):
        if type == "write":
            return [
                CoolnessTypeRead.from_orm(i).dict()
                for i in db.query(CoolnessType).offset(skip).limit(limit).all()
            ]
        else:
            user = db.query(User).filter(User.id == id).first()
            if user is None:
                raise NotFoundException(
                    detail=f"User with id: {id} is not found!")
            res = (
                db.query(Coolness)
                .filter(Coolness.user_id == id)
                .join(CoolnessHistory, CoolnessHistory.coolness_id == Coolness.id)
                .filter(CoolnessHistory.date_to == None)
                .all()
            )
            return [CoolnessRead.from_orm(status).dict() for status in res]

    def get_object(self, db: Session, id: str, type: str):
        if type == "write":
            return db.query(CoolnessType).filter(CoolnessType.id == id).first()
        else:
            return db.query(Coolness).filter(Coolness.id == id).first().type

    def stop_relation(self, db: Session, user_id: str, id: str):
        res = (
            db.query(CoolnessHistory).filter(
                CoolnessHistory.coolness_id == id).first()
        )
        if res is None:
            raise NotFoundException(
                detail=f"Coolness with id: {id} is not found!")
        res.date_to = datetime.now()
        db.add(res)
        db.flush()
        db.refresh(res)
        return res

    def exists_relation(self, db: Session, user_id: str,
                        coolness_type_id: str):
        return (
            db.query(Coolness)
            .filter(Coolness.user_id == user_id)
            .filter(Coolness.type_id == coolness_type_id)
            .first()
        ) is not None

    def get_relation(self, db: Session, user_id: str,
                     coolness_type_id: str):
        return (
            db.query(Coolness)
            .filter(Coolness.user_id == user_id)
            .filter(Coolness.type_id == coolness_type_id)
            .first()
        )

    def get_type_by_order(self, db: Session, order: int):
        return db.query(CoolnessType).filter(
            CoolnessType.order == order).first()
        
    def get_all_types(self, db: Session):
        return db.query(CoolnessType).all()


coolness_service = CoolnessService(Coolness)
