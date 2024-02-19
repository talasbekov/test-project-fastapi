from sqlalchemy import func
from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import VehicleType
from schemas import VehicleTypeCreate, VehicleTypeUpdate
from services.base import ServiceBase
from services.filter import add_filter_to_query


class VehicleTypeService(ServiceBase[VehicleType, VehicleTypeCreate, VehicleTypeUpdate]):

    def get_all(
        self, db: Session, skip: int = 0, limit: int = 100, filter: str = ''
    ):
        vehicle_types = db.query(VehicleType)

        if filter != '':
            vehicle_types = add_filter_to_query(vehicle_types, filter, VehicleType)

        vehicle_types = (vehicle_types
                     .order_by(func.to_char(VehicleType.name))
                     .offset(skip)
                     .limit(limit)
                     .all())

        total = db.query(VehicleType).count()

        return {'total': total, 'objects': vehicle_types}

    def get_by_id(self, db: Session, id: str):
        vehicle_type = super().get(db, id)
        if vehicle_type is None:
            raise NotFoundException(
                detail=f"Violation with id: {id} is not found!")
        return vehicle_type


vehicle_type_service = VehicleTypeService(VehicleType)
