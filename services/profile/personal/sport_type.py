from sqlalchemy import func, and_
from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import SportType
from services.base import ServiceBase
from utils import add_filter_to_query


class SportTypeService(ServiceBase):

    def get_by_id(self, db: Session, id: str) -> SportType:

        sport_type = db.query(SportType).filter(SportType.id == id).first()
        if not sport_type:
            raise NotFoundException("Sport type not found")
        return sport_type

    def get_all(
        self, db: Session, skip: int = 0, limit: int = 100, filter: str = ''
    ):
        sport_types = (db.query(SportType))

        if filter != '':
            sport_types = add_filter_to_query(sport_types, filter, SportType)

        sport_types = (sport_types
                       .order_by(func.to_char(func.lower(SportType.name)))
                       .offset(skip)
                       .limit(limit)
                       .all())

        count = db.query(SportType).count()

        return {"total": count, "objects": sport_types}


sport_type_service = SportTypeService(SportType)
