from sqlalchemy.orm import Session

from typing import Union, Dict, Any, List
from fastapi.encoders import jsonable_encoder
from exceptions.client import NotFoundException
from models import SportDegree
from schemas import SportDegreeCreate, SportDegreeUpdate
from services.base import ServiceBase
from datetime import datetime


class SportDegreeService(
        ServiceBase[SportDegree, SportDegreeCreate, SportDegreeUpdate]):

    def create(self, db: Session,
               obj_in: Union[SportDegreeCreate, Dict[str, Any]]) -> SportDegree:
        obj_in_data = jsonable_encoder(obj_in)
        obj_in_data['assignment_date'] = datetime.strptime(
            obj_in_data['assignment_date'], '%Y-%m-%d')
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.flush()
        return db_obj

    def get_multi(
        self, db: Session, skip: int = 0, limit: int = 100
    ) -> List[SportDegree]:
        return (db.query(SportDegree)
                  .order_by(SportDegree.name)
                  .offset(skip)
                  .limit(limit)
                  .all())

    def get_by_id(self, db: Session, id: str):
        sport_degree = super().get(db, id)
        if sport_degree is None:
            raise NotFoundException(
                detail=f"SportDegree with id: {id} is not found!")
        return sport_degree


sport_degree_service = SportDegreeService(SportDegree)
