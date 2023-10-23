from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import SportType
from services.base import ServiceBase
from typing import List


class SportTypeService(ServiceBase):

    def get_by_id(self, db: Session, id: str) -> SportType:

        sport_type = db.query(SportType).filter(SportType.id == id).first()
        if not sport_type:
            raise NotFoundException("Sport type not found")
        return sport_type

    def get_multi(
        self, db: Session, skip: int = 0, limit: int = 100
    ) -> List[SportType]:
        sport_types = (db.query(SportType)
                         .order_by(SportType.created_at.desc())
                         .offset(skip)
                         .limit(limit)
                         .all())
        count = db.query(SportType).count()

        return {"total": count, "objects": sport_types}


sport_type_service = SportTypeService(SportType)
