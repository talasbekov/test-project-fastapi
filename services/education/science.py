from typing import List

from sqlalchemy import func, and_
from sqlalchemy.orm import Session

from exceptions import NotFoundException
from models.education import Science
from schemas.education import ScienceCreate, ScienceUpdate
from services import ServiceBase


class ScienceService(ServiceBase[Science, ScienceCreate, ScienceUpdate]):

    def get_all(
        self, db: Session, skip: int = 0, limit: int = 100, filter: str = ''
    ):
        sciences = db.query(Science)

        if filter != '':
            sciences = self._add_filter_to_query(sciences, filter)

        sciences = (sciences
                     .order_by(func.to_char(Science.name))
                     .offset(skip)
                     .limit(limit)
                     .all())

        total = db.query(Science).count()

        return {'total': total, 'objects': sciences}

    def get_by_id(self, db: Session, id: str):
        science = super().get(db, id)
        if science is None:
            raise NotFoundException(
                detail=f"Science with id: {id} is not found!")
        return science
    
    def _add_filter_to_query(self, science_query, filter):
        key_words = filter.lower().split()
        sciences = (
            science_query
            .filter(
                and_(func.concat(func.concat(func.lower(Science.name), ' '),
                                 func.concat(func.lower(Science.nameKZ), ' '))
                     .contains(name) for name in key_words)
            )
        )
        return sciences

science_service = ScienceService(Science)
