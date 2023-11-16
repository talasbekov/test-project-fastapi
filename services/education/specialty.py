from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import func, and_

from exceptions import NotFoundException
from models.education import Specialty
from schemas.education import SpecialtyCreate, SpecialtyUpdate
from services import ServiceBase


class SpecialtyService(
        ServiceBase[Specialty, SpecialtyCreate, SpecialtyUpdate]):

    def get_all(
        self, db: Session, skip: int = 0, limit: int = 100, filter: str = ''
    ):
        specialties = db.query(Specialty)

        if filter != '':
            specialties = self._add_filter_to_query(specialties, filter)

        specialties = (specialties
                       .order_by(func.to_char(Specialty.name))
                       .offset(skip)
                       .limit(limit)
                       .all())

        total = db.query(Specialty).count()

        return {'total': total, 'objects': specialties}

    def get_by_id(self, db: Session, id: str):
        specialty = super().get(db, id)
        if specialty is None:
            raise NotFoundException(
                detail=f"Specialty with id: {id} is not found!")
        return specialty

    def _add_filter_to_query(self, sport_type_query, filter):
        key_words = filter.lower().split()
        sport_types = (
            sport_type_query
            .filter(
                and_(func.concat(func.concat(func.lower(Specialty.name), ' '),
                                 func.concat(func.lower(Specialty.nameKZ), ' '))
                     .contains(name) for name in key_words)
            )
        )
        return sport_types


specialty_service = SpecialtyService(Specialty)
