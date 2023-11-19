from sqlalchemy import func, and_
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

    def get_all(
        self, db: Session, skip: int = 0, limit: int = 100, filter: str = ''
    ):
        sport_types = (db.query(SportDegreeType))

        if filter != '':
            sport_types = self._add_filter_to_query(sport_types, filter)

        sport_types = (sport_types
                       .order_by(func.to_char(func.lower(SportDegreeType.name)))
                       .offset(skip)
                       .limit(limit)
                       .all())

        count = db.query(SportDegreeType).count()

        return {"total": count, "objects": sport_types}

    def _add_filter_to_query(self, sport_type_query, filter):
        key_words = filter.lower().split()
        sport_types = (
            sport_type_query
            .filter(
                and_(func.concat(func.concat(func.lower(SportDegreeType.name), ' '),
                                 func.concat(func.lower(SportDegreeType.nameKZ), ' '))
                     .contains(name) for name in key_words)
            )
        )
        return sport_types

sport_degree_type_service = SportDegreeTypeService(SportDegreeType)
