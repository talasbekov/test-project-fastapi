import uuid

from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import Penalty, PenaltyType
from schemas import PenaltyRead, PenaltyCreate, PenaltyUpdate
from .base import ServiceBase
from utils import is_valid_uuid


class PenaltyService(ServiceBase[Penalty, PenaltyCreate, PenaltyUpdate]):
    
    def create_relation(self, db: Session, user_id: uuid.UUID, type_id: uuid.UUID):
        penalty = super().create(db, PenaltyCreate(type_id=type_id, user_id=user_id))
        return penalty
    
    def get_by_option(self, db: Session, skip: int, limit: int):
        return [i for i in db.query(PenaltyType).offset(skip).limit(limit).all()]


penalty_service = PenaltyService(Penalty)
