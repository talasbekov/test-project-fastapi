from sqlalchemy import func, and_

from models import MilitaryUnit
from schemas import MilitaryUnitCreate, MilitaryUnitUpdate
from .base import ServiceBase
from sqlalchemy.orm import Session


class MilitaryUnitService(
        ServiceBase[MilitaryUnit, MilitaryUnitCreate, MilitaryUnitUpdate]):
    
    def get_all(
        self, db: Session, skip: int = 0, limit: int = 100, filter: str = ''
    ):
        military_units = db.query(MilitaryUnit)

        if filter != '':
            military_units = self._add_filter_to_query(military_units, filter)

        military_units = (military_units
                       .offset(skip)
                       .limit(limit)
                       .all())

        total = db.query(MilitaryUnit).count()

        return {'total': total, 'objects': military_units}
    
    
    def _add_filter_to_query(self, military_unit_query, filter):
        key_words = filter.lower().split()
        military_units = (
            military_unit_query
            .filter(
                and_(func.concat(func.concat(func.lower(MilitaryUnit.name), ' '),
                                 func.concat(func.lower(MilitaryUnit.nameKZ), ' '))
                     .contains(name) for name in key_words)
            )
        )
        return military_units


military_unit_service = MilitaryUnitService(MilitaryUnit)
