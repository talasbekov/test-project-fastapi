import uuid
from datetime import datetime

from sqlalchemy.orm import Session

from core import Base
from models import Secondment, StaffDivision, SecondmentHistory
from schemas import SecondmentCreate, SecondmentUpdate, StaffDivisionOptionRead
from services import staff_division_service
from utils import is_valid_uuid

from .base import ServiceBase


class SecondmentService(ServiceBase[Secondment, SecondmentCreate, SecondmentUpdate]):

    def create_relation(self, db: Session, user_id: uuid.UUID, value):
        if isinstance(value, Base):
            if isinstance(value, StaffDivision):
                status = super().create(db, SecondmentCreate(user_id=user_id, staff_division_id=value.id, name=value.name, nameKZ=value.nameKZ))
            else:
                status = super().create(db, SecondmentCreate(user_id=user_id, state_body_id=value.id, name=value.name, nameKZ=value.nameKZ))
        else:
            status = super().create(db, SecondmentCreate(user_id=user_id, staff_division_id=None, name=value))
        return status
    
    def get_by_option(self, db: Session, type: str, id: uuid.UUID, skip: int, limit: int):
        if id is None:
            return [StaffDivisionOptionRead.from_orm(i) for i in staff_division_service.get_all_parents(db, skip, limit)]
        return [StaffDivisionOptionRead.from_orm(i) for i in staff_division_service.get_child_groups(db, id, skip, limit)]


    def get_object(self, db: Session, value: str, type: str):
        if is_valid_uuid(value):
            return db.query(StaffDivision).filter(StaffDivision.id == value).first()
        return db.query(self.model).filter(self.model.name == value).first()

    def stop_relation(self, db: Session, user_id: uuid.UUID, id: uuid.UUID):
        db.query(SecondmentHistory).filter(SecondmentHistory.secondment_id == id).update({SecondmentHistory.date_to: datetime.now()})


secondment_service = SecondmentService(Secondment)
