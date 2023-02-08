from sqlalchemy.orm import Session

from .base import ServiceBase

from models import Equipment
from schemas import EquipmentCreate, EquipmentUpdate
from exceptions.client import NotFoundException


class EquipmentService(ServiceBase[Equipment, EquipmentCreate, EquipmentUpdate]):
    def get_by_id(self, db: Session, id: str):
        equipment = super().get(db, id)
        if equipment is None:
            raise NotFoundException(detail="Equipment is not found!")


equipment_service = EquipmentService(Equipment)
