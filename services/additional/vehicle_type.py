from sqlalchemy import func, and_
from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import VehicleType
from schemas import VehicleTypeCreate, VehicleTypeUpdate
from services.base import ServiceBase


class VehicleTypeService(ServiceBase[VehicleType, VehicleTypeCreate, VehicleTypeUpdate]):

    def get_all(
        self, db: Session, skip: int = 0, limit: int = 100, filter: str = ''
    ):
        vehicle_types = db.query(VehicleType)

        if filter != '':
            vehicle_types = self._add_filter_to_query(vehicle_types, filter)

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

    def _add_filter_to_query(self, vehicle_type_query, filter):
        key_words = filter.lower().split()
        vehicle_types = (
           vehicle_type_query
            .filter(
                and_(func.concat(func.concat(func.lower(VehicleType.name), ' '),
                                 func.concat(func.lower(VehicleType.nameKZ), ' '))
                     .contains(name) for name in key_words)
            )
        )
        return vehicle_types

vehicle_type_service = VehicleTypeService(VehicleType)
