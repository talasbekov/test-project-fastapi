from typing import List

from sqlalchemy import func, and_
from sqlalchemy.orm import Session

from exceptions import NotFoundException
from models.education import Institution
from schemas.education import InstitutionCreate, InstitutionUpdate
from services import ServiceBase


class InstitutionService(
        ServiceBase[Institution, InstitutionCreate, InstitutionUpdate]):

    def get_all(
        self, db: Session, skip: int = 0, limit: int = 100, filter: str = ''
    ):
        institutions = db.query(Institution)

        if filter != '':
            institutions = self._add_filter_to_query(institutions, filter)

        institutions = (institutions
                       .order_by(func.to_char(Institution.name))
                       .offset(skip)
                       .limit(limit)
                       .all())

        total = db.query(Institution).count()

        return {'total': total, 'objects': institutions}

    def get_by_id(self, db: Session, id: str):
        institution = super().get(db, id)
        if institution is None:
            raise NotFoundException(
                detail=f"Institution with id: {id} is not found!")
        return institution

    def _add_filter_to_query(self, sport_type_query, filter):
        key_words = filter.lower().split()
        sport_types = (
            sport_type_query
            .filter(
                and_(func.concat(func.concat(func.lower(Institution.name), ' '),
                                 func.concat(func.lower(Institution.nameKZ), ' '))
                     .contains(name) for name in key_words)
            )
        )
        return sport_types


institution_service = InstitutionService(Institution)
