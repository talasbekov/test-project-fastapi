from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import Vehicle
from schemas import VehicleCreate, VehicleUpdate
from services.base import ServiceBase
from typing import Union, Dict, Any
from fastapi.encoders import jsonable_encoder
from datetime import datetime
from utils.date import parse_datetime


class VehicleService(ServiceBase[Vehicle, VehicleCreate, VehicleUpdate]):
    def get_by_id(self, db: Session, id: str):
        vehicle = super().get(db, id)
        if vehicle is None:
            raise NotFoundException(detail="Vehicle is not found!")
        return vehicle

    def create(self, db: Session,
            obj_in: Union[VehicleCreate, Dict[str, Any]]) -> Vehicle:
        obj_in_data = jsonable_encoder(obj_in)
        obj_in_data['date_from'] = parse_datetime(obj_in_data['date_from'])
        db_obj = self.model(**obj_in_data) 
        db.add(db_obj)
        db.flush()
        return db_obj

vehicle_service = VehicleService(Vehicle)
