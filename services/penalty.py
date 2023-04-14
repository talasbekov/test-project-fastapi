import uuid
from datetime import datetime

from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import Penalty, PenaltyType, User, PenaltyHistory
from schemas import PenaltyRead, PenaltyCreate, PenaltyUpdate, PenaltyTypeRead
from .base import ServiceBase
from utils import is_valid_uuid


class PenaltyService(ServiceBase[Penalty, PenaltyCreate, PenaltyUpdate]):
    def create_relation(self, db: Session, user_id: uuid.UUID, type_id: uuid.UUID):
        penalty = super().create(db, PenaltyCreate(type_id=type_id, user_id=user_id))
        return penalty

    def get_by_option(
        self, db: Session, option: str, type: str, id: uuid.UUID, skip: int, limit: int
    ):
        if type == "write":
            return [
                PenaltyTypeRead.from_orm(i).dict()
                for i in db.query(PenaltyType).offset(skip).limit(limit).all()
            ]
        else:
            user = db.query(User).filter(User.id == id).first()
            if user is None:
                raise NotFoundException(detail=f"User with id: {id} is not found!")

            return [PenaltyRead.from_orm(penalty).dict() for penalty in user.penalties]

    def get_object(self, db: Session, id: str):
        return db.query(PenaltyType).filter(PenaltyType.id == id).first()

    def stop_relation(self, db: Session, user_id: uuid.UUID, id: uuid.UUID):
        penalty = (
            db.query(PenaltyHistory).filter(PenaltyHistory.penalty_id == id).first()
        )
        if penalty is None:
            raise NotFoundException(detail=f"Penalty with id: {id} is not found!")
        penalty.date_to = datetime.now()
        db.add(penalty)
        db.flush()
        return penalty

    def exists_relation(self, db: Session, user_id: str, badge_type_id: uuid.UUID):
        return (
            db.query(Penalty)
            .filter(Penalty.user_id == user_id)
            .filter(Penalty.type_id == badge_type_id)
            .first()
        ) is not None


penalty_service = PenaltyService(Penalty)
