from typing import List

from sqlalchemy import func
from sqlalchemy.orm import Session

from models import Position, PositionType
from schemas import PositionCreate, PositionUpdate, PositionReadShort, PositionPaginationRead
from services import ServiceBase
from services.filter import add_filter_to_query


class PositionService(ServiceBase[Position, PositionCreate, PositionUpdate]):

    def get_without_special(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        filter: str = ''
    ):
        specials = ['Умер', 'Погиб', 'В запасе', 'В отставке']
        positions = (db.query(Position).join(PositionType))
        if filter != '':
            positions = add_filter_to_query(positions, filter, PositionType)
        positions = (positions
                     .filter(PositionType.name.notin_(specials))
                     .order_by(PositionType.name)
                     .offset(skip)
                     .limit(limit)
                     .all())
        count = db.query(Position).join(PositionType).filter(PositionType.name.notin_(specials)).count()
        return {"total": count, "objects": positions}

    def get_multi(
        self, db: Session, skip: int = 0, limit: int = 100, filter: str = ''
    ):
        positions = (db.query(Position).join(PositionType))
        if filter != '':
            positions = add_filter_to_query(positions, filter, PositionType)
        positions = (positions
                       .order_by(PositionType.name)
                       .offset(skip)
                       .limit(limit)
                       .all())
        count = db.query(Position).count()
        return {"total": count, "objects": positions}

    def get_id_by_name(self, db: Session, name: str):
        role = db.query(Position).join(PositionType).filter(
            func.lower(PositionType.name) == name.lower()
        ).first()

        if role:
            return role.id
        else:
            return None

    def get_id_by_name_like(self, db: Session, name: str):
        role = db.query(Position).join(PositionType).filter(
            func.lower(PositionType.name).ilike(f'%{name.lower()}%')
        ).first()

        if role:
            return role.id
        else:
            return None

    def get_type_id_by_name(self, db: Session, name: str):
        role = db.query(PositionType).filter(
            func.lower(PositionType.name) == name.lower()
        ).first()

        if role:
            return role.id
        else:
            return None
    def get_type_id_by_names(self, db: Session, name: str, nameKZ: str):
        role = db.query(PositionType).filter(
            func.lower(PositionType.name) == name.lower()
        ).filter(
            func.lower(PositionType.nameKZ) == nameKZ.lower()
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
        positions = (db.query(Position).join(PositionType)
                     .filter(PositionType.name.notin_(specials))
                     .filter(Position.position_order < position.position_order)
                     .order_by(Position.position_order.desc())
                     .all())

        return positions

    def create(self, db, body):
        position_type_id = self.get_type_id_by_names(db, body.name, body.nameKZ)
        if position_type_id is None:
            position_type_id = super().create(db,
                                           PositionType(name=body.name,
                                                        nameKZ=body.nameKZ),
                                           PositionType).id
        position = Position(type_id=position_type_id,
                            max_rank_id=body.max_rank_id,
                            category_code=body.category_code,
                            form=body.form,
                            name=body.name, # maybe there is a flaw in the logic 
                            nameKZ=body.nameKZ) # maybe there is a flaw in the logic 
        position = super().create(db, position, Position)

        db.add(position)
        db.flush()
        return position

    def update(self, db, id, body):
        position = self.get_by_id(db, id)
        position_type_id = self.get_type_id_by_names(db, body.name, body.nameKZ)
        if position_type_id is None:
            position_type = super().create(db,
                                           PositionType(name=body.name,
                                                        nameKZ=body.nameKZ),
                                           PositionType)
            print("success")
            position_type_id = position_type.id
            # db.add(position_type)
            
        position.type_id = position_type_id
        # position.max_rank_id = body.max_rank_id
        position.category_code = body.category_code
        position.form = body.form
        position.name = body.name
        position.nameKZ = body.nameKZ
        db.add(position)
            
        db.flush()
        return position
    def get_short_positions(self, db: Session):
        positions = db.query(Position).all()
        return [PositionReadShort.from_orm(position) for position in positions]
position_service = PositionService(Position)  # type: ignore
