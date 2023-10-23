from typing import List
from sqlalchemy.orm import Session

from models import Position
from schemas import PositionCreate, PositionUpdate
from services import ServiceBase


class PositionService(ServiceBase[Position, PositionCreate, PositionUpdate]):

    def get_without_special(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100
    ) -> List[Position]:
        specials = ['Умер', 'Погиб', 'В запасе', 'В отставке']
        positions = (db.query(Position)
                     .filter(Position.name.notin_(specials))
                     .offset(skip)
                     .limit(limit)
                     .all())

        return positions

    def get_multi(
        self, db: Session, skip: int = 0, limit: int = 100
    ) -> List[Position]:
        positions = (db.query(Position)
                       .order_by(Position.name)
                       .offset(skip)
                       .limit(limit)
                       .all())
        count = db.query(Position).count()
        return {"total": count, "objects": positions}

    def get_id_by_name(self, db: Session, name: str):
        role = db.query(Position).filter(
            Position.name == name
        ).first()

        if role:
            return role.id
        else:
            return None


position_service = PositionService(Position)  # type: ignore
