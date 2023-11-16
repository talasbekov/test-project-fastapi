from typing import List

from sqlalchemy import func, and_
from sqlalchemy.orm import Session

from exceptions import NotFoundException
from models.education import InstitutionDegreeType
from schemas.education import InstitutionDegreeTypeCreate, InstitutionDegreeTypeUpdate
from services import ServiceBase


class InstitutionDegreeTypeService(
        ServiceBase[InstitutionDegreeType,
                    InstitutionDegreeTypeCreate,
                    InstitutionDegreeTypeUpdate]):

    def get_all(
        self, db: Session, skip: int = 0, limit: int = 100, filter: str = ''
    ):
        institutions = db.query(InstitutionDegreeType)

        if filter != '':
            institutions = self._add_filter_to_query(institutions, filter)

        institutions = (institutions
                       .order_by(func.to_char(InstitutionDegreeType.name))
                       .offset(skip)
                       .limit(limit)
                       .all())

        total = db.query(InstitutionDegreeType).count()

        return {'total': total, 'objects': institutions}

    def get_by_id(self, db: Session, id: str):
        institution_degree_type = super().get(db, id)
        if institution_degree_type is None:
            raise NotFoundException(
                detail=f"InstitutionDegreeType with id: {id} is not found!")
        return institution_degree_type

    def _add_filter_to_query(self, sport_type_query, filter):
        key_words = filter.lower().split()
        sport_types = (
            sport_type_query
            .filter(
                and_(func.concat(func.concat(func.lower(InstitutionDegreeType.name), ' '),
                                 func.concat(func.lower(InstitutionDegreeType.nameKZ), ' '))
                     .contains(name) for name in key_words)
            )
        )
        return sport_types

institution_degree_type_service = InstitutionDegreeTypeService(
    InstitutionDegreeType)
