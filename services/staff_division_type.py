from typing import Optional, List

from sqlalchemy.orm import Session

from exceptions.client import NotFoundException
from models import StaffDivisionType
from schemas import StaffDivisionTypeCreate, StaffDivisionTypeUpdate
from .base import ServiceBase


class StaffDivisionTypeService(
        ServiceBase[StaffDivisionType, StaffDivisionTypeCreate, StaffDivisionTypeUpdate]):

    def get_by_id(self, db: Session, id: str) -> StaffDivisionType:
        type = super().get(db, id)
        if type is None:
            raise NotFoundException(
                detail=f"StaffDivisionType with id: {id} is not found!")
        return type

    def get_by_name(self, db: Session,
                    name: str) -> Optional[StaffDivisionType]:
        return db.query(self.model).filter(self.model.name == name).first()

    def get_by_names(self, db: Session,
                     names: List[str]) -> List[StaffDivisionType]:
        return db.query(self.model).filter(self.model.name.in_(names)).all()


staff_division_type_service = StaffDivisionTypeService(StaffDivisionType)
