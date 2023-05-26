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

    def get_object(self, db: Session, id: str, type: str):
        if type == 'write':
            return db.query(StatusType).filter(StatusType.id == id).first()
        else:
            return db.query(Status).filter(Status.id == id).first().type

    def get_by_option(self, db: Session, type: str, id: uuid.UUID, skip: int, limit: int):
        user = db.query(User).filter(User.id == id).first()
        if user is None:
            raise NotFoundException(detail=f"User with id: {id} is not found!")
        if type == 'write':
            return [StatusTypeRead.from_orm(status).dict() for status in
                    db.query(StatusType).offset(skip).limit(limit).all()]
        else:
            return [StatusRead.from_orm(status).dict() for status in user.statuses]

    def stop_relation(self, db: Session, user_id: uuid.UUID, status_id: uuid.UUID):
        history = (db.query(StatusHistory)
                   .filter(StatusHistory.status_id == status_id)
                   .order_by(StatusHistory.created_at.desc()).first())
        if history is None:
            raise NotFoundException(detail=f"Status with id: {status_id} is not found!")
        history.date_to = datetime.now()
        db.add(history)
        db.flush()
        return history

    def exists_relation(self, db: Session, user_id: str, badge_type_id: uuid.UUID):
        return (
            db.query(Status)
            .filter(Status.user_id == user_id)
            .filter(Status.type_id == badge_type_id)
            .first()
        ) is not None


status_service = StatusService(Status)
