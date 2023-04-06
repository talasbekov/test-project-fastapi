from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import Coolness
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

coolness_service = CoolnessService(Coolness)
