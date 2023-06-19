import uuid
from datetime import datetime

from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import Penalty, PenaltyType, PenaltyHistory
from schemas import PenaltyRead, PenaltyCreate, PenaltyUpdate, PenaltyTypeRead
from .base import ServiceBase


class PenaltyService(ServiceBase[Penalty, PenaltyCreate, PenaltyUpdate]):
    def create_relation(self, db: Session, user_id: uuid.UUID,
                        type_id: uuid.UUID):
        penalty = super().create(db, PenaltyCreate(type_id=type_id, user_id=user_id))
        return penalty

    def get_by_option(
        self, db: Session, type: str, id: uuid.UUID, skip: int, limit: int
    ):
        if type == "write":
            return [
                PenaltyTypeRead.from_orm(i).dict()
                for i in db.query(PenaltyType).offset(skip).limit(limit).all()
            ]
        else:
            penalties = (
                db.query(Penalty)
                .filter(Penalty.user_id == id)
                .join(
                    PenaltyHistory,
                    and_(PenaltyHistory.user_id == id,
                         or_(PenaltyHistory.date_to < datetime.now(),
                             PenaltyHistory.date_to is None)
                         )
                )
            )
            return [PenaltyRead.from_orm(penalty).dict()
                    for penalty in penalties]

    def get_object(self, db: Session, id: str, type: str):
        if type == "write":
            return db.query(PenaltyType).filter(PenaltyType.id == id).first()
        else:
            return db.query(Penalty).filter(Penalty.id == id).first().type

    def stop_relation(self, db: Session, user_id: uuid.UUID, id: uuid.UUID):
        penalty = (
            db.query(PenaltyHistory)
            .filter(
                PenaltyHistory.penalty_id == id,
                PenaltyHistory.user_id == user_id
            ).first()
        )
        if penalty is None:
            raise NotFoundException(
                detail=f"Penalty with id: {id} is not found!")
        penalty.date_to = datetime.now()
        db.add(penalty)
        db.flush()
        return penalty

    def exists_relation(self, db: Session, user_id: str, id: uuid.UUID):
        return (
            db.query(Penalty)
            .filter(Penalty.user_id == user_id)
            .filter(Penalty.id == id)
            .first()
        ) is not None


penalty_service = PenaltyService(Penalty)
