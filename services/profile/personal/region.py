from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import Region
from schemas import RegionCreate, RegionUpdate, RegionRead
from services.base import ServiceBase

class RegionService(ServiceBase[Region, RegionCreate, RegionUpdate]):
    def get_region_by_country_id(self, db: Session, country_id: int):
        return db.query(self.model).filter(self.model.country_id == country_id).all()


region_service = RegionService(Region)
