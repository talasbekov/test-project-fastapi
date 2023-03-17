from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import Equipment
from schemas import EquipmentCreate, EquipmentUpdate
from .base import ServiceBase


class EquipmentService(ServiceBase[Equipment, EquipmentCreate, EquipmentUpdate]):
    def get_by_id(self, db: Session, id: str):
        equipment = super().get(db, id)
        if equipment is None:
            raise NotFoundException(detail="Equipment is not found!")
        return equipment


equipment_service = EquipmentService(Equipment)
