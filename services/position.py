from sqlalchemy.orm import Session

from models import (Position)
from schemas import PositionCreate, PositionUpdate
from services import ServiceBase


class PositionService(ServiceBase[Position, PositionCreate, PositionUpdate]):

    def get_by_name(self, db: Session, name: str):
        role = db.query(Position).filter(
            Position.name == name
        ).first()

        if role:
            return role.id
        else:
            return None

position_service = PositionService(Position)  # type: ignore
