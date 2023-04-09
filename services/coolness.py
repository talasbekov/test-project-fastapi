import uuid

from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import Coolness, CoolnessType
from schemas import CoolnessCreate, CoolnessRead, CoolnessUpdate
from .base import ServiceBase


class CoolnessService(ServiceBase[Coolness, CoolnessCreate, CoolnessUpdate]):

    def get_by_id(self, db: Session, id: str):
        rank = super().get(db, id)
        if rank is None:
            raise NotFoundException(detail=f"Coolness with id: {id} is not found!")
        return rank

    def get_by_user_id(self, db: Session, user_id: str):
        coolness = db.query(self.model).filter(self.model.user_id == user_id).first()
        return coolness
    
    def create_relation(self, db: Session, user_id: str, type_id: uuid.UUID):
        coolness = super().create(db, CoolnessCreate(user_id=user_id, type_id=type_id))
        return coolness
    
    def get_by_option(self, db: Session, skip: int, limit: int):
        return [i for i in db.query(CoolnessType).offset(skip).limit(limit).all()]

    def get_object(self, db: Session, id: str):
        return db.query(CoolnessType).filter(CoolnessType.id == id).first()


coolness_service = CoolnessService(Coolness)
