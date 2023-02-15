from sqlalchemy.orm import Session

from .base import ServiceBase

from models import Position
from schemas import PositionCreate, PositionUpdate
from exceptions.client import NotFoundException


class PositionService(ServiceBase[Position, PositionCreate, PositionUpdate]):
    def get_by_id(self, db: Session, id: str):
        position = super().get(db, id)
        if position is None:
            raise NotFoundException(detail="Position is not found!")
        return position



position_service = PositionService(Position)
