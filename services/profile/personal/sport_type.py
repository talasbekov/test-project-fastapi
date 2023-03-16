from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import SportType
from schemas import SportTypeCreate, SportTypeUpdate, SportTypeRead

from services.base import ServiceBase


class SportTypeService(ServiceBase):

    def get_by_id(self, db: Session, id: str) -> SportType:

        sport_type = db.query(SportType).filter(SportType.id == id).first()
        if not sport_type:
            raise NotFoundException("Sport type not found")
        return sport_type


sport_type_service = SportTypeService(SportType)
