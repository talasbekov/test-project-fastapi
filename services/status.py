import uuid
from datetime import datetime

from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import Status, StatusHistory, StatusType, User
from schemas import StatusRead, StatusCreate, StatusUpdate, StatusTypeRead
from .base import ServiceBase


class StatusService(ServiceBase[Status, StatusCreate, StatusUpdate]):

    def create_relation(self, db: Session, user_id: uuid.UUID, type_id: str):
        status = super().create(db, StatusCreate(type_id=type_id, user_id=user_id))
        return status
    
    def get_object(self, db: Session, id: str):
        return db.query(self.model).filter(StatusType.id == id).first()
    
    def get_by_option(self, db: Session, option: str, type: str, id: uuid.UUID, skip: int, limit: int):
        user = db.query(User).filter(User.id == id).first()
        if user is None:
            raise NotFoundException(detail=f"User with id: {id} is not found!")
        if type == 'write':
            return [StatusTypeRead.from_orm(status).dict() for status in db.query(StatusType).offset(skip).limit(limit).all()]
        else:
            return [StatusRead.from_orm(status).dict() for status in user.statuses]
        
    def stop_relation(self, db: Session, user_id: uuid.UUID, status_id: uuid.UUID):
        history = db.query(StatusHistory).filter(StatusHistory.status_id == status_id).first()
        if history is None:
            raise NotFoundException(detail=f"Status with id: {status_id} is not found!")
        history.date_to = datetime.now()
        db.add(history)
        db.flush()
        return history


status_service = StatusService(Status)
