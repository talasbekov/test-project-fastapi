from sqlalchemy import func
from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import SportDegreeType
from services.base import ServiceBase
from typing import List


class SportDegreeTypeService(ServiceBase):

    def get_by_id(self, db: Session, id: str) -> SportDegreeType:

        sport_type = db.query(SportDegreeType).filter(
            SportDegreeType.id == id).first()
        if not sport_type:
            raise NotFoundException("Sport type not found")
        return sport_type

    def get_multi(
        self, db: Session, skip: int = 0, limit: int = 100
    ) -> List[SportDegreeType]:
        sport_types = (db.query(SportDegreeType)
                         .order_by(func.to_char(func.lower(SportDegreeType.name)))
                         .offset(skip)
                         .limit(limit)
                         .all())
        count = db.query(SportDegreeType).count()

        return {"total": count, "objects": sport_types}


sport_degree_type_service = SportDegreeTypeService(SportDegreeType)
