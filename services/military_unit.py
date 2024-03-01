from models import MilitaryUnit
from schemas import MilitaryUnitCreate, MilitaryUnitUpdate
from services.filter import add_filter_to_query
from .base import ServiceBase
from sqlalchemy.orm import Session


class MilitaryUnitService(
        ServiceBase[MilitaryUnit, MilitaryUnitCreate, MilitaryUnitUpdate]):
    
    def get_all(
        self, db: Session, skip: int = 0, limit: int = 100, filter: str = ''
    ):
        military_units = db.query(MilitaryUnit)

        if filter != '':
            military_units = add_filter_to_query(military_units, filter, MilitaryUnit)

        military_units = (military_units
                       .offset(skip)
                       .limit(limit)
                       .all())

        total = db.query(MilitaryUnit).count()

        return {'total': total, 'objects': military_units}


military_unit_service = MilitaryUnitService(MilitaryUnit)
