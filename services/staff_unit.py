from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import StaffUnit
from schemas import StaffUnitCreate, StaffUnitUpdate

from .base import ServiceBase


class StaffUnitService(ServiceBase[StaffUnit, StaffUnitCreate, StaffUnitUpdate]):
    def get_by_id(self, db: Session, id: str):
        position = super().get(db, id)
        if position is None:
            raise NotFoundException(detail="StaffUnit is not found!")
        return position


staff_unit_service = StaffUnitService(StaffUnit)
