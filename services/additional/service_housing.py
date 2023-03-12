from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import ServiceHousing
from services.base import ServiceBase
from schemas import ServiceHousingCreate, ServiceHousingUpdate


class ServiceHousingService(ServiceBase[ServiceHousing, ServiceHousingCreate, ServiceHousingUpdate]):

    def get_by_id(self, db: Session, id: str) -> ServiceHousing:
        obj = db.query(ServiceHousing).filter(ServiceHousing.id == id).first()
        if not obj:
            raise NotFoundException("ServiceHousing not found")
        return obj
    

service_housing_service = ServiceHousingService(ServiceHousing)
