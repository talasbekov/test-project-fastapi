from typing import List

from sqlalchemy import and_, func
from sqlalchemy.orm import Session

from models import Position
from schemas import PositionCreate, PositionUpdate
from services import ServiceBase


class PositionService(ServiceBase[Position, PositionCreate, PositionUpdate]):

    def get_without_special(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        filter: str = ''
    ):
        specials = ['Умер', 'Погиб', 'В запасе', 'В отставке']
        positions = (db.query(Position))
        if filter != '':
            positions = self._add_filter_to_query(positions, filter)
        positions = (positions
                     .filter(Position.name.notin_(specials))
                     .order_by(Position.name)
                     .offset(skip)
                     .limit(limit)
                     .all())
        count = db.query(Position).filter(Position.name.notin_(specials)).count()
        return {"total": count, "objects": positions}

    def get_multi(
        self, db: Session, skip: int = 0, limit: int = 100, filter: str = ''
    ):
        positions = (db.query(Position))
        if filter != '':
            positions = self._add_filter_to_query(positions, filter)
        positions = (positions
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

    def get_lower_positions(
        self,
        db: Session,
        position_id: str,
    ) -> List[Position]:
        position = self.get_by_id(db, position_id)
        specials = ['Умер', 'Погиб', 'В запасе', 'В отставке']
        positions = (db.query(Position)
                     .filter(Position.name.notin_(specials))
                     .filter(Position.position_order < position.position_order)
                     .order_by(Position.position_order.desc())
                     .all())

        return positions

    def _add_filter_to_query(self, position_query, filter):
        key_words = filter.lower().split()
        positions = (
            position_query
            .filter(
                and_(func.concat(func.concat(func.lower(Position.name), ' '),
                                 func.concat(func.lower(Position.nameKZ), ' '))
                     .contains(name) for name in key_words)
            )
        )
        return positions


position_service = PositionService(Position)  # type: ignore
