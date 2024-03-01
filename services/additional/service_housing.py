from typing import Union, Dict, Any
from datetime import datetime

from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from exceptions.client import NotFoundException
from models import ServiceHousing
from schemas import ServiceHousingCreate, ServiceHousingUpdate
from services.base import ServiceBase


class ServiceHousingService(
        ServiceBase[ServiceHousing, ServiceHousingCreate, ServiceHousingUpdate]):

    def create(self, db: Session,
               obj_in: Union[ServiceHousingCreate, Dict[str, Any]]) -> ServiceHousing:
        obj_in_data = jsonable_encoder(obj_in)
        obj_in_data['issue_date'] = datetime.strptime(
            obj_in_data['issue_date'][:10], '%Y-%m-%d')
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.flush()
        return db_obj

    def get_by_id(self, db: Session, id: str) -> ServiceHousing:
        obj = db.query(ServiceHousing).filter(ServiceHousing.id == id).first()
        if not obj:
            raise NotFoundException("ServiceHousing not found")
        return obj


service_housing_service = ServiceHousingService(ServiceHousing)
