import uuid
from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import Status, StatusHistory, StatusType, User
from schemas import StatusRead, StatusCreate, StatusUpdate, StatusTypeRead
from services import user_service
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
        user = user_service.get_by_id(db, id)
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
            .join(StatusHistory)
            .filter(StatusHistory.date_to == None | StatusHistory.date_to > datetime.now())
            .first()
        ) is not None

    def get_by_name(self, db: Session, name: str):
        return db.query(StatusType).filter(func.lower(StatusType.name).contains(name.lower())).all()

    def get_active_status_of_user(self, db: Session, user_id: uuid.UUID, status_name: str):
        return (
            db.query(StatusHistory)
            .filter(StatusHistory.date_to == None | StatusHistory.date_to > datetime.now())
            .join(Status)
            .filter(Status.user_id == user_id)
            .join(StatusType)
            .filter(func.lower(StatusType.name).contains(status_name.lower()))
            .all()
        )


status_service = StatusService(Status)
