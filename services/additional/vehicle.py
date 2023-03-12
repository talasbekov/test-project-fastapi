from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import Vehicle
from services.base import ServiceBase
from schemas import VehicleCreate, VehicleUpdate


class VehicleService(ServiceBase[Vehicle, VehicleCreate, VehicleUpdate]):
    def get_by_id(self, db: Session, id: str):
        vehicle = super().get(db, id)
        if vehicle is None:
            raise NotFoundException(detail="Vehicle is not found!")
        return vehicle
    

vehicle_service = VehicleService(Vehicle)
