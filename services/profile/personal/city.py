from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import City
from schemas import CityCreate, CityUpdate, CityRead
from services.base import ServiceBase

class CityService(ServiceBase[City, CityCreate, CityUpdate]):
    def get_cities_by_region_id(self, db: Session, region_id: int):
        return db.query(self.model).filter(self.model.region_id == region_id).all()

    def get_cities_by_country_id(self, db: Session, country_id: int):
        return db.query(self.model).filter(self.model.region.country_id == country_id).all()

city_service = CityService(City)
