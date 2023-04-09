import uuid

from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import Status, StatusHistory
from schemas import StatusRead, StatusCreate, StatusUpdate
from .base import ServiceBase


class StatusService(ServiceBase[Status, StatusCreate, StatusUpdate]):

    def create_relation(self, db: Session, user_id: uuid.UUID, status_name: str):
        status = super().create(db, StatusCreate(name=status_name, user_id=user_id))
        return status
    
    def get_object(self, db: Session, value: str):
        return db.query(self.model).filter(self.model.name == value).first()


status_service = StatusService(Status)
